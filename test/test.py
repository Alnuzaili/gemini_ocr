import argparse
import requests
import json
import os

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Send base64 image and invoice type to API.")
    parser.add_argument("-f", "--file", required=True, help="Path to the text file containing the base64-encoded image.")
    parser.add_argument("-i", "--invoice_type", required=True, help="Invoice type string.")
    parser.add_argument("-u", "--url", help="API endpoint URL.", default="http://localhost:5000/")
    args = parser.parse_args()

    # Read base64 image from the file
    if not os.path.exists(args.file):
        print(f"Error: File '{args.file}' not found.")
        return

    try:
        with open(args.file, "r") as f:
            base64_image = f.read().strip()  # Remove any leading/trailing whitespace
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Prepare the payload
    payload = {
        "image": base64_image,
        "invoice_type": args.invoice_type
    }

    # Send POST request to the API
    try:
        response = requests.post(args.url, json=payload)
        if response.status_code == 200:
            print(response.json())
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"Error sending request: {e}")

if __name__ == "__main__":
    main()
