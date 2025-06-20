# claims.py
import requests
import os
from dotenv import load_dotenv
from datetime import date

load_dotenv()  # Load variables from .env file

API_KEY = os.getenv("CURACELL_API_KEY")

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def submit_claim():
    payload = {
        "hmo_code": "curacel_hmo_001",
        "hmo_id": 1234,
        "provider_code": "provider_xyz_001",
        "enrollee": {
            "insurance_no": "INS-0012345",
            "first_name": "Jane",
            "last_name": "Doe",
            "is_floating": False,
            "create_if_not_found": True
        },
        "encounter_date": str(date.today()),
        "admission_date": str(date.today()),
        "discharge_date": str(date.today()),
        "diagnoses": {
            "icd_codes": ["E11.9"],
            "names": ["Type 2 Diabetes Mellitus without complications"]
        },
        "pa_code": "PA-20250619-001",
        "items": [
            {
                "description": "Insulin therapy (30 days)",
                "unit_price_billed": 2000,
                "qty": 1,
                "tariff_code": "TAR001",
                "tariff_id": 0
            }
        ],
        "is_draft": False,
        "ref": "CLAIM-JDOE-0001",
        "auto_vet": True,
        "create_missing_tariffs": True,
        "attachments": []
    }

    response = requests.post(
        "https://api.sandbox.claims.curacel.co/",
        json=payload,
        headers=headers
    )

    print("Status Code:", response.status_code)
    print("Response:", response.json())

if __name__ == "__main__":
    submit_claim()
