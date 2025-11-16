# Troubleshooting Guide

## ✅ Streamlit Dashboard Integration Complete

The Streamlit dashboard has been fully integrated with your RAG system and Ollama. Here's how to use it:

## 🚀 Starting the Dashboard

### Method 1: Using the start script (Recommended)
```bash
cd road-safety-rag
python start_app.py
```

### Method 2: Direct Streamlit command
```bash
cd road-safety-rag
streamlit run web_interface.py
```

### Method 3: Using the batch file (Windows)
```bash
cd road-safety-rag
run_app.bat
```

## 🌐 Access URL

Once started, the dashboard will be available at:
- **Local URL:** `http://localhost:8501`
- **Network URL:** `http://192.168.x.x:8501` (shown in terminal)

## 🔧 Common Issues and Solutions

### Issue 1: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
# Or install all dependencies:
pip install -r requirements_complete.txt
```

### Issue 2: "Ollama is not installed or not in PATH"
**Solution:**
1. Install Ollama from https://ollama.ai
2. Restart your terminal/command prompt
3. Verify installation: `ollama --version`
4. Pull a model: `ollama pull llama3.2:3b`

### Issue 3: "No interventions loaded"
**Solution:**
- The app auto-loads `interventions.json` from the same directory
- If it doesn't load automatically:
  1. Check that `interventions.json` exists in `road-safety-rag/` folder
  2. Use the sidebar to upload the JSON file manually
  3. Check the terminal for error messages

### Issue 4: "Error generating recommendations"
**Possible causes:**
- Ollama service not running
- Model not pulled (run `ollama pull llama3.2:3b`)
- Network/firewall blocking Ollama

**Solution:**
```bash
# Check if Ollama is running
ollama list

# If not, start it (usually auto-starts)
ollama serve

# Pull the model if needed
ollama pull llama3.2:3b
```

### Issue 5: Dashboard opens but shows blank/errors
**Solution:**
1. Check browser console (F12) for JavaScript errors
2. Check terminal for Python errors
3. Clear browser cache and refresh
4. Try a different browser

### Issue 6: Embeddings not loading
**Solution:**
- Delete `road_safety_index.pkl` if it exists
- Restart the app - it will regenerate embeddings
- Check that `interventions.json` is valid JSON

## 📊 Features Available

✅ **Query System Tab:**
- Enter road safety problems
- Filter by road type and problem type
- Get AI-powered recommendations from Ollama
- View retrieved interventions with similarity scores

✅ **Database Info Tab:**
- View all 50 interventions
- Search and filter interventions
- See statistics (category, problem, code distribution)

✅ **About Tab:**
- Application information
- How it works
- Technology stack

## 🧪 Testing the Integration

1. **Test RAG Search:**
   - Go to Query System tab
   - Enter: "damaged stop sign"
   - Click "Get Recommendations"
   - Should show relevant interventions

2. **Test Ollama Integration:**
   - After getting search results
   - Check the "AI-Powered Recommendation" section
   - Should show detailed recommendations from Ollama

3. **Test Database:**
   - Go to Database Info tab
   - Should show 50 interventions
   - Try searching for "speed hump" or "road marking"

## 📝 Data Structure

Your JSON data is automatically handled with fields:
- `S. No.` - Serial number
- `problem` - Problem type
- `category` - Category (Road Sign, Road Marking, etc.)
- `type` - Specific type
- `data` - Description
- `code` - IRC code
- `clause` - Clause reference
- `content` - Full content

## 🔍 Example Queries

Try these to test the system:
- "How to fix a damaged STOP sign?"
- "What are speed hump requirements?"
- "Missing road markings"
- "Height issue with signs"
- "Non-retroreflective markings"

## 📞 Still Having Issues?

1. Check all dependencies are installed:
   ```bash
   pip install -r requirements_complete.txt
   ```

2. Verify Python version (3.8+):
   ```bash
   python --version
   ```

3. Check file permissions - ensure you can read `interventions.json`

4. Review terminal output for specific error messages

5. Try running in a clean environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   pip install -r requirements_complete.txt
   streamlit run web_interface.py
   ```

