import streamlit as st
import requests
import re

# 介面設定
st.set_page_config(page_title="Gemini AI 智慧安全審查系統", layout="wide")
st.title("🛡️ 智慧資安審查系統")

# 設定 Jenkins 連線資訊 (請確認你的 Jenkins 設定)
JENKINS_URL = "http://localhost:8080"
JOB_NAME = "security_project"
USER_NAME = "admin"
USER_PASSWORD = "password" 

def fetch_report_from_jenkins():
    """只負責抓取 Jenkins Console 並提取報告，不執行 AI 呼叫"""
    try:
        api_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"
        res = requests.get(api_url, auth=(USER_NAME, USER_PASSWORD), timeout=15)
        
        if res.status_code != 200:
            return f"❌ 無法連接 Jenkins，狀態碼: {res.status_code}", "ERROR"
        
        log_text = res.text
        
        # 暴力提取 JSON 中的 text 欄位內容
        # 邏輯：尋找 candidates，提取內部 text，並還原換行符號
        match = re.search(r'"text":\s*"(.*?)"', log_text, re.DOTALL)
        
        if match:
            report_content = match.group(1).replace('\\n', '\n').replace('\\"', '"')
            return report_content, "SUCCESS"
        else:
            return "❌ 在 Jenkins 日誌中找不到審查報告，請確認 Jenkins Build 是否成功。", "WARNING"
            
    except Exception as e:
        return f"❌ 系統連線異常: {str(e)}", "ERROR"

# 介面區
col1, col2 = st.columns([1, 3])

with col1:
    st.header("操作區")
    if st.button("🔄 同步 Jenkins 審查報告"):
        with st.spinner("正在同步..."):
            result, status = fetch_report_from_jenkins()
            if status == "SUCCESS":
                st.session_state['report'] = result
            else:
                st.error(result)

with col2:
    st.header("資安審查結果")
    if 'report' in st.session_state:
        st.markdown(st.session_state['report'])
    else:
        st.info("請點擊左側按鈕同步 Jenkins 的最新審查報告")
