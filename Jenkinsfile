pipeline {
    // 關鍵：這行指令會強制 Jenkins 離開隔離的 Docker 容器，直接在你本機電腦執行
    agent { label 'built-in' }
    
    environment {
        GEMINI_API_KEY = credentials('gemini-api-key-id')
    }
    stages {
        stage('Gemini AI 程式碼審查') {
            steps {
                // 因為回到了你打得開網頁的本機環境，這裡直接呼叫 python3 就絕對找得到了！
                sh 'python3 review.py'
            }
        }
    }
}
