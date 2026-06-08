pipeline {
    // 讓 Jenkins 直接在內建支援的 python 輕量化 container 裡執行
    agent {
        docker { 
            image 'python:3.10-alpine' 
        }
    }
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('安裝 Gemini 審查套件') {
            steps {
                // 這個映像檔自帶最新版的 pip，不需要 sudo 權限即可直接安裝
                sh 'pip install --upgrade google-generativeai'
            }
        }
        stage('Gemini AI 程式碼審查') {
            steps {
                // 自帶 python 環境，直接執行你的腳本
                sh 'python review.py'
            }
        }
    }
}
