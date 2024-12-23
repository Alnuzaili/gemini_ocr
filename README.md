# Gemini OCR API

## Installation

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
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Step 3: Install Dependencies
Install the required dependencies from the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### Step 4: Configure the Environment
Set up the `.env` file:
```bash
cp .env.sample .env
```
Update the `.env` file with your `GEMINI_API_KEY`. You can generate an API key by visiting [this site](https://aistudio.google.com/app/apikey).

### Step 5: Run the Application
Start the application using Flask:
```bash
flask run
```

## Testing the API
You can verify that the API is working correctly by running the test script:
```bash
cd test
python3 test.py -f 03.txt -i "Al-Drsoni"
```

