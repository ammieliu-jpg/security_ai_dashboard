pipeline {
    agent any
    environment {
        // 這裡填入你之前在 Jenkins 設定的 Gemini API Key 憑證 ID
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('套件安裝') {
            steps {
                // 確保環境有安裝必要的套件
                sh 'pip install google-generativeai'
            }
        }
        stage('Gemini AI 程式碼審查') {
            steps {
                // 執行你寫好的 Python 審查腳本
                sh 'python review.py'
            }
        }
    }
}
