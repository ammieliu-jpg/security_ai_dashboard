pipeline {
    agent any
    stages {
        stage('Gemini AI Security Review') {
            steps {
                script {
                    echo "=== 開始進行 Gemini AI 審查 ==="
                    // 這裡直接執行 curl，確保它一定會跑
                    sh "curl -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${GEMINI_API_KEY}' -H 'Content-Type: application/json' -d '{\"contents\":[{\"parts\":[{\"text\":\"請審查這段程式碼並回傳 JSON 格式報告: print(1)\"}]}]}'"
                    echo "=== 審查結束 ==="
                }
            }
        }
    }
}
