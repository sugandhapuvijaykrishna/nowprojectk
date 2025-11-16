"""Verify that the setup is correct"""
import json
import os
import sys

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

print("=" * 60)
print("Verifying Road Safety RAG Setup")
print("=" * 60)

# Check interventions.json
interventions_file = "interventions.json"
if os.path.exists(interventions_file):
    try:
        with open(interventions_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"[OK] interventions.json found: {len(data)} interventions")
        if data:
            print(f"   Sample keys: {list(data[0].keys())[:5]}")
    except Exception as e:
        print(f"[ERROR] Error reading interventions.json: {e}")
else:
    print(f"[WARNING] interventions.json not found")

# Check Python modules
modules = ['streamlit', 'sentence_transformers', 'numpy', 'ollama']
print("\nChecking Python modules:")
for module in modules:
    try:
        __import__(module)
        print(f"[OK] {module} installed")
    except ImportError:
        print(f"[ERROR] {module} NOT installed - run: pip install {module}")

# Check Ollama
print("\nChecking Ollama:")
try:
    import subprocess
    result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=5)
    if result.returncode == 0:
        print(f"[OK] Ollama installed: {result.stdout.strip()}")
    else:
        print("[WARNING] Ollama command failed")
except FileNotFoundError:
    print("[ERROR] Ollama not found in PATH - install from https://ollama.ai")
except Exception as e:
    print(f"[WARNING] Could not check Ollama: {e}")

print("\n" + "=" * 60)
print("Setup verification complete!")
print("=" * 60)

