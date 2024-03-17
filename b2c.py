from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/mpesa_b2c_payment', methods=['POST'])
def mpesa_b2c_payment():
    # Your MPESA API credentials
    consumer_key = ''
    consumer_secret = ''
    api_url = 'https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest'

    # Request headers
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer token_here'
    }

    # Request payload
    payload = request.get_json()

    # Make the MPESA B2C payment request
    response = requests.post(api_url, headers=headers, json=payload)

    # Return the response to the client
    return jsonify(response.json())

def get_access_token(consumer_key, consumer_secret):
    # Get the MPESA API access token
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))

    # Extract and return the access token
    return response.json().get('access_token')

if __name__ == '__main__':
    app.run(debug=True)
