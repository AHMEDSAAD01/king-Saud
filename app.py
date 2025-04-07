import flask
from flask import Flask, render_template, request, redirect
import datetime
import os

app = Flask(__name__)

# بيانات المستخدم للتجربة
VALID_USERNAME = "admin"
VALID_PASSWORD = "1234"

# مسار ملف اللوج
LOG_FILE = "logs/login_attempts.log"

# عدد المحاولات المسموحة
MAX_FAILED_ATTEMPTS = 3

# عداد فشل (بسيط بدون قواعد بيانات)
failed_attempts = {}

def log_attempt(username, status):
    time = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    log_entry = f"{time} user: {username} - {status}\n"
    
    with open(LOG_FILE, "a") as log:
        log.write(log_entry)

@app.route("/", methods=["GET", "POST"])
def login():
    global failed_attempts

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # تحقق هل المستخدم موقوف مؤقتًا؟
        if failed_attempts.get(username, 0) >= MAX_FAILED_ATTEMPTS:
            return "🚫 Account temporarily locked due to multiple failed attempts."

        # تحقق من صحة البيانات
        if username == VALID_USERNAME and password == VALID_PASSWORD:
            log_attempt(username, "SUCCESS")
            failed_attempts[username] = 0  # إعادة تعيين العداد
            return "✅ Login successful!"
        else:
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            log_attempt(username, "FAILED")
            return "❌ Incorrect credentials. Try again."

    return render_template("login.html")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # احصل على المنفذ من البيئة إذا كان موجودًا
    app.run(host="0.0.0.0", port=port, debug=True)
