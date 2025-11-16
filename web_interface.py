import streamlit as st
from ollama_integration import RoadSafetyRAG
import json
import os
import time
from datetime import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Road Safety Intervention GPT",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "AI-Powered RAG System for Road Safety Recommendations"
    }
)

# ============================================================================
# ENTERPRISE-GRADE CSS STYLING (All Inline)
# ============================================================================
st.markdown("""
<style>
    /* ===== RESET & BASE ===== */
    * {
        box-sizing: border-box;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ===== ROOT VARIABLES ===== */
    :root {
        --primary-blue: #2563eb;
        --primary-orange: #f59e0b;
        --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --gradient-secondary: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --gradient-accent: linear-gradient(90deg, #1f77b4, #ff7f0e);
        --bg-primary: #ffffff;
        --bg-secondary: #f8fafc;
        --bg-tertiary: #f1f5f9;
        --text-primary: #1e293b;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
        --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        --radius-sm: 8px;
        --radius-md: 12px;
        --radius-lg: 16px;
        --radius-xl: 24px;
    }
    
    /* ===== MAIN CONTAINER ===== */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* ===== MODERN HEADER ===== */
    .dashboard-header {
        background: var(--gradient-primary);
        padding: 3rem 2rem;
        border-radius: var(--radius-xl);
        margin-bottom: 2rem;
        box-shadow: var(--shadow-xl);
        position: relative;
        overflow: hidden;
    }
    
    .dashboard-header::before {
        content: '';
        position: absolute;
        top: -50%;
        right: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
        animation: pulse 4s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); opacity: 0.5; }
        50% { transform: scale(1.1); opacity: 0.8; }
    }
    
    .dashboard-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: white;
        text-align: center;
        margin: 0;
        text-shadow: 0 4px 12px rgba(0,0,0,0.3);
        letter-spacing: -0.02em;
        position: relative;
        z-index: 1;
    }
    
    .dashboard-subtitle {
        font-size: 1.25rem;
        color: rgba(255,255,255,0.95);
        text-align: center;
        margin-top: 0.5rem;
        font-weight: 400;
        position: relative;
        z-index: 1;
    }
    
    .dashboard-badge {
        display: inline-block;
        background: rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1.25rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
        color: white;
        margin-top: 1rem;
        border: 1px solid rgba(255,255,255,0.3);
        position: relative;
        z-index: 1;
    }
    
    /* ===== QUERY COMPOSER SECTION ===== */
    .query-composer {
        background: var(--bg-primary);
        border-radius: var(--radius-lg);
        padding: 2rem;
        box-shadow: var(--shadow-lg);
        margin-bottom: 2rem;
        border: 1px solid var(--border-color);
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .section-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        margin-bottom: 1.5rem;
        line-height: 1.6;
    }
    
    /* Enhanced Text Area */
    .stTextArea > div > div > textarea {
        border: 2px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        padding: 1.25rem !important;
        font-size: 1.05rem !important;
        line-height: 1.6 !important;
        background: var(--bg-secondary) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-sm) !important;
        font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
    }
    
    .stTextArea > div > div > textarea:focus {
        border-color: var(--primary-blue) !important;
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1), var(--shadow-md) !important;
        outline: none !important;
        background: white !important;
    }
    
    .stTextArea > div > div > textarea::placeholder {
        color: var(--text-secondary) !important;
        opacity: 0.7 !important;
    }
    
    /* Example Chip Buttons */
    .chip-container {
        display: flex;
        gap: 0.75rem;
        flex-wrap: wrap;
        margin-top: 1rem;
    }
    
    .stButton > button[kind="secondary"] {
        background: var(--bg-secondary) !important;
        color: var(--text-primary) !important;
        border: 1.5px solid var(--border-color) !important;
        border-radius: 50px !important;
        padding: 0.625rem 1.25rem !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stButton > button[kind="secondary"]:hover {
        background: var(--bg-tertiary) !important;
        border-color: var(--primary-blue) !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadow-md) !important;
    }
    
    /* Primary Action Button */
    .stButton > button[kind="primary"] {
        background: var(--gradient-accent) !important;
        color: white !important;
        border: none !important;
        border-radius: var(--radius-md) !important;
        padding: 1rem 2rem !important;
        font-size: 1.1rem !important;
        font-weight: 700 !important;
        letter-spacing: 0.025em !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        box-shadow: var(--shadow-lg) !important;
        text-transform: uppercase !important;
        width: 100% !important;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 12px 24px -4px rgba(0,0,0,0.2) !important;
    }
    
    .stButton > button[kind="primary"]:active {
        transform: translateY(0) !important;
    }
    
    /* ===== RAG OUTPUT BOX - ENTERPRISE DESIGN ===== */
    .rag-output-container {
        background: var(--gradient-primary);
        border-radius: var(--radius-xl);
        padding: 0;
        margin: 2rem 0;
        box-shadow: var(--shadow-xl);
        border: 3px solid rgba(255, 255, 255, 0.2);
        overflow: hidden;
        position: relative;
        animation: slideIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .rag-output-header {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(20px);
        padding: 1.5rem 2rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.2);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    .rag-badge-modern {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(10px);
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 700;
        color: white;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .rag-title-modern {
        font-size: 2rem;
        font-weight: 800;
        color: white;
        margin: 0;
        text-shadow: 0 2px 8px rgba(0,0,0,0.2);
        letter-spacing: -0.02em;
    }
    
    .rag-content-box {
        padding: 2.5rem;
        color: white;
        line-height: 1.8;
        font-size: 1.05rem;
    }
    
    .rag-content-inner {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: var(--radius-md);
        border: 1px solid rgba(255, 255, 255, 0.2);
        box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* ===== METRICS STRIP ===== */
    .metrics-strip {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .metric-card-modern {
        background: white;
        border-radius: var(--radius-md);
        padding: 1.5rem;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
    }
    
    .metric-card-modern:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-blue);
    }
    
    .metric-label {
        font-size: 0.875rem;
        font-weight: 600;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 800;
        color: var(--text-primary);
        line-height: 1;
    }
    
    /* ===== INTERVENTION CARDS ===== */
    .intervention-card-modern {
        background: white;
        border-radius: var(--radius-md);
        padding: 0;
        margin: 1rem 0;
        box-shadow: var(--shadow-md);
        border: 1px solid var(--border-color);
        overflow: hidden;
        transition: all 0.3s ease;
    }
    
    .intervention-card-modern:hover {
        box-shadow: var(--shadow-lg);
        transform: translateY(-2px);
        border-color: var(--primary-blue);
    }
    
    .intervention-header {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.25rem 1.5rem;
        border-bottom: 2px solid var(--border-color);
        display: flex;
        align-items: center;
        justify-content: space-between;
        flex-wrap: wrap;
        gap: 0.75rem;
    }
    
    .intervention-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }
    
    .intervention-meta {
        display: flex;
        gap: 1rem;
        align-items: center;
        flex-wrap: wrap;
    }
    
    .meta-badge {
        background: var(--bg-secondary);
        padding: 0.375rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: var(--text-secondary);
    }
    
    .meta-badge.highlight {
        background: var(--gradient-accent);
        color: white;
    }
    
    .intervention-body {
        padding: 1.5rem;
    }
    
    .detail-section {
        margin-bottom: 1.5rem;
    }
    
    .detail-label {
        font-size: 0.875rem;
        font-weight: 700;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .detail-content {
        color: var(--text-primary);
        line-height: 1.7;
        font-size: 0.95rem;
    }
    
    /* ===== SIDEBAR STYLING ===== */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8fafc 0%, #ffffff 100%);
        padding: 1.5rem;
    }
    
    .sidebar-section {
        background: white;
        border-radius: var(--radius-md);
        padding: 1.25rem;
        margin-bottom: 1rem;
        box-shadow: var(--shadow-sm);
        border: 1px solid var(--border-color);
    }
    
    /* ===== STATUS INDICATORS ===== */
    .status-indicator {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.5rem 1rem;
        border-radius: 50px;
        font-size: 0.875rem;
        font-weight: 600;
    }
    
    .status-success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .status-warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .status-info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    /* ===== TABS STYLING ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
        background: var(--bg-secondary);
        padding: 0.5rem;
        border-radius: var(--radius-md);
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: var(--radius-sm);
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: white;
        box-shadow: var(--shadow-md);
    }
    
    /* ===== EXPANDER STYLING ===== */
    .stExpander {
        border: 1px solid var(--border-color) !important;
        border-radius: var(--radius-md) !important;
        margin-bottom: 1rem !important;
        box-shadow: var(--shadow-sm) !important;
    }
    
    .stExpander > summary {
        padding: 1.25rem 1.5rem !important;
        font-weight: 600 !important;
        background: var(--bg-secondary) !important;
        border-radius: var(--radius-md) !important;
    }
    
    /* ===== SPINNER STYLING ===== */
    .stSpinner > div {
        border-color: var(--primary-blue) !important;
    }
    
    /* ===== RESPONSIVE DESIGN ===== */
    @media (max-width: 768px) {
        .dashboard-title {
            font-size: 2.5rem;
        }
        
        .rag-title-modern {
            font-size: 1.5rem;
        }
        
        .metrics-strip {
            grid-template-columns: 1fr;
        }
    }
    
    /* ===== UTILITY CLASSES ===== */
    .divider {
        height: 1px;
        background: var(--border-color);
        margin: 2rem 0;
        border: none;
    }
    
    .text-gradient {
        background: var(--gradient-accent);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DASHBOARD HEADER
# ============================================================================
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">🛣️ Road Safety Intervention GPT</h1>
    <p class="dashboard-subtitle">Enterprise AI-Powered RAG System for Road Safety Recommendations</p>
    <div style="text-align: center;">
        <span class="dashboard-badge">🤖 Powered by Ollama</span>
        <span class="dashboard-badge">🔍 Semantic Search</span>
        <span class="dashboard-badge">📊 RAG Architecture</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================================
# RAG SYSTEM INITIALIZATION
# ============================================================================
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
                    print(f"✅ Auto-loaded {len(interventions_data)} interventions")
        except Exception as e:
            print(f"⚠️ Could not auto-load: {str(e)}")
    return rag

rag_system = load_rag_system()

# ============================================================================
# SIDEBAR - ENTERPRISE DESIGN
# ============================================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-section">
        <h2 style="margin: 0 0 1rem 0; font-size: 1.25rem; font-weight: 700; color: #1e293b;">
            📊 System Status
        </h2>
    """, unsafe_allow_html=True)
    
    if rag_system.pipeline.data and len(rag_system.pipeline.data) > 0:
        st.markdown(f"""
        <div class="status-indicator status-success">
            ✅ <strong>{len(rag_system.pipeline.data)}</strong> Interventions Loaded
        </div>
        """, unsafe_allow_html=True)
        
        categories = set()
        problems = set()
        for intervention in rag_system.pipeline.data:
            if intervention.get('category'):
                categories.add(intervention.get('category'))
            if intervention.get('problem'):
                problems.add(intervention.get('problem'))
        
        st.markdown(f"""
        <div style="margin-top: 1rem;">
            <div class="status-indicator status-info" style="margin-bottom: 0.5rem;">
                📂 {len(categories)} Categories
            </div>
            <div class="status-indicator status-info">
                🎯 {len(problems)} Problem Types
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-indicator status-warning">
            ⚠️ No Data Loaded
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600; color: #1e293b;">
            📤 Data Management
        </h3>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Upload Interventions JSON", type=['json'], label_visibility="collapsed")
    if uploaded_file:
        try:
            interventions_data = json.load(uploaded_file)
            if rag_system.pipeline.add_interventions_to_db(interventions_data):
                st.success(f"✅ Loaded {len(interventions_data)} interventions")
                st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="sidebar-section">
        <h3 style="margin: 0 0 1rem 0; font-size: 1rem; font-weight: 600; color: #1e293b;">
            ⚙️ Configuration
        </h3>
    """, unsafe_allow_html=True)
    
    top_k = st.slider("Results to Retrieve", min_value=1, max_value=5, value=3, help="Number of top interventions to use for RAG context")
    ollama_model = st.text_input("Ollama Model", value=rag_system.ollama_model, help="Local Ollama model name")
    if ollama_model != rag_system.ollama_model:
        rag_system.ollama_model = ollama_model
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN CONTENT - QUERY COMPOSER
# ============================================================================
st.markdown("""
<div class="query-composer">
    <div class="section-title">
        <span>📝</span>
        <span>Query Composer</span>
    </div>
    <div class="section-description">
        Enter your road safety question below. Our RAG system will search your intervention database 
        and generate an AI-powered recommendation using Ollama.
    </div>
""", unsafe_allow_html=True)

user_query = st.text_area(
    "",
    placeholder="Example: How to fix a damaged STOP sign according to IRC standards?",
    height=140,
    key="query_input",
    label_visibility="collapsed",
    help="Describe your road safety problem or question"
)

# Example Query Chips
st.markdown("""
    <div style="margin-top: 1rem;">
        <div style="font-size: 0.875rem; font-weight: 600; color: #64748b; margin-bottom: 0.75rem;">
            💡 Quick Examples:
        </div>
    </div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
examples = [
    "How to fix a damaged STOP sign?",
    "What are speed hump requirements?",
    "Missing road markings on highway"
]

for i, example in enumerate(examples):
    with [col1, col2, col3][i]:
        if st.button(f"{example[:28]}...", key=f"ex_{i}", use_container_width=True, type="secondary"):
            user_query = example
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Action Button
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Generate AI Recommendation", type="primary", use_container_width=True):
    if user_query:
        start_time = time.time()
        
        with st.spinner("🔍 Processing: Semantic Search → Context Building → AI Generation..."):
            try:
                result = rag_system.get_recommendations(user_query, top_k=top_k)
                elapsed_time = time.time() - start_time
                
                # ========================================================================
                # RAG OUTPUT BOX - ENTERPRISE DESIGN
                # ========================================================================
                st.markdown("""
                <div class="rag-output-container">
                    <div class="rag-output-header">
                        <div>
                            <div class="rag-badge-modern">🤖 RAG-Generated Output</div>
                            <h2 class="rag-title-modern" style="margin-top: 0.75rem; margin-bottom: 0;">
                                ✨ AI-Powered Recommendation
                            </h2>
                        </div>
                    </div>
                    <div class="rag-content-box">
                        <div class="rag-content-inner">
                """, unsafe_allow_html=True)
                
                # Display AI recommendation
                if result.get('recommendation'):
                    st.markdown(result['recommendation'])
                else:
                    st.markdown("No recommendation generated. Please check your query and try again.")
                
                st.markdown("""
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # ========================================================================
                # METRICS STRIP - MODERN DESIGN
                # ========================================================================
                st.markdown("""
                <div class="metrics-strip">
                """, unsafe_allow_html=True)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card-modern">
                        <div class="metric-label">Interventions Found</div>
                        <div class="metric-value">{len(result['retrieved_interventions'])}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card-modern">
                        <div class="metric-label">Processing Time</div>
                        <div class="metric-value">{elapsed_time:.2f}s</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if result['retrieved_interventions']:
                        avg_score = sum(i.get('similarity_score', 0) for i in result['retrieved_interventions']) / len(result['retrieved_interventions'])
                        st.markdown(f"""
                        <div class="metric-card-modern">
                            <div class="metric-label">Avg Relevance</div>
                            <div class="metric-value">{avg_score:.3f}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="metric-card-modern">
                            <div class="metric-label">Avg Relevance</div>
                            <div class="metric-value">N/A</div>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col4:
                    st.markdown("""
                    <div class="metric-card-modern">
                        <div class="metric-label">RAG Status</div>
                        <div class="metric-value" style="font-size: 1.5rem;">✅</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("</div>", unsafe_allow_html=True)
                
                # ========================================================================
                # SOURCE INTERVENTIONS - MODERN CARDS
                # ========================================================================
                if result['retrieved_interventions']:
                    st.markdown("""
                    <div style="margin-top: 3rem;">
                        <h2 class="section-title" style="margin-bottom: 0.75rem;">
                            📚 Source Interventions
                        </h2>
                        <p class="section-description" style="margin-bottom: 1.5rem;">
                            These interventions from your dataset were retrieved and used to generate the AI recommendation above.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    for idx, intervention in enumerate(result['retrieved_interventions']):
                        name = intervention.get('name', 'N/A')
                        category = intervention.get('category', 'N/A')
                        score = intervention.get('similarity_score', 0)
                        problem = intervention.get('problem', 'N/A')
                        
                        st.markdown(f"""
                        <div class="intervention-card-modern">
                            <div class="intervention-header">
                                <div>
                                    <div class="intervention-title">
                                        {idx+1}. {name}
                                    </div>
                                </div>
                                <div class="intervention-meta">
                                    <span class="meta-badge">📂 {category}</span>
                                    <span class="meta-badge highlight">⭐ {score:.3f}</span>
                                </div>
                            </div>
                            <div class="intervention-body">
                        """, unsafe_allow_html=True)
                        
                        col_a, col_b = st.columns(2)
                        
                        with col_a:
                            st.markdown("""
                            <div class="detail-section">
                                <div class="detail-label">📝 Description</div>
                                <div class="detail-content">
                            """, unsafe_allow_html=True)
                            description = intervention.get('description') or intervention.get('data', 'N/A')
                            st.write(description)
                            st.markdown("</div></div>", unsafe_allow_html=True)
                            
                            st.markdown("""
                            <div class="detail-section">
                                <div class="detail-label">🎯 Problem Type</div>
                                <div class="detail-content">
                            """, unsafe_allow_html=True)
                            problems = intervention.get('problem_type', [])
                            if not problems and intervention.get('problem'):
                                problems = [intervention.get('problem')]
                            st.write(", ".join(problems) if problems else "N/A")
                            st.markdown("</div></div>", unsafe_allow_html=True)
                        
                        with col_b:
                            st.markdown("""
                            <div class="detail-section">
                                <div class="detail-label">📊 Technical Details</div>
                                <div class="detail-content">
                            """, unsafe_allow_html=True)
                            
                            details_html = "<div style='display: flex; flex-direction: column; gap: 0.5rem;'>"
                            if intervention.get('code'):
                                details_html += f"<div><strong>Code:</strong> {intervention.get('code')}</div>"
                            if intervention.get('clause'):
                                details_html += f"<div><strong>Clause:</strong> {intervention.get('clause')}</div>"
                            if intervention.get('S. No.'):
                                details_html += f"<div><strong>S. No.:</strong> {intervention.get('S. No.')}</div>"
                            details_html += f"<div><strong>Relevance:</strong> {score:.4f}</div>"
                            details_html += "</div>"
                            
                            st.markdown(details_html, unsafe_allow_html=True)
                            st.markdown("</div></div>", unsafe_allow_html=True)
                            
                            if intervention.get('content'):
                                with st.expander("📄 View Full Content"):
                                    st.write(intervention.get('content'))
                        
                        st.markdown("</div></div>", unsafe_allow_html=True)
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

# ============================================================================
# TABS SECTION
# ============================================================================
st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📚 Database Explorer", "ℹ️ About & Documentation"])

with tab1:
    st.markdown("""
    <div style="margin-bottom: 2rem;">
        <h2 class="section-title">📚 Database Explorer</h2>
        <p class="section-description">
            Browse and search through all interventions in your database. 
            Use the search below to filter by name, category, or problem type.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if rag_system.pipeline.data and len(rag_system.pipeline.data) > 0:
        # Statistics Cards
        col1, col2 = st.columns(2)
        
        with col1:
            category_counts = {}
            for intervention in rag_system.pipeline.data:
                cat = intervention.get('category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            
            st.markdown("""
            <div class="metric-card-modern">
                <div class="metric-label">By Category</div>
            """, unsafe_allow_html=True)
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                st.markdown(f"<div style='padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;'><strong>{cat}:</strong> {count}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            problem_counts = {}
            for intervention in rag_system.pipeline.data:
                problem = intervention.get('problem', '')
                if problem:
                    problem_counts[problem] = problem_counts.get(problem, 0) + 1
            
            st.markdown("""
            <div class="metric-card-modern">
                <div class="metric-label">By Problem Type</div>
            """, unsafe_allow_html=True)
            for prob, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                st.markdown(f"<div style='padding: 0.5rem 0; border-bottom: 1px solid #e2e8f0;'><strong>{prob}:</strong> {count}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Search
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        search_term = st.text_input("🔍 Search Database", placeholder="Search by name, problem, category, or description...", key="db_search")
        
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
            st.info(f"Found **{len(filtered_data)}** matching intervention(s)")
        
        # Display Results
        st.markdown(f"<h3 style='margin-top: 2rem; margin-bottom: 1rem; font-size: 1.1rem; font-weight: 600;'>Showing {len(filtered_data[:20])} of {len(filtered_data)} results</h3>", unsafe_allow_html=True)
        
        for intervention in filtered_data[:20]:
            name = intervention.get('type') or intervention.get('name', 'Unknown')
            category = intervention.get('category', 'N/A')
            problem = intervention.get('problem', 'N/A')
            
            with st.expander(f"**{name}** | {category} | Problem: {problem}"):
                st.json(intervention)
    else:
        st.info("📤 Upload a JSON file to populate the database")

with tab2:
    st.markdown("""
    <div style="max-width: 800px;">
        <h2 class="section-title">ℹ️ About Road Safety Intervention GPT</h2>
        
        <div class="metric-card-modern" style="margin: 2rem 0;">
            <h3 style="margin-top: 0; color: #1e293b; font-size: 1.25rem;">🎯 Overview</h3>
            <p style="color: #64748b; line-height: 1.7;">
                This is an enterprise-grade AI-powered system that uses <strong>Retrieval-Augmented Generation (RAG)</strong> 
                to provide intelligent recommendations for road safety interventions. The system combines semantic search 
                with local AI processing to deliver accurate, context-aware responses.
            </p>
        </div>
        
        <div class="metric-card-modern" style="margin: 2rem 0;">
            <h3 style="margin-top: 0; color: #1e293b; font-size: 1.25rem;">🔄 How RAG Works</h3>
            <ol style="color: #64748b; line-height: 2;">
                <li><strong>Retrieval:</strong> Semantic search finds relevant interventions from your dataset using AI embeddings</li>
                <li><strong>Augmentation:</strong> Retrieved interventions are formatted with all technical details (codes, clauses, specifications)</li>
                <li><strong>Generation:</strong> Ollama local model processes the enhanced context and generates comprehensive recommendations</li>
            </ol>
        </div>
        
        <div class="metric-card-modern" style="margin: 2rem 0;">
            <h3 style="margin-top: 0; color: #1e293b; font-size: 1.25rem;">✨ Key Features</h3>
            <ul style="color: #64748b; line-height: 2;">
                <li>🔍 <strong>Intelligent Semantic Search:</strong> Finds relevant results based on meaning, not just keywords</li>
                <li>🤖 <strong>AI-Powered Recommendations:</strong> Local Ollama model generates detailed, actionable advice</li>
                <li>📊 <strong>Technical Details:</strong> References IRC codes, clauses, and specifications</li>
                <li>📚 <strong>Complete Database Access:</strong> Browse and search all interventions</li>
                <li>🔒 <strong>Privacy-First:</strong> All processing happens locally on your machine</li>
            </ul>
        </div>
        
        <div class="metric-card-modern" style="margin: 2rem 0;">
            <h3 style="margin-top: 0; color: #1e293b; font-size: 1.25rem;">🛠️ Technology Stack</h3>
            <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; margin-top: 1rem;">
                <div><strong>Streamlit:</strong> Web Interface</div>
                <div><strong>Ollama:</strong> Local LLM</div>
                <div><strong>Sentence Transformers:</strong> Embeddings</div>
                <div><strong>NumPy:</strong> Vector Operations</div>
            </div>
        </div>
        
        <div class="metric-card-modern" style="margin: 2rem 0;">
            <h3 style="margin-top: 0; color: #1e293b; font-size: 1.25rem;">📖 Usage Guide</h3>
            <ol style="color: #64748b; line-height: 2;">
                <li>Enter your road safety question in the query composer</li>
                <li>Click "Generate AI Recommendation" to process</li>
                <li>Review the RAG-generated output (highlighted purple box)</li>
                <li>Explore source interventions used for context</li>
                <li>Use Database Explorer to browse all interventions</li>
            </ol>
        </div>
    </div>
    """, unsafe_allow_html=True)
        