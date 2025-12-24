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

# 3. Handle new user input
if prompt := st.chat_input("Ask a question about the PDF..."):
    
    # A. Display and store user input
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # B. Display AI response (Streaming)
    with st.chat_message("assistant"):
        # st.write_stream consumes the generator and renders chunks in real-time.
        # It returns the complete string once the stream finishes.
        response_generator = api.chat_stream(prompt)
        full_response = st.write_stream(response_generator)
    
    # C. Save the full response to history
    # This is necessary to persist the conversation after a Streamlit rerun.
    st.session_state.messages.append({"role": "assistant", "content": full_response})