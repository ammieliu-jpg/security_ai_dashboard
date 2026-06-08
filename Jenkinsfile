pipeline {
    agent any
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('Gemini AI 程式碼審查') {
            steps {
                // 現在容器裡直接有 python3 指令了，而且連帶吃得到你本機裝好的 google-generativeai 套件！
                sh 'python3 review.py'
            }
        }
    }
}
