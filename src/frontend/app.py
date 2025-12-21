import streamlit as st
import requests

st.set_page_config(page_title="PharmaDoc Agent", layout="wide")
st.title("💊 副作用報告書 AI解析エージェント")

# 1. Set file uploader
# 1. ファイルアップローダーの設置
uploaded_file = st.file_uploader("Upload CIOMS/PDF Report", type=["pdf", "txt"])

# 2. Send to Backend when a file is uploaded
# 2. ファイルがアップロードされたら、Backendに送信する
if uploaded_file is not None:
    if st.button("Analyze Document"):
        with st.spinner("Uploading to Backend..."):
            try:
                # Prepare file data in Multipart
                # ファイルデータを準備 (Multipart形式)
                files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                
                # Send as POST request
                # POSTリクエストで送信 (endpointを /upload に)
                response = requests.post("http://backend:8000/upload", files=files)
                
                if response.status_code == 200:
                    st.success(f"Success! {response.json()}")
                else:
                    st.error(f"Failed: {response.status_code}")
                    
            except Exception as e:
                st.error(f"Connection Error: {e}")