pipeline {
    agent any
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('建立 Python 虛擬環境') {
            steps {
                sh '''
                    echo "=== 開始配置本地 Python 環境 ==="
                    # 在工作區內建立一個完全獨立的虛擬環境，不踩任何權限問題
                    python3 -m venv my_env || python -m venv my_env
                    
                    # 啟用虛擬環境並安裝套件
                    . my_env/bin/activate
                    pip install --upgrade pip
                    pip install google-generativeai
                '''
            }
        }
        stage('Gemini AI 程式碼審查') {
            steps {
                sh '''
                    . my_env/bin/activate
                    echo "=== 開始執行 Gemini AI 自動化審查 ==="
                    python review.py
                '''
            }
        }
    }
}
