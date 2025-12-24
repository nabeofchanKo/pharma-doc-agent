import streamlit as st
from api_client import APIClient

# Configuration
st.set_page_config(page_title="PharmaDoc Agent", layout="wide")
api = APIClient()  # Instantiate the communication handler

st.title("💊 PharmaDoc Agent")

# Sidebar: system status
with st.sidebar:
    st.header("System Status")
    if st.button("Check Connection"):
        status = api.check_health()
        if status.get("status") == "healthy":
            st.success(f"Connected! v{status.get('version')}")
        else:
            st.error("Connection Error")

# Main: file upload
st.markdown("### Document Upload")
uploaded_file = st.file_uploader("Upload CIOMS/PDF Report", type=["pdf", "txt"])

if uploaded_file is not None:
    if st.button("Analyze Document"):
        with st.spinner("Uploading to AI Engine..."):
            # Delegate everything to the API client — no need to know the details here
            result = api.upload_file(uploaded_file, uploaded_file.name)
            
            if result:
                st.success("Upload Complete!")
                st.json(result)  # Display results neatly in JSON format
            else:
                st.error("Upload Failed. Check backend logs.")

# --- Chat Interface ---
st.markdown("---")
st.header("💬 Chat with your Document")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the PDF..."):
    
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.spinner("AI is thinking..."):
        response = api.chat(prompt)

    if response:
        ai_content = response.get("response", "Error: No response")
        
        with st.chat_message("assistant"):
            st.markdown(ai_content)
            
            if response.get("context"):
                with st.expander("Reference Context"):
                    for doc in response["context"]:
                        st.info(doc)

        st.session_state.messages.append({"role": "assistant", "content": ai_content})
    else:
        st.error("Failed to get response from backend.")