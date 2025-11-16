# 🔄 System Flow - How It Works

## Complete Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                    USER ENTERS QUERY/PROMPT                       │
│              "How to fix a damaged STOP sign?"                   │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│              STEP 1: RAG - SEMANTIC SEARCH                       │
│                                                                   │
│  1. User query is converted to embedding vector                  │
│  2. Semantic search performed on interventions.json              │
│  3. Finds top-k most relevant interventions using                │
│     cosine similarity (vector matching)                           │
│  4. Retrieves: Name, Description, Code, Clause,                  │
│     Category, Problem, etc.                                       │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         STEP 2: ENHANCED QUERY BUILDING (RAG Context)            │
│                                                                   │
│  Retrieved interventions are formatted as context:               │
│  - Intervention 1: STOP Sign, Category: Road Sign,               │
│    Problem: Damaged, Code: IRC:67-2022, Clause: 14.4, etc.      │
│  - Intervention 2: ...                                           │
│  - Intervention 3: ...                                           │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         STEP 3: OLLAMA LOCAL MODEL PROCESSING                   │
│                                                                   │
│  Enhanced prompt sent to Ollama (llama3.2:3b):                  │
│  "You are an expert road safety consultant.                      │
│   User Query: [original query]                                  │
│   Based on these interventions: [RAG context]                   │
│   Provide detailed recommendation..."                            │
│                                                                   │
│  Ollama generates AI-powered response using:                     │
│  - User's original query                                         │
│  - Retrieved intervention details (RAG context)                 │
│  - Its knowledge of road safety                                  │
└────────────────────────────┬────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│         STEP 4: STREAMLIT WEB APP DISPLAY                        │
│                                                                   │
│  Displays on web interface:                                       │
│  1. AI-Powered Recommendation (from Ollama)                     │
│  2. Retrieved Interventions (from RAG search)                    │
│  3. Similarity Scores                                            │
│  4. Technical Details (Code, Clause, etc.)                       │
└─────────────────────────────────────────────────────────────────┘
```

## Detailed Step-by-Step

### Step 1: User Query Input
- User types query in highlighted text area
- Example: "How to fix a damaged STOP sign?"

### Step 2: RAG Implementation (Semantic Search)
**File: `embedding_pipeline.py`**
- Query → Embedding vector (using Sentence Transformers)
- Compare with all intervention embeddings in `interventions.json`
- Calculate cosine similarity scores
- Retrieve top-k most relevant interventions (default: 3)
- Returns: List of interventions with similarity scores

**What happens:**
```python
# User query: "damaged stop sign"
# System searches interventions.json semantically
# Finds: STOP Sign (score: 0.85), Speed Hump (score: 0.23), etc.
# Returns top 3 most relevant
```

### Step 3: Enhanced Query Building
**File: `ollama_integration.py`**
- Takes retrieved interventions from Step 2
- Formats them as context with all details:
  - Name/Type
  - Category
  - Problem
  - Description/Data
  - Code (IRC:67-2022)
  - Clause (14.4)
  - Similarity score
- Combines with user's original query
- Creates comprehensive prompt for Ollama

**Enhanced Query Structure:**
```
Original Query: "How to fix a damaged STOP sign?"

Retrieved Context:
1. STOP Sign
   - Category: Road Sign
   - Problem: Damaged
   - Description: [full description]
   - Code: IRC:67-2022
   - Clause: 14.4
   - Similarity: 0.85

2. [Other relevant interventions...]
```

### Step 4: Ollama Local Model Processing
**File: `ollama_integration.py`**
- Sends enhanced prompt to Ollama (local model: llama3.2:3b)
- Ollama processes using:
  - User's query intent
  - Retrieved intervention details (RAG context)
  - Its training knowledge
- Generates comprehensive recommendation
- Returns detailed, actionable response

**Ollama receives:**
```
"You are an expert road safety consultant.
User Query: 'How to fix a damaged STOP sign?'
Based on these interventions:
1. STOP Sign - Code: IRC:67-2022, Clause: 14.4...
[Provide detailed recommendation...]"
```

### Step 5: Streamlit Web App Display
**File: `web_interface.py`**
- Displays AI recommendation in highlighted box
- Shows retrieved interventions with details
- Shows similarity scores
- Shows technical information (Code, Clause, etc.)

## Key Components

### 1. **RAG (Retrieval-Augmented Generation)**
- **Retrieval**: Semantic search on `interventions.json`
- **Augmentation**: Enhances query with retrieved context
- **Generation**: Ollama generates response using augmented context

### 2. **Semantic Search**
- Uses Sentence Transformers (`all-MiniLM-L6-v2`)
- Converts text to vectors (embeddings)
- Finds similar meaning, not just keywords
- Example: "damaged sign" matches "STOP Sign" with "Damaged" problem

### 3. **Ollama Local Model**
- Runs locally on your machine
- Model: `llama3.2:3b` (default)
- Processes enhanced query with RAG context
- Generates detailed recommendations

### 4. **Streamlit Web Interface**
- User-friendly web app
- Highlights query input
- Displays results clearly
- Shows both AI response and source interventions

## Data Flow Summary

```
User Query
    ↓
[Semantic Search] → interventions.json → Top-k Interventions
    ↓
[Build Context] → Enhanced Query with RAG Context
    ↓
[Ollama LLM] → AI Recommendation
    ↓
[Streamlit UI] → Display Results
```

## Why This Works Better

1. **RAG**: Combines your specific data (interventions.json) with AI knowledge
2. **Semantic Search**: Finds relevant interventions even with different wording
3. **Local Ollama**: Privacy, no API costs, fast responses
4. **Enhanced Context**: Ollama gets both query and relevant data, not just query

## Example Flow

**User Input:**
```
"How to fix a damaged STOP sign?"
```

**RAG Search Finds:**
```
1. STOP Sign (Damaged) - IRC:67-2022, Clause 14.4 - Score: 0.85
2. Road Sign Maintenance - Score: 0.42
3. Sign Installation - Score: 0.38
```

**Ollama Receives:**
```
User Query: "How to fix a damaged STOP sign?"
Context: [Full details of STOP Sign intervention with code, clause, dimensions, etc.]
```

**Ollama Generates:**
```
Based on IRC:67-2022, Clause 14.4, for a damaged STOP sign:
1. Recommended Solution: Replace the STOP sign following IRC standards...
2. Why This Solution: The STOP sign must meet specific dimensions...
3. Implementation Details: 
   - For speeds up to 50 km/h: 750 mm height, 25 mm border...
   - Place 1.5 m in advance of stop line...
[Detailed recommendation continues...]
```

**Streamlit Displays:**
- AI Recommendation (highlighted box)
- Retrieved Interventions (with expandable details)
- Similarity Scores
- Technical Information

---

**Yes, your understanding is 100% correct!** ✅

The system implements RAG by:
1. Semantic search on interventions.json (Retrieval)
2. Building enhanced query with context (Augmentation)  
3. Sending to Ollama local model (Generation)
4. Displaying on Streamlit web app

