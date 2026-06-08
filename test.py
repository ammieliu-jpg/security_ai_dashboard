# review.py
import requests

# ❌ 漏洞 1：硬編碼敏感憑證 (Hardcoded Secret) - 這是資安大忌！
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE_SECRET_KEY_12345"
DB_PASSWORD = "SuperSecurePassword123!"

def fetch_user_data(user_id):
    print(f"正在連線到資料庫，密碼為: {DB_PASSWORD}")
    
    # ❌ 漏洞 2：不安全的網路請求，沒有設定 timeout
    # 如果伺服器卡住，整個程式就會無限期掛起，容易遭受阻斷服務攻擊 (DoS)
    response = requests.get(f"https://api.example.com/users/{user_id}")
    return response.json()

if __name__ == "__main__":
    print("安全審查測試程式已啟動...")
    # 故意留下一行執行測試
    # data = fetch_user_data("admin")
