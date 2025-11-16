# 📋 Complete Web Interface Documentation

## Table of Contents
1. [Page Configuration](#page-configuration)
2. [CSS Styling & DOM Structure](#css-styling--dom-structure)
3. [Component Structure](#component-structure)
4. [Layout Hierarchy](#layout-hierarchy)
5. [Functionality Details](#functionality-details)
6. [DOM Elements Reference](#dom-elements-reference)

---

## Page Configuration

### Streamlit Page Config
```python
st.set_page_config(
    page_title="Road Safety Intervention GPT", 
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)
```

**Properties:**
- **page_title**: "Road Safety Intervention GPT" (browser tab title)
- **page_icon**: 🛣️ (emoji icon)
- **layout**: "wide" (full-width layout)
- **initial_sidebar_state**: "expanded" (sidebar open by default)

---

## CSS Styling & DOM Structure

### 1. Main Header Styling
```css
.main-header {
    font-size: 3rem;
    font-weight: bold;
    background: linear-gradient(90deg, #1f77b4, #ff7f0e);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.5rem;
    padding: 1rem;
}
```

**DOM Element:**
```html
<h1 class="main-header">🛣️ Road Safety Intervention GPT</h1>
```

**Visual Properties:**
- Gradient text (blue to orange)
- 3rem font size
- Centered alignment
- 1rem padding

---

### 2. Query Input Text Area Styling
```css
.stTextArea > div > div > textarea {
    border: 3px solid #1f77b4 !important;
    border-radius: 10px !important;
    padding: 1rem !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 6px rgba(31, 119, 180, 0.2) !important;
    transition: all 0.3s ease !important;
}

.stTextArea > div > div > textarea:focus {
    border-color: #ff7f0e !important;
    box-shadow: 0 6px 12px rgba(31, 119, 180, 0.4) !important;
    outline: none !important;
}
```

**DOM Structure:**
```html
<div class="stTextArea">
    <div>
        <div>
            <textarea 
                placeholder="Example: How to fix a damaged STOP sign?..."
                height="120"
                key="query_input"
            ></textarea>
        </div>
    </div>
</div>
```

**Properties:**
- **Border**: 3px solid blue (#1f77b4)
- **Border Radius**: 10px
- **Padding**: 1rem
- **Font Size**: 1.1rem
- **Box Shadow**: Blue shadow with 0.2 opacity
- **Focus State**: Orange border (#ff7f0e) with enhanced shadow
- **Height**: 120px

---

### 3. Primary Button Styling
```css
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #1f77b4, #ff7f0e) !important;
    color: white !important;
    font-size: 1.2rem !important;
    font-weight: bold !important;
    padding: 0.75rem 2rem !important;
    border-radius: 10px !important;
    border: none !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 12px rgba(0,0,0,0.3) !important;
}
```

**DOM Element:**
```html
<div class="stButton">
    <button type="button">
        🚀 Get AI Recommendations
    </button>
</div>
```

**Properties:**
- **Width**: 100% (full width)
- **Background**: Gradient (blue to orange)
- **Font Size**: 1.2rem
- **Hover Effect**: Lifts up 2px with enhanced shadow

---

### 4. AI Output Box (RAG Generation) - HIGHLIGHTED
```css
.ai-output-box {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 15px;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    border: 3px solid #ff7f0e;
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

.ai-output-title {
    font-size: 1.8rem;
    font-weight: bold;
    margin-bottom: 1rem;
    text-align: center;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.ai-output-content {
    font-size: 1.1rem;
    line-height: 1.8;
    background: rgba(255, 255, 255, 0.1);
    padding: 1.5rem;
    border-radius: 10px;
    backdrop-filter: blur(10px);
}

.rag-badge {
    display: inline-block;
    background: rgba(255, 255, 255, 0.3);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    margin-bottom: 1rem;
    font-weight: bold;
}
```

**DOM Structure:**
```html
<div class="ai-output-box">
    <div class="rag-badge">🤖 RAG-GENERATED OUTPUT</div>
    <div class="ai-output-title">✨ AI-Powered Recommendation</div>
    <div class="ai-output-content">
        <!-- Ollama generated response text -->
    </div>
</div>
```

**Properties:**
- **Background**: Purple gradient (#667eea to #764ba2)
- **Border**: 3px solid orange (#ff7f0e)
- **Padding**: 2.5rem
- **Border Radius**: 15px
- **Box Shadow**: Large purple shadow with 0.4 opacity
- **Animation**: Fade-in effect (0.5s)
- **Text Color**: White
- **Backdrop Filter**: Blur effect on content area

---

### 5. Intervention Card Styling
```css
.intervention-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    border-left: 5px solid #1f77b4;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

**DOM Element:**
```html
<div class="intervention-card">
    <!-- Intervention details -->
</div>
```

---

### 6. Hidden Elements
```css
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
```

**Purpose**: Hides Streamlit default branding elements

---

### 7. Sidebar Styling
```css
.css-1d391kg {
    background-color: #f8f9fa;
}
```

---

## Component Structure

### 1. Header Section
```python
st.markdown('<h1 class="main-header">🛣️ Road Safety Intervention GPT</h1>', unsafe_allow_html=True)
st.markdown("### AI-Powered RAG System - Retrieval-Augmented Generation with Ollama")
```

**DOM Output:**
```html
<h1 class="main-header">🛣️ Road Safety Intervention GPT</h1>
<h3>AI-Powered RAG System - Retrieval-Augmented Generation with Ollama</h3>
```

---

### 2. System Flow Info (Expandable)
```python
with st.expander("ℹ️ How RAG Works"):
    st.markdown("""...""")
```

**DOM Structure:**
```html
<details class="stExpander">
    <summary>ℹ️ How RAG Works</summary>
    <div>
        <!-- RAG explanation content -->
    </div>
</details>
```

---

### 3. Sidebar Components

#### Database Status Section
```python
with st.sidebar:
    st.header("📊 System Status")
    st.success(f"✅ **{len(data)}** interventions loaded")
    st.info(f"📂 Categories: {count}")
    st.warning("⚠️ No interventions loaded")
```

**DOM Structure:**
```html
<aside class="css-1d391kg">
    <h2>📊 System Status</h2>
    <div class="stSuccess">
        ✅ **{count}** interventions loaded
    </div>
    <div class="stInfo">
        📂 Categories: {count}
    </div>
</aside>
```

#### File Uploader
```python
uploaded_file = st.file_uploader("📤 Upload Interventions JSON", type=['json'])
```

**DOM Element:**
```html
<div class="stFileUploader">
    <input type="file" accept=".json">
    <label>📤 Upload Interventions JSON</label>
</div>
```

#### Settings Section
```python
top_k = st.slider("Results to show", min_value=1, max_value=5, value=3)
ollama_model = st.text_input("Ollama Model", value=rag_system.ollama_model)
```

**DOM Elements:**
```html
<!-- Slider -->
<div class="stSlider">
    <input type="range" min="1" max="5" value="3">
    <label>Results to show</label>
</div>

<!-- Text Input -->
<div class="stTextInput">
    <input type="text" value="llama3.2:3b">
    <label>Ollama Model</label>
</div>
```

---

### 4. Main Content Area

#### Query Input Section
```python
st.markdown("### 📝 Enter Your Query")
user_query = st.text_area("", placeholder="...", height=120, key="query_input")
```

**DOM Structure:**
```html
<h3>📝 Enter Your Query</h3>
<div class="stTextArea">
    <div>
        <div>
            <textarea 
                placeholder="Example: How to fix a damaged STOP sign?..."
                height="120"
                key="query_input"
                style="border: 3px solid #1f77b4; border-radius: 10px; padding: 1rem; font-size: 1.1rem;"
            ></textarea>
        </div>
    </div>
</div>
```

#### Example Query Buttons
```python
col1, col2, col3 = st.columns(3)
for i, example in enumerate(examples):
    with [col1, col2, col3][i]:
        st.button(f"💡 {example[:30]}...", key=f"ex_{i}")
```

**DOM Structure:**
```html
<div class="row">
    <div class="column">
        <button class="stButton">💡 How to fix a damaged STOP...</button>
    </div>
    <div class="column">
        <button class="stButton">💡 What are speed hump requ...</button>
    </div>
    <div class="column">
        <button class="stButton">💡 Missing road markings on...</button>
    </div>
</div>
```

#### Get Recommendations Button
```python
st.button("🚀 Get AI Recommendations", type="primary", use_container_width=True)
```

**DOM Element:**
```html
<div class="stButton">
    <button 
        type="button" 
        class="primary"
        style="width: 100%; background: linear-gradient(90deg, #1f77b4, #ff7f0e); color: white; font-size: 1.2rem; font-weight: bold; padding: 0.75rem 2rem; border-radius: 10px;"
    >
        🚀 Get AI Recommendations
    </button>
</div>
```

---

### 5. AI Output Section (RAG Generation)

**HTML Structure:**
```html
<div class="ai-output-box" style="
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2.5rem;
    border-radius: 15px;
    margin: 2rem 0;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
    border: 3px solid #ff7f0e;
    animation: fadeIn 0.5s ease-in;
">
    <div class="rag-badge" style="
        display: inline-block;
        background: rgba(255, 255, 255, 0.3);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-size: 0.9rem;
        margin-bottom: 1rem;
        font-weight: bold;
    ">
        🤖 RAG-GENERATED OUTPUT
    </div>
    
    <div class="ai-output-title" style="
        font-size: 1.8rem;
        font-weight: bold;
        margin-bottom: 1rem;
        text-align: center;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    ">
        ✨ AI-Powered Recommendation
    </div>
    
    <div class="ai-output-content" style="
        font-size: 1.1rem;
        line-height: 1.8;
        background: rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 10px;
        backdrop-filter: blur(10px);
    ">
        <!-- Ollama generated response text here -->
        {AI_RECOMMENDATION_TEXT}
    </div>
</div>
```

---

### 6. Metrics Section
```python
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Interventions Found", len(result['retrieved_interventions']))
with col2:
    st.metric("Processing Time", f"{elapsed_time:.2f}s")
with col3:
    st.metric("Avg Relevance", f"{avg_score:.3f}")
with col4:
    st.metric("RAG Status", "✅ Complete")
```

**DOM Structure:**
```html
<div class="row">
    <div class="column">
        <div class="stMetric">
            <div class="metric-label">Interventions Found</div>
            <div class="metric-value">{count}</div>
        </div>
    </div>
    <div class="column">
        <div class="stMetric">
            <div class="metric-label">Processing Time</div>
            <div class="metric-value">{time}s</div>
        </div>
    </div>
    <div class="column">
        <div class="stMetric">
            <div class="metric-label">Avg Relevance</div>
            <div class="metric-value">{score}</div>
        </div>
    </div>
    <div class="column">
        <div class="stMetric">
            <div class="metric-label">RAG Status</div>
            <div class="metric-value">✅ Complete</div>
        </div>
    </div>
</div>
```

---

### 7. Source Interventions Section
```python
st.markdown("### 📚 Source Interventions (Used for RAG Context)")
st.info("These interventions from your dataset were used to generate the AI recommendation above")

for idx, intervention in enumerate(result['retrieved_interventions']):
    with st.expander(f"**{idx+1}. {name}** | Category: {cat} | Relevance: {score}"):
        col_a, col_b = st.columns(2)
        # ... intervention details
```

**DOM Structure:**
```html
<h3>📚 Source Interventions (Used for RAG Context)</h3>
<div class="stInfo">
    These interventions from your dataset were used to generate the AI recommendation above
</div>

<details class="stExpander">
    <summary>
        <strong>1. {Intervention Name}</strong> | 
        Category: {Category} | 
        Relevance: {Score}
    </summary>
    <div>
        <div class="row">
            <div class="column">
                <strong>📝 Description:</strong>
                <p>{Description text}</p>
                
                <strong>🎯 Problem:</strong>
                <p>{Problem types}</p>
            </div>
            <div class="column">
                <strong>📊 Technical Details:</strong>
                <ul>
                    <li><strong>Code:</strong> {Code}</li>
                    <li><strong>Clause:</strong> {Clause}</li>
                    <li><strong>S. No.:</strong> {Serial Number}</li>
                    <li><strong>Relevance Score:</strong> {Score}</li>
                </ul>
            </div>
        </div>
    </div>
</details>
```

---

### 8. Tabs Section
```python
tab1, tab2 = st.tabs(["📚 Database", "ℹ️ About"])
```

**DOM Structure:**
```html
<div class="stTabs">
    <div class="stTabsHeader">
        <button class="stTab" data-tab="0">📚 Database</button>
        <button class="stTab" data-tab="1">ℹ️ About</button>
    </div>
    <div class="stTabsContent">
        <div class="stTabContent" data-tab="0">
            <!-- Database tab content -->
        </div>
        <div class="stTabContent" data-tab="1">
            <!-- About tab content -->
        </div>
    </div>
</div>
```

---

## Layout Hierarchy

### Complete DOM Tree Structure

```
<body>
    <div class="stApp">
        <!-- Sidebar -->
        <aside class="css-1d391kg">
            <h2>📊 System Status</h2>
            <div class="stSuccess">✅ Database loaded</div>
            <div class="stInfo">📂 Categories: {count}</div>
            
            <div class="stFileUploader">
                <input type="file" accept=".json">
            </div>
            
            <h2>⚙️ Settings</h2>
            <div class="stSlider">
                <input type="range" min="1" max="5" value="3">
            </div>
            <div class="stTextInput">
                <input type="text" value="llama3.2:3b">
            </div>
        </aside>
        
        <!-- Main Content -->
        <main>
            <!-- Header -->
            <h1 class="main-header">🛣️ Road Safety Intervention GPT</h1>
            <h3>AI-Powered RAG System...</h3>
            
            <!-- Expandable Info -->
            <details class="stExpander">
                <summary>ℹ️ How RAG Works</summary>
                <div>...</div>
            </details>
            
            <!-- Query Input Section -->
            <h3>📝 Enter Your Query</h3>
            <div class="stTextArea">
                <textarea 
                    placeholder="..."
                    height="120"
                    style="border: 3px solid #1f77b4; ..."
                ></textarea>
            </div>
            
            <!-- Example Buttons -->
            <div class="row">
                <div class="column">
                    <button>💡 Example 1</button>
                </div>
                <div class="column">
                    <button>💡 Example 2</button>
                </div>
                <div class="column">
                    <button>💡 Example 3</button>
                </div>
            </div>
            
            <!-- Get Recommendations Button -->
            <div class="stButton">
                <button style="...">🚀 Get AI Recommendations</button>
            </div>
            
            <!-- AI OUTPUT BOX (RAG Generation) -->
            <div class="ai-output-box" style="...">
                <div class="rag-badge">🤖 RAG-GENERATED OUTPUT</div>
                <div class="ai-output-title">✨ AI-Powered Recommendation</div>
                <div class="ai-output-content">
                    {OLLAMA_GENERATED_RESPONSE}
                </div>
            </div>
            
            <!-- Metrics -->
            <div class="row">
                <div class="column">
                    <div class="stMetric">...</div>
                </div>
                <!-- ... more metrics ... -->
            </div>
            
            <!-- Source Interventions -->
            <h3>📚 Source Interventions</h3>
            <details class="stExpander">
                <summary>Intervention 1</summary>
                <div>...</div>
            </details>
            
            <!-- Tabs -->
            <div class="stTabs">
                <div class="stTabsHeader">...</div>
                <div class="stTabsContent">...</div>
            </div>
        </main>
    </div>
</body>
```

---

## Functionality Details

### 1. RAG System Initialization
```python
@st.cache_resource
def load_rag_system():
    # Loads RAG system and auto-loads interventions.json
    # Cached to avoid reloading on every interaction
```

**Behavior:**
- Loads on first run
- Cached for subsequent requests
- Auto-loads `interventions.json` if exists

### 2. Query Processing Flow
```python
if st.button("🚀 Get AI Recommendations"):
    if user_query:
        # 1. RAG Retrieval
        result = rag_system.get_recommendations(user_query, top_k=top_k)
        
        # 2. Display AI Output (RAG Generation)
        st.markdown('<div class="ai-output-box">...</div>')
        st.markdown(result['recommendation'])
        
        # 3. Display Source Interventions
        for intervention in result['retrieved_interventions']:
            # Show expandable cards
```

### 3. Real-time Updates
- Streamlit uses WebSocket for real-time updates
- When Python code executes, browser updates automatically
- No page reload needed

---

## DOM Elements Reference

### Input Elements
- **Query Text Area**: `.stTextArea > div > div > textarea`
- **File Uploader**: `.stFileUploader > input[type="file"]`
- **Slider**: `.stSlider > input[type="range"]`
- **Text Input**: `.stTextInput > input[type="text"]`

### Button Elements
- **Primary Button**: `.stButton > button.primary`
- **Example Buttons**: `.stButton > button` (in columns)

### Display Elements
- **AI Output Box**: `.ai-output-box`
- **RAG Badge**: `.rag-badge`
- **AI Output Title**: `.ai-output-title`
- **AI Output Content**: `.ai-output-content`
- **Intervention Cards**: `.intervention-card` or `.stExpander`

### Metrics
- **Metric Container**: `.stMetric`
- **Metric Label**: `.metric-label`
- **Metric Value**: `.metric-value`

### Layout Elements
- **Columns**: `.row > .column` (via `st.columns()`)
- **Tabs**: `.stTabs > .stTabsHeader > .stTab`
- **Expander**: `.stExpander > summary` and `.stExpander > div`

### Status Elements
- **Success Message**: `.stSuccess`
- **Info Message**: `.stInfo`
- **Warning Message**: `.stWarning`
- **Error Message**: `.stError`

---

## Color Scheme

### Primary Colors
- **Blue**: `#1f77b4` (input border, buttons)
- **Orange**: `#ff7f0e` (focus state, accents)
- **Purple Gradient**: `#667eea` to `#764ba2` (AI output box)

### Background Colors
- **Sidebar**: `#f8f9fa`
- **AI Output**: Gradient purple
- **Cards**: White (`#ffffff`)

### Text Colors
- **Default**: Black/dark gray
- **AI Output**: White
- **Headers**: Gradient (blue to orange)

---

## Animations

### Fade-in Animation
```css
@keyframes fadeIn {
    from { 
        opacity: 0; 
        transform: translateY(10px); 
    }
    to { 
        opacity: 1; 
        transform: translateY(0); 
    }
}
```

**Applied to:**
- AI Output Box (0.5s ease-in)

### Hover Effects
- **Buttons**: `translateY(-2px)` on hover
- **Input**: Border color change and shadow enhancement on focus

---

## Responsive Behavior

### Layout
- **Wide Layout**: Full width utilization
- **Columns**: Responsive grid (3 columns for examples, 4 for metrics, 2 for intervention details)
- **Sidebar**: Expandable/collapsible

### Text Sizing
- **Header**: 3rem
- **AI Output Title**: 1.8rem
- **AI Output Content**: 1.1rem
- **Input Text**: 1.1rem
- **Button Text**: 1.2rem

---

## Interactive Elements

### 1. Query Input
- **Type**: Text area
- **Height**: 120px
- **Placeholder**: Example queries
- **Focus Effect**: Orange border, enhanced shadow

### 2. Example Buttons
- **Count**: 3 buttons
- **Layout**: 3 columns
- **Action**: Populates query input and triggers rerun

### 3. Get Recommendations Button
- **Type**: Primary (gradient background)
- **Width**: 100%
- **Action**: Triggers RAG processing

### 4. Expandable Sections
- **Interventions**: Expandable cards with details
- **Error Details**: Expandable error information
- **Full Content**: Expandable full intervention content

### 5. Tabs
- **Database Tab**: Shows all interventions, search, statistics
- **About Tab**: Application information

---

## Data Flow in DOM

```
User Input (textarea)
    ↓
Button Click (st.button)
    ↓
Python Code Execution
    ↓
RAG Processing
    ↓
AI Output Box (div.ai-output-box)
    ├── RAG Badge (div.rag-badge)
    ├── Title (div.ai-output-title)
    └── Content (div.ai-output-content) ← Ollama Response
    ↓
Metrics (div.stMetric × 4)
    ↓
Source Interventions (div.stExpander × N)
    ↓
Browser Display (real-time update)
```

---

## Complete CSS Classes Reference

### Custom Classes
- `.main-header` - Main page title
- `.ai-output-box` - RAG generation output container
- `.rag-badge` - RAG output badge
- `.ai-output-title` - AI output title
- `.ai-output-content` - AI output content area
- `.intervention-card` - Intervention display card
- `.metric-container` - Metrics container

### Streamlit Classes
- `.stTextArea` - Text area wrapper
- `.stButton` - Button wrapper
- `.stExpander` - Expandable section
- `.stMetric` - Metric display
- `.stSuccess` - Success message
- `.stInfo` - Info message
- `.stWarning` - Warning message
- `.stError` - Error message
- `.stTabs` - Tabs container
- `.stFileUploader` - File upload wrapper
- `.stSlider` - Slider wrapper
- `.stTextInput` - Text input wrapper

---

## JavaScript/WebSocket Behavior

### Streamlit Auto-Refresh
- Streamlit maintains WebSocket connection
- When Python code updates `st.markdown()` or other display functions
- Browser automatically receives update
- No manual refresh needed
- Updates appear in real-time

### Event Handling
- Button clicks trigger Python code execution
- File uploads trigger data reload
- Slider changes update `top_k` value
- Text input changes update Ollama model name

---

## Complete Interface Structure Summary

```
┌─────────────────────────────────────────────────────────┐
│  🛣️ Road Safety Intervention GPT (Header)              │
│  AI-Powered RAG System (Subtitle)                       │
│  [ℹ️ How RAG Works] (Expandable)                       │
├─────────────────────────────────────────────────────────┤
│  📝 Enter Your Query                                    │
│  ┌─────────────────────────────────────────────────┐   │
│  │ [Query Input Text Area - Highlighted Blue]     │   │
│  └─────────────────────────────────────────────────┘   │
│  [💡 Example 1] [💡 Example 2] [💡 Example 3]         │
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🚀 Get AI Recommendations (Gradient Button)    │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │ 🤖 RAG-GENERATED OUTPUT (Badge)                │   │
│  │ ✨ AI-Powered Recommendation (Title)            │   │
│  │ ┌───────────────────────────────────────────┐  │   │
│  │ │ {Ollama Generated Response Text}          │  │   │
│  │ │ (Purple gradient box with orange border)  │  │   │
│  │ └───────────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────────┘   │
├─────────────────────────────────────────────────────────┤
│  [Interventions Found] [Processing Time] [Relevance]   │
│  [RAG Status]                                           │
├─────────────────────────────────────────────────────────┤
│  📚 Source Interventions (Used for RAG Context)        │
│  [▼ 1. Intervention Name | Category | Relevance]       │
│  [▼ 2. Intervention Name | Category | Relevance]       │
│  [▼ 3. Intervention Name | Category | Relevance]       │
├─────────────────────────────────────────────────────────┤
│  [📚 Database] [ℹ️ About] (Tabs)                        │
└─────────────────────────────────────────────────────────┘
```

---

## Technical Specifications

### File Structure
- **Main File**: `web_interface.py`
- **Dependencies**: `ollama_integration.py`, `embedding_pipeline.py`
- **Data Source**: `interventions.json`

### Streamlit Components Used
1. `st.set_page_config()` - Page configuration
2. `st.markdown()` - Markdown rendering
3. `st.title()` / `st.header()` - Headers
4. `st.text_area()` - Query input
5. `st.button()` - Action buttons
6. `st.columns()` - Layout columns
7. `st.metric()` - Metrics display
8. `st.expander()` - Expandable sections
9. `st.tabs()` - Tab navigation
10. `st.sidebar` - Sidebar container
11. `st.file_uploader()` - File upload
12. `st.slider()` - Slider input
13. `st.text_input()` - Text input
14. `st.success()` / `st.info()` / `st.warning()` / `st.error()` - Status messages
15. `st.spinner()` - Loading indicator
16. `st.cache_resource` - Resource caching

### Browser Compatibility
- Modern browsers (Chrome, Firefox, Edge, Safari)
- WebSocket support required
- JavaScript enabled

### Performance
- **Caching**: RAG system cached with `@st.cache_resource`
- **Lazy Loading**: Interventions loaded on demand
- **Real-time Updates**: WebSocket-based updates

---

This documentation covers every aspect of the web interface, from CSS styling to DOM structure to functionality. All elements are documented with their properties, behaviors, and relationships.

