# Resume-Critique-AI-Tool
This web-based tool analyzes your resume for grammar issues and structure improvements using Python and simple AI logic. Upload your resume in PDF, DOCX, or TXT format, get instant feedback, and download improvements as a PDF.

# Project Structure
Resume-AI-Critique-Tool/

│
├── app.py

├── utils.py

├── requirements.txt

├── setup.py

├── start_resume_tool.ps1

├── templates/

│   └── index.html

├── uploads/               # stores uploaded resumes (auto-created)

└── improved_resumes/      # stores improved resumes as PDFs (auto-created)

The folders uploads/ and improved_resumes/ are created automatically when the app runs. If needed, you can also create them manually in the project root.

# Recommended Software

Python 3.10+

Java (for DOCX/PDF extraction)

Visual Studio Code (recommended for running PowerShell)

Google Chrome / Edge or any modern browser


# How to Run the Project

Clone this repository.

Open the project folder in Visual Studio Code.

Open the integrated terminal (make sure it's set to PowerShell).

Run:.\start_resume_tool.ps1

Open your browser and go to:
http://127.0.0.1:5000


# What You Can Do

Upload resumes in .pdf, .docx, or .txt

View real-time feedback and suggestions

Highlight grammar and structure issues

Download the improvements needed in resume as a clean PDF
