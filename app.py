import base64
from flask import Flask, render_template, request, jsonify, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv
from markupsafe import escape
import json

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
load_dotenv()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])

system_instruction = "You are a highly accurate and adaptable data extraction expert specializing in arabic invoice images. Given an invoice image, meticulously extract and return all relevant data in JSON format. Ensure the output is comprehensive, error-free, and formatted correctly, regardless of the image's layout or format. Adapt to different styles and structures to provide the most accurate and complete data extraction. If the image quality is poor, apply image enhancement techniques to improve clarity."

ALLOWED_MIME_TYPES = {
    "application/pdf","text/plain", "text/html", "text/csv", "text/xml", "text/rtf",
    "image/jpeg", "image/png", "image/gif", "image/webp", "image/heic", "image/heif",
}

ALLOWED_INVOICE_TYPES = {
    "Al-Drsoni","Al-Othman","Al-Ifari","Almarai", "AlsafiDanone", "sadafco"
}

def allowed_file(mime_type):
    # Check if the MIME type is in the allowed list
    return mime_type in ALLOWED_MIME_TYPES

def selectInvoiceType(invoice_type):
    filename = f"prompts/{invoice_type}.txt"
    filepath = os.path.join(os.path.dirname(__file__), filename)  # Get absolute path
    if invoice_type in ALLOWED_INVOICE_TYPES:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:  # Explicitly specify UTF-8 encoding
                prompt = f.read().strip()  # Read and remove leading/trailing whitespace
                return prompt
        except FileNotFoundError:
            return f"Prompt file '{filename}' not found."
        except UnicodeDecodeError as e:
            return f"Encoding error while reading '{filename}': {str(e)}"

@app.route("/", methods=["GET", "POST"])
def index():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction,
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
        ),
    )

    gemini_response = ""
    parsed_json = ""
    try:
        if request.method == "POST":
            data = request.json  # Parse JSON payload
            base64_image = data.get("image")
            invoice_type = data.get("invoice_type")

            if not base64_image or not invoice_type:
                return jsonify({"error": "Missing 'base64_image' or 'invoice_type' parameter."}), 400

            if not selectInvoiceType(invoice_type):
                return jsonify({"error": "Invalid invoice type. Please select a valid invoice type."}), 400

            # Decode the base64 image and save it as a file
            try:
                image_data = base64.b64decode(base64_image)

                file_path = os.path.join(app.config["UPLOAD_FOLDER"], "uploaded_image.png")
                with open(file_path, "wb") as f:
                    f.write(image_data)
            except Exception as e:
                return jsonify({"error": f"Error decoding base64 image: {str(e)}"}), 400

            # Generate content using the model
            prompt = selectInvoiceType(invoice_type)
            file_to_upload = genai.upload_file(file_path)
            response = model.generate_content([file_to_upload, "\n\n", prompt])
            gemini_response = response.text
            if '```json' in gemini_response:
                # Extract JSON part after "```json" and strip newlines
                json_part = gemini_response.split('```json')[-1].strip('` \n')
                parsed_json = json.loads(json_part)
                print(json.dumps(parsed_json, indent=4, ensure_ascii=False))
            else:
                print("Unexpected response format:")
                print(gemini_response)

    except Exception as e:
        # Handle errors and set an appropriate error message
        gemini_response = f"An error occurred: {str(e)}"
    return parsed_json

if __name__ == "__main__":
    app.run(debug=True)
