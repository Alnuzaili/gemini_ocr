# Gemini OCR API

## Overview

The Gemini OCR API is designed to extract structured data from Arabic invoice images using advanced AI-powered OCR capabilities. It is highly accurate and adaptable, supporting various invoice layouts and formats. The API processes invoices in either base64-encoded format or via a direct image URL and returns the extracted data in a JSON format.

### Key Features:
- Supports a wide range of invoice formats, including **Al-Drsoni, Al-Othman, Al-Ifari, Almarai, AlsafiDanone, and sadafco**.
- Processes images sent as **base64-encoded data** or via **URL**.
- Leverages Google's **Gemini AI model** for precise and adaptable data extraction.
- Returns structured JSON data for seamless integration with other systems.

---

## Installation

Follow the steps below to set up the API on your local machine:

### Step 1: Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/Alnuzaili/gemini_ocr.git
cd gemini_ocr
```

### Step 2: Set Up a Virtual Environment (Optional but Recommended)
Create and activate a virtual environment to manage dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
Install the required dependencies listed in the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 4: Configure the Environment
1. Copy the sample `.env` file:
   ```bash
   cp .env.sample .env
   ```
2. Update the `.env` file with your **Gemini API Key**:
   - Obtain your API key by visiting [Google AI Studio](https://aistudio.google.com/app/apikey).
   - Set the `GEMINI_API_KEY` in the `.env` file.

### Step 5: Run the Application
Start the Flask application:
```bash
flask run
```

The API will now be available at `http://127.0.0.1:5000/`.

---

## How to Use the API

The API supports two methods for sending invoice images: **base64 encoding** and **image URLs**. Here's how to use it:

### Request Format

#### Endpoint:
`POST /`

#### Parameters:
- `image`: (optional) Base64-encoded image string.
- `image_url`: (optional) Direct URL to the invoice image.
- `invoice_type`: (required) The type of invoice. Must be one of:
  - `Al-Drsoni`
  - `Al-Othman`
  - `Al-Ifari`
  - `Almarai`
  - `AlsafiDanone`
  - `sadafco`

**Note**: You must provide either `image` or `image_url`, but not both. If both are provided, the API will return an error.

#### Example JSON Payload:
```json
{
  "image": "base64_encoded_image_string",
  "invoice_type": "Al-Drsoni"
}
```
Or:
```json
{
  "image_url": "https://example.com/invoice.jpg",
  "invoice_type": "Almarai"
}
```

---

### Example Response:
```json
{
    "invoice_number": "62255",
    "invoice_date": "30/05/2024",
    "currency": "SAR",
    "payment_terms": null,
    "supplier_name": "AL-OTHMAN AGRI. PROD. & PROC. COAST",
    "supplier_address": "PO. Box 402-Al-Khobar - P. Code 31952-Saudi Arabia",
    "supplier_vat": "300429164700003",
    "customer_name": "AAL AL KAIF",
    "customer_address": "PRINCE MESHAAL IBN ABD AL AZIZ\nIRQAH\nRIYADH",
    "customer_vat": "182550038",
    "line_items": [
        {
            "id": "178",
            "item_description_arabic": "حليب كامل الدسم 1.75 لتر",
            "item_description_english": "MILK FC 1.75 LTR",
            "quantity": 10,
            "uom": null,
            "unit_price": 7.86,
            "total_price": 15.72,
            "tax_percentage_per_item": 15,
            "total_price_with_tax": 18.078
        },
        {
            "id": "753",
            "item_description_arabic": "حليب بروتين 320 مل",
            "item_description_english": "PROTIN MILK PLN 320ML",
            "quantity": 35,
            "uom": null,
            "unit_price": 5.24,
            "total_price": 52.4,
            "tax_percentage_per_item": 15,
            "total_price_with_tax": 60.26
        },
    ],
    "subtotal": null,
    "tax": null,
    "total_amount_due": null
}
```

---

## Testing the API

You can test the API using the provided `test.py` script.

### Step 1: Navigate to the Test Directory
```bash
cd test
```

### Step 2: Run the Script
#### Option 1: Using a Base64 Image
```bash
python3 test.py -f 03.txt -i "Al-Drsoni"
```

#### Option 2: Using an Image URL
```bash
python3 test.py -l "https://example.com/invoice.jpg" -i "Al-Drsoni"
```

### Parameters:
- `-f`: Path to a text file containing the base64-encoded image.
- `-l`: Direct URL to the invoice image.
- `-i`: Invoice type.

### Example Output:
The script will print the structured JSON response returned by the API.

---

## Notes
- Ensure the `.env` file is properly configured with a valid Gemini API Key.
- Only supported invoice types should be passed; otherwise, the API will return an error.
- For large images, consider optimizing or compressing them before sending.

---

Feel free to contribute or report issues at [GitHub Repository](https://github.com/Alnuzaili/gemini_ocr).