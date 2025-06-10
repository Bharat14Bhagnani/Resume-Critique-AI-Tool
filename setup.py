import subprocess
import sys
import os

def run(cmd):
    print(f"\n➡️ Running: {cmd}")
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"❌ Command failed: {cmd}")
        sys.exit(1)

def create_venv():
    if not os.path.exists('venv'):
        print("📦 Creating virtual environment...")
        run(f"{sys.executable} -m venv venv")
    else:
        print("✅ Virtual environment already exists.")

def install_dependencies():
    pip_path = os.path.join('venv', 'Scripts', 'pip.exe')
    print("📥 Installing required libraries...")
    run(f'"{pip_path}" install -r requirements.txt')

def download_spacy_model():
    python_path = os.path.join('venv', 'Scripts', 'python.exe')
    print("📥 Downloading spaCy English model...")
    run(f'"{python_path}" -m spacy download en_core_web_sm')

def main():
    create_venv()
    install_dependencies()
    download_spacy_model()
    print("\n✅ Setup complete!")
    print("\n👉 To run the app, type:")
    print("   venv\\Scripts\\python app.py")

if __name__ == "__main__":
    main()
