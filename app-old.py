from flask import Flask, render_template, request, jsonify, url_for
import google.generativeai as genai
import os
from dotenv import load_dotenv
from markupsafe import escape
import markdown
import mimetypes

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

def allowed_file(filename):
    # Check if the file has one of the allowed extensions
    mime_type = mimetypes.guess_type(filename)[0]
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


@app.route("/", methods=["GET","POST"])
def index():
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=system_instruction,
        generation_config=genai.types.GenerationConfig(
            temperature=0.1,
        ),
    )

    gemini_response = ""
    uploaded_file_url = ""
    try:
        if request.method == "POST":
            file = request.files.get("file")
            if file:
                if allowed_file(file.filename):
                    if selectInvoiceType(request.form.get("invoice_type")):
                        prompt = selectInvoiceType(request.form.get("invoice_type"))
                        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
                        file.save(file_path)
                        file_to_upload = genai.upload_file(file_path)
                        response = model.generate_content([file_to_upload, "\n\n", prompt])
                        gemini_response = response.text
                        gemini_response = markdown.markdown(gemini_response)
                    else:
                        gemini_response = "Invalid invoice type. Please select a valid invoice type."
                else:
                    gemini_response = "File type not allowed. Please upload a file of type: " + ", ".join(ALLOWED_MIME_TYPES)
            else:
                response = model.generate_content(prompt)
                gemini_response = response.text
                gemini_response = markdown.markdown(gemini_response)
    except Exception as e:
        # Handle errors and set an appropriate error message
        gemini_response = f"An error occurred: {str(e)}"
    return render_template("index.html", gemini_response=gemini_response, uploaded_file_url=uploaded_file_url, ALLOWED_INVOICE_TYPES=ALLOWED_INVOICE_TYPES)
