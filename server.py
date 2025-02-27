import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

# هنا احنا عايزين نربط كل ملفات التصميم والواجهات مع بعض
# هنا التطبيق بيستخدم مجلد "MD-Shop-2" كجذر للقوالب (templates) والملفات الثابتة (static)
# تأكد إن هيكل المشروع بالشكل ده:
# MD-Shop-2/
# ├── server.py
# ├── data/
# │     └── accounts.json
# ├── login/
# │     ├── login.html
# │     ├── login.css
# │     └── login.js
# └── register/
#       ├── register.html
#       ├── register.css
#       └── register.js

app = Flask(__name__, template_folder=".", static_folder=".")
app.secret_key = 'your_secret_key_here'

# التأكد من وجود مجلد data لتخزين معلومات الحسابات بصيغة JSON
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')

# إذا لم يكن ملف accounts.json موجوداً، ننشئ ملف فارغ يحتوي على قائمة فارغة
if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, 'w', encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

def read_accounts():
    """قراءة الحسابات من ملف JSON"""
    try:
        with open(ACCOUNTS_FILE, 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"خطأ عند قراءة الحسابات: {e}")
        return []

def write_accounts(accounts):
    """كتابة الحسابات في ملف JSON"""
    try:
        with open(ACCOUNTS_FILE, 'w', encoding="utf-8") as f:
            json.dump(accounts, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"خطأ عند كتابة الحسابات: {e}")

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    # تأكد إن ملف login/login.html موجود جوا مجلد MD-Shop-2
    return render_template('login/login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    accounts = read_accounts()
    found = False
    
    for account in accounts:
        if account.get("email") == email and account.get("password") == password:
            found = True
            break

    if found:
        flash("تم تسجيل الدخول بنجاح!", "success")
        return redirect(url_for('dashboard'))
    else:
        flash("بيانات الدخول غير صحيحة!", "error")
        return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    # هنا ممكن تضيف المزيد من تصميم لوحة التحكم حسب رغبتك
    return "<h1>لوحة التحكم</h1><p>مرحبا بك في لوحة التحكم!</p>"

@app.route('/register', methods=['GET'])
def register_page():
    # تأكد إن ملف register/register.html موجود جوا مجلد MD-Shop-2
    return render_template('register/register.html')

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("الباسورد وتأكيده غير متطابقين!", "error")
        return redirect(url_for('register_page'))
    
    accounts = read_accounts()
    for account in accounts:
        if account.get("email") == email:
            flash("الحساب بهذا الايميل مسجل مسبقاً!", "error")
            return redirect(url_for('register_page'))
    
    new_account = {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "email": email,
        "password": password
    }
    accounts.append(new_account)
    write_accounts(accounts)
    
    flash("تم إنشاء الحساب بنجاح!", "success")
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(debug=True)