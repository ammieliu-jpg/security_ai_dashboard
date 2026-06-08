import streamlit as st
import requests
import re
import json

# 設定網頁標題與寬版佈局
st.set_page_config(page_title="元宇宙資安自動化審查系統", layout="wide")
st.title("🛡️ AI 在元宇宙安全與隱私保護中的應用")
st.subheader("CI/CD 管線自動化資安審查儀表板")

# ====================================================================
# 🛠️ 填入你的 Jenkins 連線資訊 (免 Token 密碼直連版)
# ====================================================================
JENKINS_URL = "http://localhost:8080"
JOB_NAME = "security_project"
USER_NAME = "admin"
# 👈 請在這裡直接填入你登入 Jenkins 網頁時使用的實體密碼
USER_PASSWORD = "admin" 

def get_jenkins_latest_report():
    try:
        # 使用 /lastBuild/consoleText API 取得最新一次建置（#15）的主控台純文字日誌
        api_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"
        
        # auth 參數直接傳入 (帳號, 密碼)，Jenkins 就會自動放行
        response = requests.get(api_url, auth=(USER_NAME, USER_PASSWORD), timeout=10)
        
        if response.status_code == 200:
            log_text = response.text
            
            # 使用正則表達式，在密密麻麻的日誌中，精準抓取符合 JSON 格式的 Gemini 回應區塊
            json_match = re.search(r'\{.*"candidates".*\}', log_text, re.DOTALL)
            
            if json_match:
                raw_json = json_match.group(0)
                data = json.loads(raw_json)
                
                # 提取出 Gemini 的中文報告內文
                report_text = data['candidates'][0]['content']['parts'][0]['text']
                return report_text, "SUCCESS"
            else:
                return "❌ 連線成功，但無法在 Jenkins 日誌中解析出 Gemini JSON 報告。\n請確認 Jenkins 最新一次建置是否成功產出報告。", "WARNING"
        elif response.status_code == 401 or response.status_code == 403:
            return "❌ 帳號或密碼錯誤！請檢查 USER_PASSWORD 是否填寫正確。", "ERROR"
        else:
            return f"❌ 無法連線至 Jenkins API (狀態碼: {response.status_code})", "ERROR"
            
    except requests.exceptions.ConnectionError:
        return "❌ 連線失敗！請確認您的 Jenkins 服務（localhost:8080）是否有正常開啟。", "ERROR"
    except Exception as e:
        return f"❌ 發生未知錯誤: {e}", "ERROR"

# ====================================================================
# 🖥️ Streamlit 網頁前端 UI 排版
# ====================================================================
st.markdown("---")

# 切分左右兩欄：左邊放控制台，右邊放壯觀的 AI 報告
col1, col2 = st.columns([1, 2])

with col1:
    st.info("### ⚙️ CI/CD 管線監控狀態")
    st.write(f"**目標專案 (Job)：** `{JOB_NAME}`")
    st.write(f"**Jenkins 伺服器：** `{JENKINS_URL}`")
    st.write(f"**驗證模式：** `Basic Auth (帳號密碼直連)`")
    
    st.markdown(" ")
    # 點擊按鈕手動強制同步最新狀況
    if st.button("🔄 同步 Jenkins 最新審查報告", type="primary"):
        st.toast("正在從 Jenkins 撈取最新數據...")

with col2:
    st.markdown("### 🤖 同步自 Jenkins 的 AI 漏洞審查報告")
    
    # 網頁載入時自動去撈取 Jenkins 資料
    with st.spinner("正在從 Jenkins 遠端伺服器安全同步數據中..."):
        report, status = get_jenkins_latest_report()
        
    if status == "SUCCESS":
        st.success("✅ 成功對接 Jenkins CI/CD 管線！最新安全報告已同步。")
        # Markdown 會自動把 \n 與 ** 轉換成漂亮的標題、粗體與清單，畫面會變得超級精美！
        st.markdown(report)
    elif status == "WARNING":
        st.warning(report)
    else:
        st.error(report)
