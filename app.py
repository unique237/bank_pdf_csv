from flask import Flask, request, send_file, render_template
import os
import tempfile
import pandas as pd
from PyPDF2 import PdfReader
import re
from io import StringIO, BytesIO
import datetime

app = Flask(__name__)

# Configure temporary directory for file processing
TEMP_DIR = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(text):
    """Clean extracted text from PDF"""
    # Remove excessive whitespace and newlines
    text = re.sub(r'\s+', ' ', text.strip())
    return text

def parse_bank_statement(pdf_path):
    """Parse PDF bank statement and extract tabular data"""
    try:
        # Open PDF in binary mode
        with open(pdf_path, 'rb') as file:
            reader = PdfReader(file)
            text = ""
            for page in reader.pages:
                extracted_text = page.extract_text()
                if extracted_text:
                    text += extracted_text + "\n"
            
            # Clean the extracted text
            text = clean_text(text)
            
            # Simple regex pattern to match common bank statement formats
            # Example: MM/DD/YYYY Description Amount
            pattern = r'(\d{2}/\d{2}/\d{4})\s+([^\d]+?)\s+(-?\d+\.\d{2})'
            matches = re.findall(pattern, text)
            
            # Create DataFrame from matches
            data = []
            for match in matches:
                date, description, amount = match
                data.append({
                    'Date': date,
                    'Description': description.strip(),
                    'Amount': float(amount)
                })
            
            # If no matches found, return basic data from invoice
            if not data:
                # Extract basic invoice data as fallback
                invoice_pattern = r'INVOICE #\s*T(\d+).*?DATE\s*(\d{2}/\d{2}/\d{4}).*?TOTAL AMOUNT\s*\$(\d+\.\d{2})'
                invoice_match = re.search(invoice_pattern, text, re.DOTALL)
                if invoice_match:
                    invoice_num, date, amount = invoice_match.groups()
                    data.append({
                        'Date': date,
                        'Description': f"Invoice {invoice_num}",
                        'Amount': float(amount)
                    })
            
            if not data:
                raise Exception("No tabular data found in PDF")
            
            df = pd.DataFrame(data)
            return df
    
    except Exception as e:
        raise Exception(f"Error parsing PDF: {str(e)}")

def generate_csv(df):
    """Generate CSV file from DataFrame"""
    output = StringIO()
    df.to_csv(output, index=False)
    output.seek(0)
    return output

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return {'error': 'No file uploaded'}, 400
        
        file = request.files['file']
        
        if file.filename == '':
            return {'error': 'No file selected'}, 400
        
        if file and allowed_file(file.filename):
            # Create temporary file
            temp_file = os.path.join(TEMP_DIR, f"temp_{datetime.datetime.now().timestamp()}.pdf")
            
            try:
                # Save uploaded file temporarily
                file.save(temp_file)
                
                # Parse PDF and generate DataFrame
                df = parse_bank_statement(temp_file)
                
                # Generate CSV
                csv_output = generate_csv(df)
                
                # Clean up temporary file
                os.remove(temp_file)
                
                # Return CSV file
                return send_file(
                    csv_output,
                    mimetype='text/csv',
                    as_attachment=True,
                    download_name='bank_statement.csv'
                )
                
            except Exception as e:
                # Clean up in case of error
                if os.path.exists(temp_file):
                    os.remove(temp_file)
                return {'error': str(e)}, 500
                
        return {'error': 'Invalid file type'}, 400
    
    except Exception as e:
        return {'error': f'Server error: {str(e)}'}, 500

if __name__ == '__main__':
    app.run(debug=True)