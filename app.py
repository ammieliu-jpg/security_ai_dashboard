import streamlit as st
import google.generativeai as genai
import requests
import re
import json

# 1. 網頁全螢幕設定與大標題
st.set_page_config(page_title="元宇宙資安自動化審查系統", layout="wide")
st.title("🛡️ 基於大語言模型之 Jenkins+SonarQube 智慧化安全審查主控台")
st.caption("結合 CI/CD 流程與 Gemini AI 的即時動態資安防禦平台")

# ====================================================================
# 🛠️ 核心設定：Jenkins 連線資訊 (免 Token 密碼直連版)
# ====================================================================
JENKINS_URL = "http://localhost:8080"
JOB_NAME = "security_project"
USER_NAME = "admin"
USER_PASSWORD = "admin"  # 👈 記得改成你登入 Jenkins 網頁的真實密碼

def fetch_jenkins_cicd_log():
    try:
        # API 直連 Jenkins 撈取最新建置的 Console 紀錄
        api_url = f"{JENKINS_URL}/job/{JOB_NAME}/lastBuild/consoleText"
        res = requests.get(api_url, auth=(USER_NAME, USER_PASSWORD), timeout=5)
        
        if res.status_code == 200:
            # 在 Log 文字中尋找符合 JSON 格式的 Gemini 回傳區塊
            json_match = re.search(r'\{.*"candidates".*\}', res.text, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group(0))
                # 拔出裡面的中文資安報告
                return data['candidates'][0]['content']['parts'][0]['text'], "SUCCESS"
            else:
                return "❌ 連線成功，但目前 Jenkins 最新建置的日誌裡沒有 Gemini JSON 報告。\n請確認 Jenkins 後台是否有跑完最新一輪建置。", "WARNING"
        elif res.status_code in [401, 403]:
            return "❌ Jenkins 帳號或密碼驗證失敗，請檢查程式碼中的 USER_PASSWORD 設定。", "ERROR"
        else:
            return f"❌ 無法連線至 Jenkins 伺服器 (狀態碼: {res.status_code})", "ERROR"
    except Exception as e:
        return f"❌ 無法與本地 Jenkins 建立安全連線: {e}", "ERROR"


# ====================================================================
# 🖥️ 畫面排版：左側邊欄 (Sidebar)
# ====================================================================
with st.sidebar:
    st.header("🔑 系統核心設定")
    # 原本的 API Key 輸入框
    user_api_key = st.text_input("輸入 Gemini API Key:", type="password", help="用於即時貼上程式碼分析時使用")
    st.info("提示：此金鑰用於即時驅動 Gemini AI 進行動態威脅建模與代碼重構。")
    
    st.markdown("---")
    st.markdown("### ⚙️ Jenkins 管線監控狀態")
    st.write(f"**目標專案：** `{JOB_NAME}`")
    st.write(f"**伺服器位址：** `{JENKINS_URL}`")
    st.write(f"**驗證模式：** `密碼認證直連`")


# ====================================================================
# 🖥️ 畫面排版：主畫面（左欄：程式碼輸入 / 右欄：AI 審查報告）
# ====================================================================
col1, col2 = st.columns([1, 1.2])  # 調整左右黃金比例

with col1:
    st.markdown("### 📊 CI/CD 程式碼輸入中心")
    # 原本的 Code Editor 文字輸入框
    default_code = """import os
def ping(ip):
    os.system('ping ' + ip)"""
    
    code_input = st.text_area(
        "請在下方貼上需要審查的程式碼（支援任何語言）：", 
        value=default_code, 
        height=350
    )

with col2:
    st.markdown("### 🤖 Gemini AI 智慧代碼審查助理")
    
    # 🌟 這裡就是最關鍵的雙分頁（Tabs）升級！
    tab1, tab2 = st.tabs(["💡 即時貼上代碼分析", "🔄 Jenkins CI/CD 管線同步"])
    
    # --- 頁籤 1：你原本就做好的現場貼、現場即時分析功能 ---
    with tab1:
        st.caption("💡 等待左側管線提交程式碼... 點擊下方按鈕後 AI 將當場進行動態分析。")
        if st.button("🚀 啟動 AI 智慧漏洞審查", key="local_review_btn"):
            if not user_api_key:
                st.error("請先在左側邊欄填入你的 Gemini API Key！")
            else:
                with st.spinner("AI 專家正在分析此段代碼..."):
                    try:
                        genai.configure(api_key=user_api_key)
                        model = genai.GenerativeModel('gemini-1.5-flash')
                        prompt = f"你是一位資安專家，請審查以下程式碼並用中文指出漏洞與修正建議：\n\n{code_input}"
                        response = model.generate_content(prompt)
                        st.success("現場分析完成！")
                        st.markdown(response.text)
                    except Exception as e:
                        st.error(f"分析失敗: {e}")
                        
    # --- 頁籤 2：全新加入的 Jenkins 遠端同步功能 ---
    with tab2:
        st.markdown("##### 🚀 整合運維端：撈取最新一次 GitHub 提交之自動化審查報告")
        
        # 畫出那個亮眼的藍色同步按鈕！
        if st.button("🔄 一鍵同步 Jenkins 遠端管線日誌", type="primary", key="jenkins_sync_btn"):
            with st.spinner("正在穿越 Docker 容器通道，向 Jenkins 伺服器同步數據中..."):
                report_content, log_status = fetch_jenkins_cicd_log()
                
            if log_status == "SUCCESS":
                st.success("✅ 數據同步完成！成功對接本地 Jenkins 自動化審查管線。")
                st.markdown(report_content)
            elif log_status == "WARNING":
                st.warning(report_content)
            else:
                st.error(report_content)
        else:
            st.info("💡 當前處於等待狀態。當 GitHub 有新 Commit 觸發 Jenkins 建置後，點擊上方按鈕即可在此同步視覺化安全報告。")
