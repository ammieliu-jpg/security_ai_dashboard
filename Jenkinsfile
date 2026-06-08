pipeline {
    agent any
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('初始化 Python 環境') {
            steps {
                // 1. 探查 Jenkins 容器是哪種 Linux 並安裝 Python3 與 pip
                sh '''
                    if command -v apk >/dev/null 2>&1; then
                        echo "偵測到 Alpine 環境，開始安裝 python3..."
                        apk update && apk add --no-cache python3 py3-pip
                    elif command -v apt-get >/dev/null 2>&1; then
                        echo "偵測到 Debian/Ubuntu 環境，開始安裝 python3..."
                        sudo apt-get update && sudo apt-get install -y python3 python3-pip
                    else
                        echo "無法辨識的系統，嘗試直接呼叫環境..."
                    fi
                '''
            }
        }
        stage('安裝 Gemini 套件') {
            steps {
                // 2. 使用剛剛裝好的 pip 建立核心依賴
                sh 'pip3 install --break-system-packages google-generativeai || pip install google-generativeai'
            }
        }
        stage('Gemini AI 程式碼審查') {
            steps {
                // 3. 執行你的審查腳本
                sh 'python3 review.py || python review.py'
            }
        }
    }
}
