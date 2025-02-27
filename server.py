import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

# إعداد التطبيق لاستخدام مجلد "MD-Shop-2" كقاعدة للملفات الثابتة والقوالب
app = Flask(__name__, template_folder="MD-Shop-2", static_folder="MD-Shop-2")
app.secret_key = 'your_secret_key_here'

# التأكد من وجود مجلد data لتخزين معلومات الحسابات
DATA_DIR = 'data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
ACCOUNTS_FILE = os.path.join(DATA_DIR, 'accounts.json')

# في حال عدم وجود ملف accounts.json، نقوم بإنشاء ملف JSON فارغ (قائمة فارغة)
if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, 'w', encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

def read_accounts():
    """قراءة الحسابات من ملف JSON"""
    with open(ACCOUNTS_FILE, 'r', encoding="utf-8") as f:
        return json.load(f)

def write_accounts(accounts):
    """كتابة الحسابات إلى ملف JSON"""
    with open(ACCOUNTS_FILE, 'w', encoding="utf-8") as f:
        json.dump(accounts, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login/login.html')

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    accounts = read_accounts()
    found = False

    # التحقق من وجود الحساب من خلال ملف JSON
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
    return "<h1>لوحة التحكم</h1><p>مرحبا بك!</p>"

@app.route('/register', methods=['GET'])
def register_page():
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
    # التأكد من عدم وجود ايميل مسجل مسبقاً
    for account in accounts:
        if account.get("email") == email:
            flash("الحساب بهذا الايميل موجود بالفعل!", "error")
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