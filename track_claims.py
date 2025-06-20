from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("CURACEL_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Accept": "application/json"
}

@app.route('/track-claim', methods=['GET'])
def track_claim():
    insurance_no = request.args.get('insurance_no')
    claim_ref = request.args.get('claim_ref')

    if not insurance_no and not claim_ref:
        return jsonify({"error": "Please provide either insurance_no or claim_ref"}), 400

    url = "https://api.sandbox.claims.curacel.co/api/v1/claims"
    params = {}
    if insurance_no:
        params['insurance_no'] = insurance_no
    if claim_ref:
        params['ref'] = claim_ref

    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code == 200:
        claims = response.json()
        return jsonify({"claims": claims})
    else:
        return jsonify({"error": response.text}), response.status_code

if __name__ == '__main__':
    app.run(debug=True)
