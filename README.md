# Road Safety Intervention GPT

A Streamlit-based web application that uses Retrieval-Augmented Generation (RAG) with Ollama to provide AI-powered recommendations for road safety interventions.

## Features

- 🔍 **Semantic Search**: Find relevant road safety interventions using vector embeddings
- 🤖 **AI Recommendations**: Get contextual recommendations powered by Ollama LLM
- 📊 **Interactive Interface**: User-friendly Streamlit web interface
- 📚 **Database Management**: Upload and manage road safety intervention data
- 🎯 **Smart Filtering**: Filter by road type, problem type, and more

## Requirements

### Prerequisites

1. **Python 3.8+**
2. **Ollama** - Download and install from [https://ollama.ai](https://ollama.ai)
3. **Ollama Model** - Pull a model (default: `llama3.2:3b`)
   ```bash
   ollama pull llama3.2:3b
   ```

### Python Dependencies

Install all required packages:

```bash
pip install -r requirements_complete.txt
```

Or install individually:

```bash
pip install streamlit ollama sentence-transformers numpy pandas faiss-cpu torch transformers scikit-learn
```

## Installation

1. Clone or navigate to the project directory:
   ```bash
   cd road-safety-rag
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements_complete.txt
   ```

3. Ensure Ollama is running:
   ```bash
   ollama serve
   ```

4. Pull the required model (if not already done):
   ```bash
   ollama pull llama3.2:3b
   ```

## Usage

### Starting the Application

Run the Streamlit app:

```bash
streamlit run web_interface.py
```

The application will open in your default web browser at `http://localhost:8501`

### Using the Application

1. **Load Data**: 
   - The app will auto-load `interventions.json` if it exists
   - Or upload a JSON file via the sidebar

2. **Query System**:
   - Enter your road safety problem in the query box
   - Optionally select road type and problem types
   - Click "Get Recommendations"
   - View retrieved interventions and AI-powered recommendations

3. **Database Info**:
   - View all interventions in the database
   - Search and filter interventions
   - See statistics about the database

### JSON Data Format

Your interventions JSON should follow this format:

```json
[
  {
    "intervention_id": "RSI-001",
    "name": "Speed Humps",
    "description": "Vertical deflection devices that physically slow vehicles by creating discomfort at higher speeds.",
    "problem_type": ["speeding", "residential safety", "pedestrian safety"],
    "road_type": ["local streets", "school zones", "residential areas"],
    "effectiveness": "High",
    "cost": "Low to Medium",
    "implementation_time": "1-2 weeks",
    "references": ["WHO Guidelines"]
  }
]
```

## Project Structure

```
road-safety-rag/
├── web_interface.py          # Streamlit web interface
├── ollama_integration.py      # RAG system with Ollama integration
├── embedding_pipeline.py      # Vector embedding and search pipeline
├── interventions.json         # Sample intervention data
├── requirements_complete.txt  # All Python dependencies
├── requirements.txt          # Core dependencies
├── main.py                   # CLI testing script
└── app.py                    # Alternative entry point
```

## How It Works

1. **Embedding Pipeline**: 
   - Uses sentence transformers to create vector embeddings of interventions
   - Stores embeddings in a pickle file for fast retrieval

2. **Semantic Search**:
   - Converts user query to embedding
   - Finds most similar interventions using cosine similarity
   - Returns top-k most relevant interventions

3. **Ollama Integration**:
   - Takes retrieved interventions as context
   - Generates comprehensive recommendations using Ollama LLM
   - Provides actionable insights based on the context

## Configuration

### Changing Ollama Model

You can change the Ollama model in two ways:

1. **Environment Variable**:
   ```bash
   export OLLAMA_MODEL=mistral
   ```

2. **In the App**: Use the sidebar settings to change the model

### Adjusting Retrieval Count

Use the slider in the sidebar to adjust how many interventions to retrieve (1-10).

## Troubleshooting

### Ollama Not Found

- Ensure Ollama is installed and in your PATH
- Try running `ollama --version` to verify installation
- On Windows, you may need to restart your terminal after installation

### Model Not Found

- Pull the model: `ollama pull llama3.2:3b`
- Or use a different model that you have installed

### No Interventions Found

- Upload intervention data via the sidebar
- Ensure `interventions.json` exists in the project directory
- Check that the JSON format is correct

### Slow Performance

- Use a smaller model (e.g., `llama3.2:1b` instead of `llama3.2:3b`)
- Reduce the number of interventions retrieved
- Ensure you have sufficient RAM

## Example Queries

- "How to reduce speeding on residential streets near a school?"
- "What are cost-effective solutions for pedestrian safety?"
- "How to prevent intersection crashes on busy roads?"
- "Solutions for run-off-road accidents on highways"

## License

This project is provided as-is for educational and research purposes.

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

