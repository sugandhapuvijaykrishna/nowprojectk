import streamlit as st
from ollama_integration import RoadSafetyRAG
import json
import os
import time
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Road Safety Intervention GPT", 
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS with highlighted query input
st.markdown("""
    <style>
    /* Main header */
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
    
    /* Highlight query input area */
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
    
    /* Primary button styling */
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
    
    /* Response box styling */
    .response-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1.5rem 0;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
    }
    
    .intervention-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #1f77b4;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #f8f9fa;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🛣️ Road Safety Intervention GPT</h1>', unsafe_allow_html=True)
st.markdown("### AI-Powered Recommendations Using RAG & Ollama")

# System Flow Info
with st.expander("ℹ️ How It Works - Click to see the flow"):
    st.markdown("""
    **🔄 Complete System Flow:**
    
    1. **📝 Your Query** → You enter a question/prompt
    2. **🔍 RAG Semantic Search** → System searches `interventions.json` using AI embeddings
    3. **📊 Enhanced Query** → Retrieved interventions are formatted as context
    4. **🤖 Ollama Local Model** → Processes enhanced query and generates recommendation
    5. **💻 Streamlit Display** → Shows AI response + retrieved interventions
    
    **RAG = Retrieval (semantic search) + Augmentation (context building) + Generation (Ollama)**
    
    ---
    
    **🖥️ How Local Model Works with Streamlit:**
    
    - **Streamlit** runs locally on your machine (localhost:8501)
    - **Ollama** runs locally on your machine (localhost:11434 or subprocess)
    - When you click "Get Recommendations":
      1. Streamlit Python code executes
      2. Calls Ollama via local HTTP API or subprocess
      3. Ollama processes query using local model (llama3.2:3b)
      4. Response returns to Streamlit (same machine, fast!)
      5. Streamlit automatically updates browser in real-time
      6. You see the result instantly!
    
    **Everything runs on YOUR computer - no cloud, no external APIs!** ✅
    """)

# Initialize RAG system
@st.cache_resource
def load_rag_system():
    rag = RoadSafetyRAG()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    interventions_file_path = os.path.join(script_dir, "interventions.json")
    if os.path.exists(interventions_file_path) and not rag.pipeline.data:
        try:
            with open(interventions_file_path, 'r', encoding='utf-8') as f:
                interventions_data = json.load(f)
                if rag.pipeline.add_interventions_to_db(interventions_data):
                    print(f"✅ Auto-loaded {len(interventions_data)} interventions from interventions.json")
        except Exception as e:
            print(f"⚠️ Could not auto-load interventions.json: {str(e)}")
    return rag

rag_system = load_rag_system()

# Sidebar
with st.sidebar:
    st.header("📊 System Status")
    st.markdown("---")
    
    # Database status
    if rag_system.pipeline.data and len(rag_system.pipeline.data) > 0:
        st.success(f"✅ **{len(rag_system.pipeline.data)}** interventions loaded")
        
        # Quick stats
        categories = set()
        problems = set()
        for intervention in rag_system.pipeline.data:
            if intervention.get('category'):
                categories.add(intervention.get('category'))
            if intervention.get('problem'):
                problems.add(intervention.get('problem'))
        
        st.info(f"📂 Categories: {len(categories)}")
        st.info(f"🎯 Problem Types: {len(problems)}")
    else:
        st.warning("⚠️ No interventions loaded")
        st.markdown("Upload a JSON file to get started")
    
    st.markdown("---")
    
    # File uploader
    uploaded_file = st.file_uploader("📤 Upload Interventions JSON", type=['json'])
    if uploaded_file:
        try:
            interventions_data = json.load(uploaded_file)
            if rag_system.pipeline.add_interventions_to_db(interventions_data):
                st.success(f"✅ Loaded {len(interventions_data)} interventions")
                st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("---")
    st.header("⚙️ Settings")
    
    top_k = st.slider("Results to show", min_value=1, max_value=5, value=3)
    
    ollama_model = st.text_input("Ollama Model", value=rag_system.ollama_model)
    if ollama_model != rag_system.ollama_model:
        rag_system.ollama_model = ollama_model

# Main content area - Focused on Query Input
st.markdown("---")

# Query Input Section - HIGHLIGHTED
st.markdown("### 🔍 Enter Your Road Safety Query")
st.markdown("Ask questions about road safety interventions, signs, markings, or traffic calming measures")

# Query input with highlighting
user_query = st.text_area(
    "",
    placeholder="Example: How to fix a damaged STOP sign? or What are the requirements for speed humps?",
    height=120,
    key="query_input",
    help="Describe your road safety problem or question"
)

# Example queries
col1, col2, col3 = st.columns(3)
examples = [
    "How to fix a damaged STOP sign?",
    "What are speed hump requirements?",
    "Missing road markings on highway"
]

for i, example in enumerate(examples):
    with [col1, col2, col3][i]:
        if st.button(f"💡 {example[:30]}...", key=f"ex_{i}", use_container_width=True):
            user_query = example
            st.rerun()

st.markdown("---")

# Get Recommendations Button - PROMINENT
if st.button("🚀 Get AI Recommendations", type="primary", use_container_width=True):
    if user_query:
        start_time = time.time()
        
        with st.spinner("🔍 Searching database and generating recommendations with Ollama..."):
            try:
                result = rag_system.get_recommendations(user_query, top_k=top_k)
                elapsed_time = time.time() - start_time
                
                # Display Results
                st.markdown("---")
                
                # Success metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Interventions Found", len(result['retrieved_interventions']))
                with col2:
                    st.metric("Processing Time", f"{elapsed_time:.2f}s")
                with col3:
                    if result['retrieved_interventions']:
                        avg_score = sum(i.get('similarity_score', 0) for i in result['retrieved_interventions']) / len(result['retrieved_interventions'])
                        st.metric("Avg Relevance", f"{avg_score:.3f}")
                
                st.markdown("---")
                
                # AI Recommendation - HIGHLIGHTED
                if result.get('recommendation'):
                    st.markdown("### 🤖 AI-Powered Recommendation")
                    st.markdown('<div class="response-box">', unsafe_allow_html=True)
                    st.markdown(result['recommendation'])
                    st.markdown('</div>', unsafe_allow_html=True)
                
                st.markdown("---")
                
                # Retrieved Interventions
                if result['retrieved_interventions']:
                    st.markdown("### 📋 Relevant Interventions from Database")
                    
                    for idx, intervention in enumerate(result['retrieved_interventions']):
                        with st.expander(
                            f"**{idx+1}. {intervention.get('name', 'N/A')}** | "
                            f"Category: {intervention.get('category', 'N/A')} | "
                            f"Relevance: {intervention.get('similarity_score', 0):.3f}",
                            expanded=(idx == 0)
                        ):
                            col_a, col_b = st.columns(2)
                            
                            with col_a:
                                st.markdown("**📝 Description:**")
                                description = intervention.get('description') or intervention.get('data', 'N/A')
                                st.write(description)
                                
                                st.markdown("**🎯 Problem:**")
                                problems = intervention.get('problem_type', [])
                                if not problems and intervention.get('problem'):
                                    problems = [intervention.get('problem')]
                                st.write(", ".join(problems) if problems else "N/A")
                            
                            with col_b:
                                st.markdown("**📊 Technical Details:**")
                                if intervention.get('code'):
                                    st.write(f"**Code:** {intervention.get('code')}")
                                if intervention.get('clause'):
                                    st.write(f"**Clause:** {intervention.get('clause')}")
                                if intervention.get('S. No.'):
                                    st.write(f"**S. No.:** {intervention.get('S. No.')}")
                                st.write(f"**Relevance Score:** {intervention.get('similarity_score', 0):.4f}")
                                
                                if intervention.get('content'):
                                    with st.expander("📄 View Full Content"):
                                        st.write(intervention.get('content'))
                else:
                    st.warning("⚠️ No relevant interventions found. Try rephrasing your query.")
                    if result.get('recommendation'):
                        st.info(result['recommendation'])
                
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                with st.expander("🔍 Error Details"):
                    st.exception(e)
    else:
        st.warning("⚠️ Please enter a query in the text area above")

# Additional tabs for database info
tab1, tab2 = st.tabs(["📚 Database", "ℹ️ About"])

with tab1:
    st.header("📚 Database Information")
    
    if rag_system.pipeline.data and len(rag_system.pipeline.data) > 0:
        st.metric("Total Interventions", len(rag_system.pipeline.data))
        
        # Statistics
        col1, col2 = st.columns(2)
        
        with col1:
            category_counts = {}
            for intervention in rag_system.pipeline.data:
                cat = intervention.get('category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            st.markdown("**By Category:**")
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {cat}: {count}")
        
        with col2:
            problem_counts = {}
            for intervention in rag_system.pipeline.data:
                problem = intervention.get('problem', '')
                if problem:
                    problem_counts[problem] = problem_counts.get(problem, 0) + 1
            st.markdown("**By Problem Type:**")
            for prob, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                st.write(f"- {prob}: {count}")
        
        # Search
        st.markdown("---")
        search_term = st.text_input("🔍 Search Database", placeholder="Search by name, problem, or category")
        
        filtered_data = rag_system.pipeline.data
        if search_term:
            search_lower = search_term.lower()
            filtered_data = [
                i for i in rag_system.pipeline.data
                if (search_lower in (i.get('type') or i.get('name', '')).lower() or
                    search_lower in (i.get('data') or i.get('description', '')).lower() or
                    search_lower in (i.get('problem', '')).lower() or
                    search_lower in (i.get('category', '')).lower())
            ]
            st.info(f"Found {len(filtered_data)} matching intervention(s)")
        
        # Display filtered results
        for intervention in filtered_data[:20]:  # Limit to 20 for performance
            name = intervention.get('type') or intervention.get('name', 'Unknown')
            with st.expander(f"**{name}** | {intervention.get('category', 'N/A')} | Problem: {intervention.get('problem', 'N/A')}"):
                st.json(intervention)
    else:
        st.info("📤 Upload a JSON file to populate the database")

with tab2:
    st.header("ℹ️ About")
    st.markdown("""
    ### Road Safety Intervention GPT
    
    **AI-powered RAG system for road safety recommendations**
    
    #### How It Works:
    1. **Semantic Search**: Your query is matched against the intervention database using AI embeddings
    2. **Relevant Retrieval**: Top matching interventions are retrieved based on similarity
    3. **AI Analysis**: Ollama LLM analyzes the retrieved interventions and generates recommendations
    4. **Comprehensive Response**: You get both the AI recommendation and relevant intervention details
    
    #### Features:
    - 🔍 Intelligent semantic search
    - 🤖 AI-powered recommendations via Ollama
    - 📊 Detailed intervention information
    - 📚 Complete database access
    
    #### Technology:
    - **Streamlit**: Web interface
    - **Ollama**: Local LLM (llama3.2:3b)
    - **Sentence Transformers**: Embeddings
    - **RAG**: Retrieval-Augmented Generation
    """)
