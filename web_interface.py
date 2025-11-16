import streamlit as st
from ollama_integration import RoadSafetyRAG
import json
import os
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Road Safety Intervention GPT", 
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': "Road Safety Intervention GPT - AI-powered RAG system"
    }
)

# Initialize session state
if 'query_history' not in st.session_state:
    st.session_state.query_history = []
if 'results_cache' not in st.session_state:
    st.session_state.results_cache = {}

# Enhanced CSS styling
st.markdown("""
    <style>
    /* Main styling */
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    /* Card styling */
    .stExpander {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .recommendation-box {
        padding: 1.5rem;
        border-radius: 8px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        padding-top: 2rem;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">🛣️ Road Safety Intervention GPT</h1>', unsafe_allow_html=True)
st.markdown("### AI-powered recommendations for road safety interventions using RAG and Ollama")

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
    st.header("📊 Database Setup")
    st.markdown("---")
    
    # Database status
    if rag_system.pipeline.data and len(rag_system.pipeline.data) > 0:
        st.success(f"✅ Database loaded: **{len(rag_system.pipeline.data)}** interventions")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        interventions_file_path = os.path.join(script_dir, "interventions.json")
        if os.path.exists(interventions_file_path):
            st.info(f"📁 Data from: interventions.json")
        
        # Quick stats
        with st.expander("📈 Quick Stats"):
            categories = {}
            problems = {}
            for intervention in rag_system.pipeline.data:
                cat = intervention.get('category', 'Unknown')
                categories[cat] = categories.get(cat, 0) + 1
                prob = intervention.get('problem', '')
                if prob:
                    problems[prob] = problems.get(prob, 0) + 1
            
            st.write(f"**Categories:** {len(categories)}")
            st.write(f"**Problem Types:** {len(problems)}")
    else:
        st.warning("⚠️ No interventions loaded. Please upload a JSON file.")
    
    # File uploader
    uploaded_file = st.file_uploader("Upload interventions JSON", type=['json'], help="Upload a JSON file containing road safety interventions")
    if uploaded_file:
        try:
            interventions_data = json.load(uploaded_file)
            if rag_system.pipeline.add_interventions_to_db(interventions_data):
                st.success(f"✅ Loaded {len(interventions_data)} interventions")
                st.rerun()
            else:
                st.error("Failed to load interventions")
        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please check the file format.")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    
    st.markdown("---")
    st.header("⚙️ Settings")
    top_k = st.slider("Number of interventions to retrieve", min_value=1, max_value=10, value=3, help="How many top interventions to show")
    
    # Ollama model selection
    ollama_model = st.text_input("Ollama Model", value=rag_system.ollama_model, help="Ollama model to use (e.g., llama3.2:3b, mistral, etc.)")
    if ollama_model != rag_system.ollama_model:
        rag_system.ollama_model = ollama_model
        st.info(f"Model set to: {ollama_model}")
    
    st.markdown("---")
    st.header("📊 Session Info")
    st.write(f"**Queries made:** {len(st.session_state.query_history)}")
    if st.button("🗑️ Clear History"):
        st.session_state.query_history = []
        st.session_state.results_cache = {}
        st.rerun()

# Main tabs
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Query System", "📚 Database Info", "📊 Analytics", "ℹ️ About"])

# Tab 1: Query System
with tab1:
    st.header("Get Safety Recommendations")
    st.markdown("Ask questions about road safety interventions and get AI-powered recommendations")
    
    # Query input section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        user_query = st.text_area(
            "Describe your road safety problem:",
            placeholder="e.g., 'How to fix a damaged STOP sign?' or 'What are the requirements for speed humps?'",
            height=100,
            help="Describe the road safety issue you need help with"
        )
        
        # Example queries
        with st.expander("💡 Example Queries"):
            examples = [
                "How to fix a damaged STOP sign?",
                "What are speed hump requirements?",
                "Missing road markings on highway",
                "Height issue with road signs",
                "Non-retroreflective markings"
            ]
            for example in examples:
                if st.button(f"📝 {example}", key=f"example_{example}", use_container_width=True):
                    user_query = example
                    st.rerun()
    
    with col2:
        road_type = st.selectbox(
            "Road Type (optional):",
            ["", "Highway", "Urban Arterial", "Local Street", "Intersection", "School Zone", "Rural Road"],
            help="Filter by specific road type"
        )
        
        problem_type = st.multiselect(
            "Problem Types (optional):",
            ["Damaged", "Height Issue", "Faded", "Spacing Issue", "Improper Placement", 
             "Obstruction", "Non-Retroreflective", "Missing", "Wrongly Placed", "Visibility Issue",
             "Placement Issue", "Non-Retro Reflective", "Wrong Colour Selection", "Non-Standard"],
            help="Select relevant problem types"
        )
    
    # Query history
    if st.session_state.query_history:
        with st.expander("📜 Recent Queries"):
            for i, hist_query in enumerate(reversed(st.session_state.query_history[-5:])):
                if st.button(f"{i+1}. {hist_query[:50]}...", key=f"hist_{i}", use_container_width=True):
                    user_query = hist_query
                    st.rerun()
    
    # Get recommendations button
    if st.button("🚀 Get Recommendations", type="primary", use_container_width=True):
        if user_query:
            start_time = time.time()
            
            with st.spinner("🔍 Searching interventions and generating AI recommendations..."):
                # Build enhanced query
                query_parts = [user_query]
                if road_type:
                    query_parts.append(f"for {road_type} roads")
                if problem_type:
                    query_parts.append(f"related to {', '.join(problem_type)}")
                
                full_query = " ".join(query_parts)
                
                try:
                    # Check cache
                    cache_key = f"{full_query}_{top_k}"
                    if cache_key in st.session_state.results_cache:
                        result = st.session_state.results_cache[cache_key]
                        st.info("📋 Using cached results")
                    else:
                        result = rag_system.get_recommendations(full_query, top_k=top_k)
                        st.session_state.results_cache[cache_key] = result
                    
                    elapsed_time = time.time() - start_time
                    
                    # Add to history
                    if user_query not in st.session_state.query_history:
                        st.session_state.query_history.append(user_query)
                    
                    if result['retrieved_interventions']:
                        # Success metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Interventions Found", len(result['retrieved_interventions']))
                        with col2:
                            st.metric("Processing Time", f"{elapsed_time:.2f}s")
                        with col3:
                            avg_score = sum(i.get('similarity_score', 0) for i in result['retrieved_interventions']) / len(result['retrieved_interventions'])
                            st.metric("Avg Similarity", f"{avg_score:.3f}")
                        
                        st.markdown("---")
                        st.subheader("📋 Retrieved Interventions")
                        
                        # Display interventions
                        for idx, intervention in enumerate(result['retrieved_interventions']):
                            header_parts = [f"🚦 **{intervention.get('name', 'N/A')}**"]
                            if intervention.get('category'):
                                header_parts.append(f"Category: {intervention.get('category')}")
                            header_parts.append(f"Similarity: {intervention.get('similarity_score', 0):.3f}")
                            
                            with st.expander(" | ".join(header_parts), expanded=(idx == 0)):
                                col_a, col_b = st.columns(2)
                                
                                with col_a:
                                    st.markdown("**📝 Description:**")
                                    description = intervention.get('description') or intervention.get('data', 'N/A')
                                    st.write(description)
                                    
                                    st.markdown("**🎯 Problem:**")
                                    problems = intervention.get('problem_type', [])
                                    if not problems and intervention.get('problem'):
                                        problems = [intervention.get('problem')]
                                    if problems:
                                        st.write(", ".join(problems) if isinstance(problems, list) else problems)
                                    else:
                                        st.write("N/A")
                                    
                                    if intervention.get('category'):
                                        st.markdown("**📂 Category:**")
                                        st.write(intervention.get('category'))
                                
                                with col_b:
                                    if intervention.get('road_type'):
                                        st.markdown("**🛣️ Suitable Road Types:**")
                                        road_types = intervention.get('road_type', [])
                                        if road_types:
                                            st.write(", ".join(road_types) if isinstance(road_types, list) else road_types)
                                    
                                    st.markdown("**📊 Technical Details:**")
                                    details = []
                                    if intervention.get('code'):
                                        details.append(f"**Code:** {intervention.get('code')}")
                                    if intervention.get('clause'):
                                        details.append(f"**Clause:** {intervention.get('clause')}")
                                    if intervention.get('S. No.'):
                                        details.append(f"**S. No.:** {intervention.get('S. No.')}")
                                    if intervention.get('intervention_id') and intervention.get('intervention_id') != 'N/A':
                                        details.append(f"**ID:** {intervention.get('intervention_id')}")
                                    details.append(f"**Similarity Score:** {intervention.get('similarity_score', 0):.3f}")
                                    
                                    for detail in details:
                                        st.write(f"- {detail}")
                                    
                                    if intervention.get('content'):
                                        with st.expander("📄 View full content"):
                                            st.write(intervention.get('content'))
                        
                        st.markdown("---")
                        st.subheader("🤖 AI-Powered Recommendation")
                        st.markdown('<div class="recommendation-box">', unsafe_allow_html=True)
                        st.markdown(result['recommendation'])
                        st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Export options
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            # Export as JSON
                            json_str = json.dumps(result, indent=2, ensure_ascii=False)
                            st.download_button(
                                label="📥 Download JSON",
                                data=json_str,
                                file_name=f"recommendation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                                mime="application/json"
                            )
                        with col2:
                            # Export as CSV
                            if result['retrieved_interventions']:
                                df = pd.DataFrame(result['retrieved_interventions'])
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download CSV",
                                    data=csv,
                                    file_name=f"recommendations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                                    mime="text/csv"
                                )
                        with col3:
                            # Copy to clipboard
                            if st.button("📋 Copy Results"):
                                st.success("Results copied! (Use Ctrl+V to paste)")
                        
                        # Query details
                        with st.expander("📊 Query Details"):
                            st.write(f"**Original Query:** {user_query}")
                            st.write(f"**Enhanced Query:** {full_query}")
                            st.write(f"**Interventions Retrieved:** {len(result['retrieved_interventions'])}")
                            st.write(f"**Processing Time:** {elapsed_time:.2f} seconds")
                            st.write(f"**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                    else:
                        st.warning("⚠️ No interventions found. Please try:")
                        st.markdown("""
                        - Rephrasing your query
                        - Uploading more intervention data
                        - Using different keywords
                        """)
                        st.info(result.get('recommendation', 'No recommendations available.'))
                        
                except Exception as e:
                    st.error(f"❌ Error generating recommendations: {str(e)}")
                    with st.expander("🔍 Error Details"):
                        st.exception(e)
        else:
            st.warning("⚠️ Please enter a road safety problem description")

# Tab 2: Database Info
with tab2:
    st.header("📚 Database Information")
    
    if hasattr(rag_system.pipeline, 'data') and rag_system.pipeline.data:
        st.metric("Total Interventions", len(rag_system.pipeline.data))
        
        # Statistics with visualizations
        col1, col2, col3 = st.columns(3)
        
        with col1:
            category_counts = {}
            for intervention in rag_system.pipeline.data:
                cat = intervention.get('category', 'Unknown')
                category_counts[cat] = category_counts.get(cat, 0) + 1
            st.markdown("**Category Distribution:**")
            for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {cat}: {count}")
        
        with col2:
            problem_counts = {}
            for intervention in rag_system.pipeline.data:
                problem = intervention.get('problem', '')
                if not problem:
                    problem_list = intervention.get('problem_type', [])
                    if problem_list:
                        problem = problem_list[0] if isinstance(problem_list, list) else problem_list
                if problem:
                    problem_counts[problem] = problem_counts.get(problem, 0) + 1
            st.markdown("**Problem Types:**")
            for prob, count in sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)[:10]:
                st.write(f"- {prob}: {count}")
            if len(problem_counts) > 10:
                st.write(f"... and {len(problem_counts) - 10} more")
        
        with col3:
            code_counts = {}
            for intervention in rag_system.pipeline.data:
                code = intervention.get('code', 'Unknown')
                code_counts[code] = code_counts.get(code, 0) + 1
            st.markdown("**Code Distribution:**")
            for code, count in sorted(code_counts.items(), key=lambda x: x[1], reverse=True):
                st.write(f"- {code}: {count}")
        
        st.markdown("---")
        st.subheader("📋 All Available Interventions")
        
        # Search/filter
        col1, col2 = st.columns([3, 1])
        with col1:
            search_term = st.text_input("🔍 Search interventions", placeholder="Search by name, problem type, or description")
        with col2:
            filter_category = st.selectbox("Filter by Category", ["All"] + list(set(i.get('category', '') for i in rag_system.pipeline.data if i.get('category'))))
        
        filtered_data = rag_system.pipeline.data
        if search_term:
            search_lower = search_term.lower()
            filtered_data = [
                i for i in filtered_data
                if (search_lower in (i.get('name') or i.get('type', '')).lower() or
                    search_lower in (i.get('description') or i.get('data', '')).lower() or
                    search_lower in (i.get('problem', '')).lower() or
                    search_lower in (i.get('category', '')).lower() or
                    any(search_lower in str(p).lower() for p in (i.get('problem_type', []) or [])))
            ]
        if filter_category != "All":
            filtered_data = [i for i in filtered_data if i.get('category') == filter_category]
        
        if search_term or filter_category != "All":
            st.info(f"Found {len(filtered_data)} intervention(s)")
        
        # Display with pagination
        items_per_page = 10
        total_pages = (len(filtered_data) - 1) // items_per_page + 1 if filtered_data else 1
        
        if total_pages > 1:
            page = st.number_input("Page", min_value=1, max_value=total_pages, value=1)
            start_idx = (page - 1) * items_per_page
            end_idx = start_idx + items_per_page
            display_data = filtered_data[start_idx:end_idx]
        else:
            display_data = filtered_data
        
        for intervention in display_data:
            name = intervention.get('name') or intervention.get('type', 'Unknown')
            intervention_id = intervention.get('intervention_id') or intervention.get('S. No.', 'N/A')
            with st.expander(
                f"**{name}** | ID: {intervention_id} | Category: {intervention.get('category', 'N/A')}"
            ):
                st.json(intervention)
        
        # Export database
        st.markdown("---")
        st.subheader("📥 Export Database")
        col1, col2 = st.columns(2)
        with col1:
            json_str = json.dumps(rag_system.pipeline.data, indent=2, ensure_ascii=False)
            st.download_button(
                label="📥 Download as JSON",
                data=json_str,
                file_name=f"interventions_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        with col2:
            df = pd.DataFrame(rag_system.pipeline.data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download as CSV",
                data=csv,
                file_name=f"interventions_database_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
    else:
        st.info("📤 Upload a JSON file with interventions to populate the database")

# Tab 3: Analytics
with tab3:
    st.header("📊 Analytics Dashboard")
    
    if hasattr(rag_system.pipeline, 'data') and rag_system.pipeline.data:
        # Category distribution chart
        category_counts = {}
        for intervention in rag_system.pipeline.data:
            cat = intervention.get('category', 'Unknown')
            category_counts[cat] = category_counts.get(cat, 0) + 1
        
        if category_counts:
            fig = px.pie(
                values=list(category_counts.values()),
                names=list(category_counts.keys()),
                title="Interventions by Category"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Problem type distribution
        problem_counts = {}
        for intervention in rag_system.pipeline.data:
            problem = intervention.get('problem', '')
            if not problem:
                problem_list = intervention.get('problem_type', [])
                if problem_list:
                    problem = problem_list[0] if isinstance(problem_list, list) else problem_list
            if problem:
                problem_counts[problem] = problem_counts.get(problem, 0) + 1
        
        if problem_counts:
            top_problems = dict(sorted(problem_counts.items(), key=lambda x: x[1], reverse=True)[:10])
            fig = px.bar(
                x=list(top_problems.keys()),
                y=list(top_problems.values()),
                title="Top 10 Problem Types",
                labels={'x': 'Problem Type', 'y': 'Count'}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, use_container_width=True)
        
        # Query history analytics
        if st.session_state.query_history:
            st.subheader("📈 Query History Analytics")
            st.write(f"**Total Queries:** {len(st.session_state.query_history)}")
            st.write("**Recent Queries:**")
            for i, query in enumerate(reversed(st.session_state.query_history[-10:]), 1):
                st.write(f"{i}. {query}")
    else:
        st.info("No data available for analytics. Please load interventions first.")

# Tab 4: About
with tab4:
    st.header("ℹ️ About This Application")
    st.markdown("""
    ### Road Safety Intervention GPT
    
    This application uses **Retrieval-Augmented Generation (RAG)** to provide AI-powered recommendations 
    for road safety interventions.
    
    #### How It Works:
    1. **Embedding Pipeline**: Uses sentence transformers to create vector embeddings of road safety interventions
    2. **Semantic Search**: Searches for relevant interventions based on your query using cosine similarity
    3. **Ollama Integration**: Uses Ollama LLM to generate contextual recommendations based on retrieved interventions
    
    #### Features:
    - 🔍 Semantic search for road safety interventions
    - 🤖 AI-powered recommendations using Ollama
    - 📊 Detailed intervention information
    - 📚 Database management and exploration
    - 📈 Analytics and visualizations
    - 📥 Export functionality
    - 📜 Query history
    
    #### Requirements:
    - Ollama installed and running (download from https://ollama.ai)
    - Ollama model (default: llama3.2:3b)
    
    #### Usage:
    1. Upload a JSON file with road safety interventions (or use the default interventions.json)
    2. Enter your road safety problem in the query system
    3. Get AI-powered recommendations based on relevant interventions
    
    #### Technology Stack:
    - **Streamlit**: Web interface
    - **Ollama**: Local LLM inference
    - **Sentence Transformers**: Embedding generation
    - **NumPy**: Vector similarity calculations
    - **Plotly**: Data visualizations
    - **Pandas**: Data manipulation
    
    #### Version:
    - **v2.0** - Enhanced production-ready version with analytics and export features
    """)
