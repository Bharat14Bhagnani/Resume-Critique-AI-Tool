import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from fpdf import FPDF
import unicodedata
import re
from docx import Document
import pdfplumber
import language_tool_python

# Create necessary folders if not present
os.makedirs("uploads", exist_ok=True)
os.makedirs("improved_resumes", exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["IMPROVED_FOLDER"] = "improved_resumes"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # Max 5 MB files

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".txt"}

def allowed_file(filename):
    return os.path.splitext(filename)[1].lower() in ALLOWED_EXTENSIONS

# Extract text based on file type
def extract_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == ".txt":
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".docx":
        doc = Document(filepath)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        return "\n".join(full_text)
    elif ext == ".pdf":
        with pdfplumber.open(filepath) as pdf:
            pages = [page.extract_text() or '' for page in pdf.pages]
        return "\n".join(pages)
    else:
        return ""

# Grammar checker using language_tool_python
tool = language_tool_python.LanguageTool('en-US')

def check_grammar(text):
    matches = tool.check(text)
    issues = []
    for match in matches:
        # Show the sentence with issue and message
        context = text[match.offset : match.offset + match.errorLength]
        issues.append(f"{match.message} → '{context}'")
    return issues or ["No grammar issues found."]

# Simple structure feedback example
def structure_feedback(text):
    feedback = []
    lines = text.splitlines()
    # Example: check if resume is too short
    if len(lines) < 20:
        feedback.append("Resume seems too short, consider adding more details.")
    # Example: check for presence of 'Experience' section
    if not any("experience" in line.lower() for line in lines):
        feedback.append("Add an 'Experience' section to improve your resume.")
    return feedback or ["No structure issues found."]

# PDF generator for combined feedback
def generate_pdf(text, filepath):
    clean_text = (
        unicodedata.normalize("NFKD", text)
        .encode("latin-1", "ignore")
        .decode("latin-1")
    )
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    lines = clean_text.split("\n")
    for line in lines:
        pdf.multi_cell(0, 10, line)
    pdf.output(filepath)

# Highlight issues for HTML preview
def highlight_feedback(text):
    # Highlight all issue sentences inside <span>
    # Simple example: highlight anything after '→'
    pattern = r"(→ '.*?')"
    return re.sub(pattern, r'<span class="highlight">\1</span>', text).replace("\n", "<br>")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        uploaded_file = request.files.get("resume")
        if uploaded_file and allowed_file(uploaded_file.filename):
            filename = secure_filename(uploaded_file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            uploaded_file.save(filepath)

            try:
                resume_text = extract_text(filepath)
            except Exception as e:
                return f"Error reading file: {str(e)}"

            grammar_issues = check_grammar(resume_text)
            structure_tips = structure_feedback(resume_text)

            combined_feedback = "=== Structure Suggestions ===\n"
            combined_feedback += "\n".join(structure_tips) + "\n\n"
            combined_feedback += "=== Grammar Suggestions ===\n"
            combined_feedback += "\n".join(grammar_issues)

            highlighted_feedback = highlight_feedback(combined_feedback)

            improved_filename = f"improved_{os.path.splitext(filename)[0]}.pdf"
            improved_pdf_path = os.path.join(app.config["IMPROVED_FOLDER"], improved_filename)
            generate_pdf(combined_feedback, improved_pdf_path)

            return render_template(
                "index.html",
                filename=improved_filename,
                grammar_issues=grammar_issues,
                structure_feedback=structure_tips,
                resume_preview=highlighted_feedback
            )

        return "Invalid file format. Please upload a PDF, DOCX, or TXT file."
    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(app.config["IMPROVED_FOLDER"], filename, as_attachment=True)

if __name__ == "__main__":
    print("🚀 Running Flask app...")
    app.run(debug=False, use_reloader=False)

