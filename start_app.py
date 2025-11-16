#!/usr/bin/env python
"""
Simple script to start the Streamlit app with error handling
"""
import subprocess
import sys
import os

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    print("=" * 60)
    print("Starting Road Safety Intervention GPT Dashboard")
    print("=" * 60)
    print(f"Working directory: {script_dir}")
    print()
    
    # Check if interventions.json exists
    interventions_file = os.path.join(script_dir, "interventions.json")
    if os.path.exists(interventions_file):
        print(f"✅ Found interventions.json")
    else:
        print(f"⚠️  interventions.json not found in {script_dir}")
    
    print()
    print("Starting Streamlit...")
    print("The app will open in your browser automatically.")
    print("If it doesn't, navigate to: http://localhost:8501")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "web_interface.py"], check=True)
    except KeyboardInterrupt:
        print("\n\nShutting down...")
    except Exception as e:
        print(f"\n❌ Error starting Streamlit: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure Streamlit is installed: pip install streamlit")
        print("2. Check that all dependencies are installed: pip install -r requirements_complete.txt")
        sys.exit(1)

if __name__ == "__main__":
    main()

