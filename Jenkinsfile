pipeline {
    agent any
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('Gemini AI 自動化漏洞審查') {
            steps {
                sh '''
                    echo "=== 開始讀取待審查程式碼 ==="
                    # 將 test.py 或你想審查的原始碼內容轉成 JSON 安全格式
                    # 如果你想審查特定檔案，可以把 test.py 改成你的目標檔案名稱
                    CODE_CONTENT=$(cat test.py | sed 's/"/\\\\"/g' | sed ':a;N;$!ba;s/\\n/\\\\n/g')
                    
                    echo "=== 正在發送請求至 Google Gemini API ==="
                    # 直接使用 curl 呼叫 Gemini 2.5 Flash 官方最新 API 端點
                    curl -X POST "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=${GEMINI_API_KEY}" \\
                         -H "Content-Type: application/json" \\
                         -d "{
                               \\"contents\\": [{
                                   \\"parts\\": [{
                                       \\"text\\": \\"你是一位專業的資安審查專家。請幫我審查以下這段 Python 程式碼，指出其中隱含的資安漏洞（例如 SQL Injection、硬編碼憑證等），並給出具體的修正建議。程式碼如下：\\\\n\\\\n${CODE_CONTENT}\\"
                                   }]
                               }]
                           }" > gemini_response.json

                    echo "=== Gemini AI 審查報告結果 ==="
                    # 將結果印出來，為了防止容器沒裝 jq，我們直接用 python 或純文字印出
                    cat gemini_response.json
                '''
            }
        }
    }
}
