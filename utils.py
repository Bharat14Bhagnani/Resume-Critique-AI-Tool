import os
import docx2txt
import language_tool_python
from PyPDF2 import PdfReader

# Initialize LanguageTool for English US
tool = language_tool_python.LanguageTool('en-US')

def extract_text(file_path):
    """
    Extract text from PDF, DOCX, or TXT file.
    """
    ext = os.path.splitext(file_path)[1].lower()
    text = ""
    if ext == '.pdf':
        with open(file_path, 'rb') as file:
            reader = PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
    elif ext == '.docx':
        text = docx2txt.process(file_path)
    elif ext == '.txt':
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
    else:
        raise ValueError("Unsupported file type. Please upload PDF, DOCX or TXT.")
    return text

def check_grammar(text):
    """
    Check grammar issues and return a list of messages with suggestions.
    """
    matches = tool.check(text)
    return [f"{match.message} (Suggestion: {', '.join(match.replacements)})" for match in matches][:10]

def structure_feedback(text):
    """
    Basic feedback on structure based on simple heuristics.
    (You can improve this later.)
    """
    feedback = []
    lines = text.splitlines()
    if len(lines) < 20:
        feedback.append("Resume looks short; consider adding more details.")
    if "Objective" not in text and "Summary" not in text:
        feedback.append("Consider adding a clear Objective or Summary section.")
    if "Experience" not in text:
        feedback.append("Add an Experience section to showcase your work history.")
    if "Skills" not in text:
        feedback.append("Add a Skills section to highlight your key competencies.")
    return feedback
