import streamlit as st
import google.generativeai as genai

# ==========================================
# 1. 初始化與網頁基本設定
# ==========================================
st.set_page_config(page_title="Gemini AI 智慧安全審查系統", layout="wide")

st.title("🛡️ 基於大語言模型之 Jenkins+SonarQube 智慧化安全審查主控台")
st.caption("結合 CI/CD 流程與 Gemini AI 的即時動態資安防禦平台")
st.write("---")

# 在網頁側邊欄讓使用者輸入金鑰，或是你們可以直接寫死在程式碼中方便上台展示
# 註：上台前可以先去 Google AI Studio 申請免費的 API 金鑰
with st.sidebar:
    st.header("🔑 系統核心設定")
    api_key = st.text_input("輸入 Gemini API Key：", type="password", value="")
    st.info("提示：此金鑰用於即時驅動 Gemini AI 進行動態威脅建模與代碼重構。")

# ==========================================
# 2. 網頁版面配置 (1:1.5 左右分欄)
# ==========================================
col1, col2 = st.columns([1.2, 1.8])

with col1:
    st.header("📊 CI/CD 程式碼輸入中心")
    st.write("請在下方貼上需要審查的程式碼（支援任何語言）：")
    
    # 讓使用者當場輸入或貼上程式碼的大框框
    user_code = st.text_area(
        "Code Editor", 
        height=400, 
        placeholder="例如貼上：\nimport os\ndef ping(ip):\n    os.system('ping ' + ip)"
    )
    
    # 送出審查的按鈕
    analyze_button = st.button("🚀 啟動 AI 智慧漏洞審查", use_container_width=True)

with col2:
    st.header("🤖 Gemini AI 智慧代碼審查助理")
    
    # 當使用者點擊按鈕時，觸發活的 AI 分析邏輯
    if analyze_button:
        if not api_key:
            st.warning("⚠️ 請先在左側欄位輸入 Gemini API Key 才能啟動即時動態分析。")
        elif not user_code.strip():
            st.warning("⚠️ 請先在左側輸入或貼上任何程式碼。")
        else:
            with st.spinner("🔄 Gemini AI 正在深入分析程式碼架構、進行威脅建模..."):
                try:
                    # 設定 Gemini API
                    genai.configure(api_key=api_key)
                    
                    # 使用最新的 gemini-1.5-flash 模型（速度最快，適合上台展示）
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # 這是我們下給 Gemini 的終極 Prompt 密技，強迫它吐出 Android Studio 風格的格式
                    prompt = f"""
                    你現在是一個資深的企業級 DevSecOps 安全專家與高階程式碼審查員。
                    請針對以下使用者提供的程式碼進行深度的漏洞掃描與分析：
                    
                    ```
                    {user_code}
                    ```
                    
                    請嚴格按照以下繁體中文格式進行回覆，確保結構清晰，適合呈現在網頁 Dashboard 上：
                    
                    ### 🎯 綜合安全漏洞評等
                    [請評估此程式碼的危險程度：極高/高/中/低，並給予一句總結]
                    
                    ---
                    
                    ### 📌 偵測到的致命缺陷與資安風險
                    * **錯誤成因：** [簡短且直白地說明這個程式碼哪裡寫錯了，黑客會怎麼攻擊]
                    
                    ---
                    
                    ### 🛠️ Android Studio 風格：建議修改對照表
                    
                    ❌ **原始不安全程式碼：**
                    ```
                    [撈出原本最危險的那一兩行程式碼]
                    ```
                    
                    ✅ **AI 建議重構程式碼：**
                    ```
                    [請直接給出修改好、最安全、最標準的程式碼，並加上註解說明原因]
                    ```
                    """
                    
                    # 呼叫模型生成回應
                    response = model.generate_content(prompt)
                    
                    # 將活的 AI 回應直接渲染到網頁右側
                    st.success("✨ AI 審查完成！報告已即時生成：")
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"❌ 呼叫 Gemini API 時發生錯誤: {e}")
    else:
        st.write("💡 等待左側管線提交程式碼... 點擊按鈕後 AI 將當場進行動態分析。")
