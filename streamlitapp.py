import streamlit as st
import requests
import json
from typing import Dict, Any
import time
import os

# ── CONFIG ────────────────────────────────────────────────────────────────
API_BASE_URL = os.getenv("API_BASE_URL", "https://document-query-engine-ia2czk4njq-uc.a.run.app")
DEFAULT_TENANT_ID = os.getenv("DEFAULT_TENANT_ID", "d572f04c-0ce5-48c5-a644-b88b8f369936")

# GCP Authentication (if needed)
GCP_SERVICE_ACCOUNT_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")

# ── PAGE CONFIG ──────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Document Query Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #000000;
        text-align: center;
        margin-bottom: 2rem;
    }
    .query-box {
        background-color: #ffffff;
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #000000;
        margin: 1rem 0;
    }
    .response-box {
        background-color: #ffffff;
        color: #000000;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #333333;
        margin: 1rem 0;
    }
    .source-doc {
        background-color: #ffffff;
        color: #000000;
        padding: 1rem;
        border-radius: 8px;
        border-left: 3px solid #666666;
        margin: 0.5rem 0;
        font-size: 0.9rem;
    }
    .error-box {
        background-color: #ffffff;
        color: #000000;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #000000;
        margin: 1rem 0;
    }
    .metric-box {
        background-color: #ffffff;
        color: #000000;
        padding: 0.8rem;
        border-radius: 8px;
        text-align: center;
        margin: 0.5rem;
        border: 1px solid #cccccc;
    }
</style>
""", unsafe_allow_html=True)

# ── HELPER FUNCTIONS ─────────────────────────────────────────────────────
def get_auth_headers() -> Dict[str, str]:
    """Get authentication headers for API calls."""
    headers = {"Content-Type": "application/json"}
    
    # Add GCP authentication if service account key is provided
    if GCP_SERVICE_ACCOUNT_KEY:
        try:
            import google.auth
            import google.auth.transport.requests
            from google.oauth2 import service_account
            import json
            
            # Parse the service account key
            service_account_info = json.loads(GCP_SERVICE_ACCOUNT_KEY)
            credentials = service_account.Credentials.from_service_account_info(
                service_account_info,
                scopes=['https://www.googleapis.com/auth/cloud-platform']
            )
            
            # Get the access token
            auth_req = google.auth.transport.requests.Request()
            credentials.refresh(auth_req)
            
            headers["Authorization"] = f"Bearer {credentials.token}"
        except Exception as e:
            st.warning(f"Authentication setup failed: {str(e)}")
    
    return headers

def call_query_api(question: str, tenant_id: str) -> Dict[str, Any]:
    """Call the Document Query Engine API."""
    try:
        url = f"{API_BASE_URL}/query"
        payload = {
            "question": question,
            "tenant_id": tenant_id
        }
        
        headers = get_auth_headers()
        
        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=120  # Increased timeout to 2 minutes
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False, 
                "error": f"API Error {response.status_code}: {response.text}"
            }
            
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out after 2 minutes. Please try again with a simpler query."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Could not connect to the API. Please check your connection."}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error: {str(e)}"}

def check_api_health() -> Dict[str, Any]:
    """Check if the API is healthy."""
    try:
        url = f"{API_BASE_URL}/health"
        headers = get_auth_headers()
        response = requests.get(url, headers=headers, timeout=30)  # Increased from 10 to 30 seconds
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {"success": False, "error": f"Health check failed: {response.status_code}"}
            
    except Exception as e:
        return {"success": False, "error": f"Health check error: {str(e)}"}

# ── MAIN APP ─────────────────────────────────────────────────────────────
def main():
    # Header
    st.markdown('<div class="main-header">🔍 Document Query Engine</div>', unsafe_allow_html=True)
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Tenant ID (fixed for testing)
        tenant_id = st.text_input(
            "Tenant ID",
            value=DEFAULT_TENANT_ID,
            help="The tenant ID for data isolation",
            disabled=False  # Allow editing for testing different tenants
        )
        
        st.markdown("---")
        
        # API Health Check
        st.header("🏥 API Status")
        if st.button("Check API Health", type="secondary"):
            with st.spinner("Checking API health..."):
                health_result = check_api_health()
                
            if health_result["success"]:
                health_data = health_result["data"]
                st.success("✅ API is healthy!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f'<div class="metric-box"><strong>Status</strong><br>{health_data.get("status", "Unknown")}</div>', unsafe_allow_html=True)
                with col2:
                    st.markdown(f'<div class="metric-box"><strong>Database</strong><br>{health_data.get("database", "Unknown")}</div>', unsafe_allow_html=True)
                
                if "rows" in health_data:
                    st.info(f"📊 Database has {health_data['rows']} rows in view")
            else:
                st.error(f"❌ API Health Check Failed: {health_result['error']}")
        
        st.markdown("---")
        
        # Example Questions
        st.header("💡 Example Questions")
        example_questions = [
            "What is the 5-year roadmap?",
            "What are the financial projections for 2028?",
            "Tell me about TRICARE contracts",
            "What are the key milestones?",
            "What is the Digital Health Integration Partnership?",
            "What are the profit margins for different contracts?"
        ]
        
        for i, question in enumerate(example_questions):
            if st.button(f"📝 {question}", key=f"example_{i}"):
                st.session_state.example_question = question
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Ask a Question")
        
        # Use example question if selected
        default_question = st.session_state.get("example_question", "")
        
        question = st.text_area(
            "Enter your question about the documents:",
            value=default_question,
            height=100,
            placeholder="e.g., What are the key financial milestones in the 5-year plan?"
        )
        
        # Clear example question after use
        if "example_question" in st.session_state:
            del st.session_state.example_question
        
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 2])
        
        with col_btn1:
            query_button = st.button("🔍 Query Documents", type="primary", use_container_width=True)
        
        with col_btn2:
            clear_button = st.button("🗑️ Clear", use_container_width=True)
        
        if clear_button:
            st.rerun()
    
    with col2:
        st.header("📊 Query Stats")
        
        # Initialize session state for stats
        if "query_count" not in st.session_state:
            st.session_state.query_count = 0
        if "total_response_time" not in st.session_state:
            st.session_state.total_response_time = 0
        
        # Display stats
        avg_time = (st.session_state.total_response_time / st.session_state.query_count) if st.session_state.query_count > 0 else 0
        
        st.metric("Total Queries", st.session_state.query_count)
        st.metric("Avg Response Time", f"{avg_time:.2f}s")
        st.metric("Current Tenant", tenant_id[:8] + "..." if len(tenant_id) > 8 else tenant_id)
    
    # Process query
    if query_button and question.strip():
        if not tenant_id.strip():
            st.error("❌ Tenant ID is required!")
            return
            
        st.markdown(f'<div class="query-box"><strong>🔍 Query:</strong> {question}</div>', unsafe_allow_html=True)
        
        # Make API call
        with st.spinner("🔄 Searching documents..."):
            start_time = time.time()
            result = call_query_api(question, tenant_id)
            response_time = time.time() - start_time
        
        # Update stats
        st.session_state.query_count += 1
        st.session_state.total_response_time += response_time
        
        if result["success"]:
            data = result["data"]
            answer = data.get("answer", "No answer provided")
            source_docs = data.get("source_documents", [])
            
            # Display response
            st.markdown(f'<div class="response-box"><strong>💡 Answer:</strong><br><br>{answer}</div>', unsafe_allow_html=True)
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Response Time", f"{response_time:.2f}s")
            with col2:
                st.metric("Source Documents", len(source_docs))
            with col3:
                st.metric("Answer Length", f"{len(answer)} chars")
            
            # Display source documents
            if source_docs:
                st.markdown("---")
                st.header("📚 Source Documents")
                
                for i, doc in enumerate(source_docs):
                    with st.expander(f"📄 Document {i+1} (ID: {doc.get('metadata', {}).get('document_id', 'Unknown')[:8]}...)"):
                        st.markdown(f'<div class="source-doc">{doc.get("text", "No text available")}</div>', unsafe_allow_html=True)
                        
                        # Show metadata
                        metadata = doc.get("metadata", {})
                        if metadata:
                            st.json(metadata)
            else:
                st.warning("📭 No source documents found for this query.")
                
        else:
            st.markdown(f'<div class="error-box"><strong>❌ Error:</strong><br>{result["error"]}</div>', unsafe_allow_html=True)
    
    elif query_button and not question.strip():
        st.warning("⚠️ Please enter a question before querying.")
    
    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; color: #666; font-size: 0.9rem;">
            🔍 Document Query Engine with Vector Search | 
            🔒 Multi-Tenant Secure | 
            ⚡ Powered by OpenAI + Gemini 2.5 Flash
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 