pipeline {
    agent any
    tools {
        // 讓 Jenkins 自動幫你載入剛剛設定的 Python3 環境
        python 'Python3'
    }
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('套件安裝') {
            steps {
                // 有了 Python 工具後，就能正常呼叫 pip 了
                sh 'pip install --upgrade google-generativeai'
            }
        }
        stage('Gemini AI 程式碼審查') {
            steps {
                sh 'python review.py'
            }
        }
    }
}
