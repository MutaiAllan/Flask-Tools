from flask import Flask, request, redirect, url_for, make_response, send_from_directory, jsonify
from werkzeug.utils import secure_filename
import os
import base64

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return make_response("Select file", 400)
        files = request.files.getlist('file')
        # if user does not select file, browser also
        # submit an empty part without filename
        for file in files:
            if file.filename == '':
                return redirect(request.url)
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return make_response("Files uploaded successfully", 200)
    
        # if file.filename == '':
        #     return make_response("Upload file", 400)
        # if file and allowed_file(file.filename):
        #     filename = secure_filename(file.filename)
        #     file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        #     return make_response("File uploaded successfully", 200)
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@app.route('/uploads/<path:filename>', methods=['GET'])
def download_file(filename):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    except FileNotFoundError:
        return make_response("File not found", 404)
    
def encode_file(file_path):
    with open(file_path, 'rb') as f:
        encoded_bytes = base64.b64encode(f.read())
        return encoded_bytes.decode('utf-8')

@app.route('/files', methods=['GET'])
def get_files():
    try:
        files_data = {}
        for root, _, files in os.walk(app.config['UPLOAD_FOLDER']):
            for file in files:
                file_path = os.path.join(root, file)
                files_data[file] = encode_file(file_path)
        return jsonify(files_data)
    except Exception as e:
        return make_response(str(e), 500)
    

if __name__ == '__main__':
    app.run(debug=True)
