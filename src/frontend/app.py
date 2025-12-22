import streamlit as st
from api_client import APIClient

# 設定
st.set_page_config(page_title="PharmaDoc Agent", layout="wide")
api = APIClient()  # 通信係をインスタンス化

st.title("💊 PharmaDoc Agent")

# Sidebar: システムステータス
with st.sidebar:
    st.header("System Status")
    if st.button("Check Connection"):
        status = api.check_health()
        if status.get("status") == "healthy":
            st.success(f"Connected! v{status.get('version')}")
        else:
            st.error("Connection Error")

# Main: ファイルアップロード
st.markdown("### Document Upload")
uploaded_file = st.file_uploader("Upload CIOMS/PDF Report", type=["pdf", "txt"])

if uploaded_file is not None:
    if st.button("Analyze Document"):
        with st.spinner("Uploading to AI Engine..."):
            # APIClientに丸投げ！詳細は知らなくていい
            result = api.upload_file(uploaded_file, uploaded_file.name)
            
            if result:
                st.success("Upload Complete!")
                st.json(result)  # 結果をJSONで綺麗に表示
            else:
                st.error("Upload Failed. Check backend logs.")