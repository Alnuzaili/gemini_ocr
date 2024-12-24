import argparse
import requests
import json
import os

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Send image (base64 or URL) and invoice type to API.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-f", "--file", help="Path to the text file containing the base64-encoded image.")
    group.add_argument("-l", "--url", help="Image URL.")
    parser.add_argument("-i", "--invoice_type", required=True, help="Invoice type string.")
    parser.add_argument("-u", "--api_url", help="API endpoint URL.", default="http://localhost:5000/")
    args = parser.parse_args()

    # Prepare the payload
    payload = {"invoice_type": args.invoice_type}

    if args.file:
        # Read base64 image from the file
        if not os.path.exists(args.file):
            print(f"Error: File '{args.file}' not found.")
            return
        try:
            with open(args.file, "r") as f:
                base64_image = f.read().strip()  # Remove any leading/trailing whitespace
            payload["image"] = base64_image
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    elif args.url:
        # Use the provided image URL
        payload["image_url"] = args.url

    # Send POST request to the API
    try:
        response = requests.post(args.api_url, json=payload)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        else:
            print(f"Error: Received status code {response.status_code}")
            print("Response:", response.text)
    except Exception as e:
        print(f"Error sending request: {e}")

if __name__ == "__main__":
    main()
