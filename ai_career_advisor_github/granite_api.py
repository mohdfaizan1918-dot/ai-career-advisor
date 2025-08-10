import os
import requests

API_KEY = os.getenv("IBM_API_KEY")
BASE_URL = os.getenv("IBM_URL")
MODEL_ID = os.getenv("GRANITE_MODEL_ID", "ibm/granite-13b-chat-v2")
PROJECT_ID = os.getenv("IBM_PROJECT_ID")
VERSION = os.getenv("IBM_API_VERSION", "2024-05-29")

def get_access_token():
    iam_url = "https://iam.cloud.ibm.com/identity/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "apikey": API_KEY,
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
    }
    response = requests.post(iam_url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception(f"IAM token error: {response.status_code} - {response.text}")

def call_granite(prompt, max_tokens=300):
    token = get_access_token()
    url = f"{BASE_URL}/ml/v1/text/generation?version={VERSION}"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "model_id": MODEL_ID,
        "input": prompt,
        "project_id": PROJECT_ID,
        "parameters": {
            "max_new_tokens": max_tokens
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data.get("results", [{}])[0].get("generated_text", "")
    else:
        raise Exception(f"Granite API Error: {response.status_code} - {response.text}")
