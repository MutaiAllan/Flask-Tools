import os
import logging
import boto3
from flask import Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from myapp.models import Organisations, db  # Adjust the import to match your project structure

app = Flask(__name__)

# AWS S3 Configuration
S3_BUCKET = 'your-s3-bucket-name'
S3_REGION = 'your-s3-region'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

s3_client = boto3.client('s3', region_name=S3_REGION)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_unique_filename(filename, org_name):
    name, extension = os.path.splitext(filename)
    organisation_name = org_name.strip().split()
    unique_filename = organisation_name[0] + extension
    return unique_filename

@app.route("/api/v1/admin/create_org", methods=["POST"])
@jwt_required()  # Protect the route with JWT authentication
def create_org():
    try:
        current_user = get_jwt_identity()

        data = request.form
        expected_fields = ["org_name", "org_description", "domain"]
        for field in expected_fields:
            if field not in data:
                return jsonify({"message": f"{field} is required"}), 400

        org_name = data['org_name']
        org_description = data['org_description']
        domain = data['domain']

        if 'file' not in request.files:
            return jsonify({"message": "No file selected"}), 404
        files = request.files.getlist('file')

        for file in files:
            if file.filename == '':
                return jsonify({"message": "Title required"}), 406
            if file and allowed_file(file.filename):
                unique_filename = generate_unique_filename(file.filename, org_name)
                file_name = secure_filename(unique_filename)

                # Upload to S3
                try:
                    s3_client.upload_fileobj(
                        file,
                        S3_BUCKET,
                        file_name,
                        ExtraArgs={'ACL': 'public-read', 'ContentType': file.content_type}
                    )
                    file_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_name}"
                except Exception as e:
                    logging.error(f"Error uploading file to S3: {e}")
                    return jsonify({"message": "File upload failed"}), 500

        existing_org = Organisations.query.filter_by(org_name=org_name).first()
        if existing_org:
            return jsonify({'error': 'Organisation name already exists!'}), 403

        new_org = Organisations(
            org_name=org_name,
            org_description=org_description,
            owner_id=current_user,
            logo=file_name,
            domain=domain
        )

        db.session.add(new_org)
        db.session.commit()

        # Function to update organisation order
        update_org_order()

        return jsonify({"message": "Organisation created successfully!"}), 201
    except Exception as e:
        logging.error(f"Error creating an organisation: {e}")
        return jsonify({"message": "An error occurred"}), 500
