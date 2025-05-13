### **Bank Statement Converter – Simplified Overview**  

This is a **lightweight web app** built with Flask. It helps you **convert bank statement PDFs** (or similar documents like invoices) into CSV files. The goal is to keep things **simple, private, and functional**.  

---

### **Features**
✅ Upload PDF files easily—**drag and drop** or select manually.  
✅ Extract key details (like **date, description, amount**) from bank statements or invoices.  
✅ Download the data as a **CSV file**.  
✅ **Privacy-first:** No files are stored permanently; they’re deleted right after processing.  
✅ Supports basic **bank statements and invoices**, with fallback parsing for tricky formats.  

---

### **Getting Started (Dev Mode)**
🛠 **Requirements:**  
- Python **3.8+**  
- `pip` (Python package manager)  

🔧 **Installation Steps:**  
1️⃣ Download or clone the project.  
2️⃣ Open the project folder:  
   ```sh
   cd bank-statement-converter
   ```  
3️⃣ Install required dependencies:  
   ```sh
   pip install flask PyPDF2 pandas
   ```  

---

### **Project Structure**
```sh
project/
├── templates/      # Frontend HTML template
│   └── index.html  
├── app.py         # Flask backend logic  
└── README.md      # Documentation  
```

---

### **Running the App**
🚀 Start the Flask server:  
```sh
python app.py
```  
🌐 Open **http://localhost:5000** in your browser.  
📂 **Upload a PDF**, and the app will convert it to CSV.  

---

### **How to Use**
1️⃣ **Upload**: Drag and drop a PDF or select it manually.  
2️⃣ **Processing**: The app extracts table data or invoice details.  
3️⃣ **Download**: The CSV file (`bank_statement.csv`) is automatically downloaded.  
4️⃣ **Privacy**: Files are processed **temporarily** and deleted immediately.  

---

### **Limitations**
⚠️ Uses **basic regex** for data extraction—some bank formats may not work perfectly.  
⚠️ Best for **simple bank statements** or invoices; complex PDFs might need **advanced tools** like `pdfplumber`.  
⚠️ Basic security—if used in production, **CSRF protection and file validation** are needed.  
⚠️ Not optimized for **large PDFs** or heavy traffic.  

---

### **Future Upgrades**
💡 Better support for **various bank statement formats** (e.g., `pdfplumber`, `tabula-py`).  
💡 Improved UI—**progress indicators and clearer error messages**.  
💡 **Stronger security** with file size limits and malware checks.  
💡 Support for **multi-page PDFs** and more complex tables.  

---

### **License**
**University of Yaoundé 1, Cameroon License**  

## By a student trying to make some money 