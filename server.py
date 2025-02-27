import os
import json
from flask import Flask, request, redirect, url_for, flash, render_template_string

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # استبدل هذا بقيمة مفتاح سري قوي

# ملف لتخزين بيانات الحسابات بصيغة JSON في نفس المجلد
DATA_FILE = "accounts.json"
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)

def read_accounts():
    """قراءة بيانات الحسابات من ملف JSON"""
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print("Error reading accounts:", e)
        return []

def write_accounts(accounts):
    """كتابة بيانات الحسابات إلى ملف JSON"""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(accounts, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print("Error writing accounts:", e)

# قالب صفحة تسجيل الدخول مع تضمين الـ CSS والـ JS داخل الصفحة
login_template = """
<!DOCTYPE html>
<html lang="ar">
  <head>
    <meta charset="UTF-8">
    <title>تسجيل الدخول - MD Shop</title>
    <style>
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #87CEFA;
        margin: 0;
        padding: 0;
      }
      .container {
        width: 100%;
        max-width: 400px;
        margin: 100px auto;
        background: white;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
      }
      input {
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      button {
        width: 100%;
        padding: 10px;
        background: #1e3d59;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }
      button:hover {
        background: #16324f;
      }
      .messages {
        color: red;
        margin-bottom: 10px;
      }
      a { color: #1e3d59; text-decoration: none; }
      a:hover { text-decoration: underline; }
    </style>
    <script>
      // مثال على كود جافاسكريبت بسيط لتأثير الشعار
      document.addEventListener("DOMContentLoaded", () => {
        const logo = document.getElementById("logo");
        if(logo) {
          logo.addEventListener("click", () => {
            logo.style.transform = "scale(1.1)";
            setTimeout(() => { logo.style.transform = "scale(1)"; }, 300);
          });
        }
      });
    </script>
  </head>
  <body>
    <div class="container">
      <h1 id="logo" style="text-align:center;">MD Shop</h1>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <div class="messages">
          {% for category, message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
          </div>
        {% endif %}
      {% endwith %}
      <form action="/login" method="post">
        <input type="email" name="email" placeholder="الايميل" required>
        <input type="password" name="password" placeholder="الباسورد" required>
        <button type="submit">تسجيل الدخول</button>
      </form>
      <p style="text-align:center; margin-top:10px;"><a href="/register">إنشاء حساب جديد</a></p>
    </div>
  </body>
</html>
"""

# قالب صفحة إنشاء الحساب
register_template = """
<!DOCTYPE html>
<html lang="ar">
  <head>
    <meta charset="UTF-8">
    <title>إنشاء حساب - MD Shop</title>
    <style>
      body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: #87CEFA;
        margin: 0;
        padding: 0;
      }
      .container {
        width: 100%;
        max-width: 400px;
        margin: 50px auto;
        background: white;
        padding: 20px;
        box-shadow: 0 0 10px rgba(0,0,0,0.1);
      }
      input {
        width: 100%;
        padding: 10px;
        margin: 5px 0;
        border: 1px solid #ccc;
        border-radius: 4px;
      }
      button {
        width: 100%;
        padding: 10px;
        background: #1e3d59;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }
      button:hover {
        background: #16324f;
      }
      .messages {
        color: red;
        margin-bottom: 10px;
      }
      a { color: #1e3d59; text-decoration: none; }
      a:hover { text-decoration: underline; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1 style="text-align:center;">إنشاء حساب جديد</h1>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <div class="messages">
          {% for category, message in messages %}
            <p>{{ message }}</p>
          {% endfor %}
          </div>
        {% endif %}
      {% endwith %}
      <form action="/register" method="post">
        <input type="text" name="first_name" placeholder="الاسم الأول" required>
        <input type="text" name="last_name" placeholder="الاسم الأخير" required>
        <input type="tel" name="phone" placeholder="رقم الهاتف" required>
        <input type="email" name="email" placeholder="الايميل" required>
        <input type="password" name="password" placeholder="الباسورد" required>
        <input type="password" name="confirm_password" placeholder="تأكيد الباسورد" required>
        <button type="submit">إنشاء حساب</button>
      </form>
      <p style="text-align:center; margin-top:10px;"><a href="/login">العودة لتسجيل الدخول</a></p>
    </div>
  </body>
</html>
"""

# قالب صفحة لوحة التحكم
dashboard_template = """
<!DOCTYPE html>
<html lang="ar">
  <head>
    <meta charset="UTF-8">
    <title>لوحة التحكم - MD Shop</title>
    <style>
      body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f0f0f0; margin: 0; padding: 20px; }
      .container { max-width: 600px; margin: auto; background: white; padding: 20px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
      a { color: #1e3d59; text-decoration: none; }
      a:hover { text-decoration: underline; }
    </style>
  </head>
  <body>
    <div class="container">
      <h1>لوحة التحكم</h1>
      <p>مرحبا بك في لوحة التحكم!</p>
      <p><a href="/login">تسجيل خروج</a></p>
    </div>
  </body>
</html>
"""

@app.route("/")
def index():
    return redirect(url_for("login_page"))

@app.route("/login", methods=["GET"])
def login_page():
    return render_template_string(login_template)

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    accounts = read_accounts()
    found = False
    for account in accounts:
        if account.get("email") == email and account.get("password") == password:
            found = True
            break
    if found:
        flash("تم تسجيل الدخول بنجاح!", "success")
        return redirect(url_for("dashboard"))
    else:
        flash("بيانات الدخول غير صحيحة!", "error")
        return redirect(url_for("login_page"))

@app.route("/register", methods=["GET"])
def register_page():
    return render_template_string(register_template)

@app.route("/register", methods=["POST"])
def register():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    
    if password != confirm_password:
        flash("الباسورد وتأكيده غير متطابقين!", "error")
        return redirect(url_for("register_page"))
    
    accounts = read_accounts()
    for account in accounts:
        if account.get("email") == email:
            flash("الحساب بهذا الايميل موجود بالفعل!", "error")
            return redirect(url_for("register_page"))
    
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
    return redirect(url_for("login_page"))

@app.route("/dashboard")
def dashboard():
    return render_template_string(dashboard_template)

if __name__ == "__main__":
    # تأكد من تشغيل السيرفر من نفس المجلد الذي يتواجد فيه ملف server.py
    app.run(debug=True)