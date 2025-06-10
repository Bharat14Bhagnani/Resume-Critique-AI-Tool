# Add Java JDK 21 to the PATH for this session
$env:Path = "C:\Program Files\Java\jdk-21\bin;" + $env:Path

# Activate the Python virtual environment (adjust 'venv' if your folder is named differently)
. .\venv\Scripts\Activate.ps1

# Start the Flask app
python app.py
