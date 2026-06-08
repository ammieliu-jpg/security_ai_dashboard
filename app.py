import streamlit as st
import requests
import re
import json

# 1. 設定網頁標題與寬版佈局
st.set_page_config(page_title="元宇宙資安自動化審查系統", layout="wide")
st.title("🛡️ AI 在元宇宙安全與隱私保護中的應用")
st.subheader("CI/CD 管線自動化資安審查儀表板")

# ====================================================================
# 🛠️ 請填入你的 Jenkins 連線資訊
# ====================================================================
JENKINS_URL = "http://localhost:8080"
JOB_NAME = "security_project"
USER_NAME = "admin"
USER_PASSWORD = "admin"  # 👈 請改成你登入 Jenkins 的真實密碼

def get_jenkins_latest_report():
    try:
        # 呼叫 Jenkins API 撈取最新一次建置的 Console 日誌
        api_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"
        response = requests.get(api_url, auth=(USER_NAME, USER_PASSWORD), timeout=10)
        
        if response.status_code == 200:
            log_text = response.text
            # 用正則表達式抓取日誌裡的 Gemini JSON 區塊
            json_match = re.search(r'\{.*"candidates".*\}', log_text, re.DOTALL)
            
            if json_match:
                raw_json = json_match.group(0)
                data = json.loads(raw_json)
                report_text = data['candidates'][0]['content']['parts'][0]['text']
                return report_text, "SUCCESS"
            else:
                return "❌ 連線成功，但無法在 Jenkins 日誌中解析出 Gemini JSON 報告。\n請確認 Jenkins 最新一次建置是否成功。", "WARNING"
        elif response.status_code in [401, 403]:
            return "❌ Jenkins 帳號或密碼錯誤！請檢查程式碼中的 USER_PASSWORD。", "ERROR"
        else:
            return f"❌ 無法連線至 Jenkins API (狀態碼: {response.status_code})", "ERROR"
    except Exception as e:
        return f"❌ 連線失敗，請確認 Jenkins 服務是否開啟: {e}", "ERROR"

# ====================================================================
# 🖥️ 畫面排版：這段才會把「左邊控制台 + 按鈕」做出來！
# ====================================================================
st.markdown("---")

# 建立左右兩欄 (比例 1:2)
col1, col2 = st.columns([1, 2])

with col1:
    st.info("### ⚙️ CI/CD 管線監控狀態")
    st.write(f"**目標專案 (Job)：** `{JOB_NAME}`")
    st.write(f"**Jenkins 伺服器：** `{JENKINS_URL}`")
    st.write(f"**驗證模式：** `Basic Auth (密碼直連)`")
    
    st.markdown(" ")
    # 🌟 關鍵：這行就是把「同步按鈕」畫在左邊欄位！
    if st.button("🔄 同步 Jenkins 最新審查報告", type="primary"):
        st.toast("正在從 Jenkins 遠端伺服器撈取最新數據...")
        # 點擊按鈕時，Streamlit 會自動重新載入並觸發下方的 get_jenkins_latest_report()

with col2:
    st.markdown("### 🤖 同步自 Jenkins 的 AI 漏洞審查報告")
    
    # 轉圈圈動畫
    with st.spinner("正在安全同步中..."):
        report, status = get_jenkins_latest_report()
        
    if status == "SUCCESS":
        st.success("✅ 成功對接 Jenkins CI/CD 管線！最新安全報告已同步。")
        st.markdown(report)
    elif status == "WARNING":
        st.warning(report)
    else:
        st.error(report)
