from ibm_watson_machine_learning import APIClient
import os

def test_ibm_connection():
    try:
        # IBM Cloud credentials
        wml_credentials = {
            "url": "https://us-south.ml.cloud.ibm.com",
            "apikey": "cpd-apikey-IBMid-698000N65M-2024-12-07T09:11:12Z"
        }
        
        # Initialize client
        client = APIClient(wml_credentials)
        
        # Try to get spaces (this will verify authentication)
        spaces = client.spaces.get_details()
        print("Connection successful!")
        print("Spaces:", spaces)
        
    except Exception as e:
        print("Connection failed:")
        print(str(e))

# Run test
test_ibm_connection()