pipeline {
    agent any
    stages {
        stage('Gemini AI Security Review') {
            steps {
                script {
                    echo "=== 開始進行 Gemini AI 審查 ==="
                    
                    // 這裡透過 credentialsId 來安全讀取你設定好的 API Key
                    // 請確認你在 Jenkins Credentials 建立的 ID 是 "gemini-api-key"
                    withCredentials([string(credentialsId: 'gemini-api-key', variable: 'API_KEY')]) {
                        sh """
                        curl -X POST 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}' \
                        -H 'Content-Type: application/json' \
                        -d '{"contents":[{"parts":[{"text":"請審查這段程式碼並回傳 JSON 格式報告: print(1)"}]}]}'
                        """
                    }
                }
            }
        }
    }
}
