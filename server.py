import os
import json
import shutil
from flask import Flask, request, redirect, send_from_directory

app = Flask(__name__, static_folder=os.getcwd())

# تعريف مسارات المجلدات الأساسية
BASE_DIR   = os.getcwd()
ADMIN_DIR  = os.path.join(BASE_DIR, "admin")
USER_DIR   = os.path.join(BASE_DIR, "user")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SERVER_DIR = os.path.join(BASE_DIR, "server")

# تعريف مسارات ملفات تخزين الحسابات في مجلد server
ADMIN_DATA_FILE = os.path.join(SERVER_DIR, "admin_accounts.json")
USER_DATA_FILE  = os.path.join(SERVER_DIR, "user_accounts.json")

# قائمة الملفات الأساسية المطلوبة مع موقعها المتوقع ومحتوى افتراضي (فارغ أو مع نص توضيحي بسيط)
REQUIRED_FILES = {
    os.path.join(ADMIN_DIR, "login.html"): """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>تسجيل دخول الأدمن - MD Shop</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="container">
    <h2>تسجيل دخول الأدمن</h2>
    <!-- محتوى صفحة تسجيل دخول الأدمن -->
  </div>
</body>
</html>
""",
    os.path.join(USER_DIR, "login.html"): """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>تسجيل الدخول - MD Shop</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="container">
    <h2>تسجيل الدخول</h2>
    <form action="/login" method="POST">
      <div class="form-group">
        <label for="email">الايميل</label>
        <input type="email" id="email" name="email" required>
      </div>
      <div class="form-group">
        <label for="password">كلمة المرور</label>
        <input type="password" id="password" name="password" required>
      </div>
      <button type="submit">دخول</button>
    </form>
    <p>لا تمتلك حساباً؟ <a href="signup.html">إنشاء حساب جديد</a></p>
  </div>
</body>
</html>
""",
    os.path.join(USER_DIR, "signup.html"): """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>إنشاء حساب - MD Shop</title>
  <link rel="stylesheet" href="../assets/common.css">
</head>
<body>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="container">
    <h2>إنشاء حساب جديد</h2>
    <form action="/signup" method="POST">
      <div class="form-group">
        <label for="firstName">الاسم الأول</label>
        <input type="text" id="firstName" name="firstName" required>
      </div>
      <div class="form-group">
        <label for="lastName">الاسم الثاني</label>
        <input type="text" id="lastName" name="lastName" required>
      </div>
      <div class="form-group">
        <label for="phone">رقم الهاتف</label>
        <input type="text" id="phone" name="phone" required>
      </div>
      <div class="form-group">
        <label for="email">الايميل</label>
        <input type="email" id="email" name="email" required>
      </div>
      <div class="form-group">
        <label for="password">كلمة المرور</label>
        <input type="password" id="password" name="password" required>
      </div>
      <div class="form-group">
        <label for="confirmPassword">تأكيد كلمة المرور</label>
        <input type="password" id="confirmPassword" name="confirmPassword" required>
      </div>
      <button type="submit">إنشاء حساب</button>
    </form>
    <p>لديك حساب بالفعل؟ <a href="login.html">العودة لتسجيل الدخول</a></p>
  </div>
</body>
</html>
"""
}

# الملف الخاص بالتصميم العام (يجب ربطه في جميع الصفحات)
COMMON_CSS_FILE = os.path.join(ASSETS_DIR, "common.css")

def ensure_directories():
    """التأكد من وجود المجلدات المطلوبة، وإن لم تكن موجودة يتم إنشاؤها."""
    for directory in [ADMIN_DIR, USER_DIR, ASSETS_DIR, SERVER_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"تم إنشاء المجلد: {directory}")

def ensure_files():
    """التأكد من وجود الملفات الأساسية في أماكنها المحددة، وإن لم تكن موجودة يتم إنشاؤها بمحتوى افتراضي."""
    # التأكد من ملفات الصفحات
    for filepath, content in REQUIRED_FILES.items():
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"تم إنشاء الملف: {filepath}")
    # التأكد من ملف التصميم العام (ننشئه فارغاً إن لم يكن موجوداً)
    if not os.path.exists(COMMON_CSS_FILE):
        with open(COMMON_CSS_FILE, "w", encoding="utf-8") as f:
            f.write("/* common.css - قم بتصميم الشكل العام هنا */\n")
        print(f"تم إنشاء ملف التصميم العام: {COMMON_CSS_FILE}")
        
def ensure_data_files():
    """التأكد من وجود ملفات تخزين الحسابات (للأدمن والمستخدمين)."""
    if not os.path.exists(ADMIN_DATA_FILE):
        with open(ADMIN_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"admins": []}, f, ensure_ascii=False, indent=4)
        print(f"تم إنشاء ملف بيانات الأدمن: {ADMIN_DATA_FILE}")
    if not os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump({"users": []}, f, ensure_ascii=False, indent=4)
        print(f"تم إنشاء ملف بيانات المستخدمين: {USER_DATA_FILE}")

def organize_files():
    """
    إذا وُجد ملفات في أماكن خاطئة، نقوم بنقلها إلى المكان الصحيح.
    هنا كمثال، إذا وُجد login.html في المجلد الأساسي بدلاً من مجلد user.
    """
    misplaced_files = {
        os.path.join(BASE_DIR, "login.html"): os.path.join(USER_DIR, "login.html"),
        os.path.join(BASE_DIR, "signup.html"): os.path.join(USER_DIR, "signup.html"),
        os.path.join(BASE_DIR, "admin_login.html"): os.path.join(ADMIN_DIR, "login.html")
    }
    for src, dest in misplaced_files.items():
        if os.path.exists(src):
            shutil.move(src, dest)
            print(f"تم نقل الملف من {src} إلى {dest}")

# استدعاء إجراءات التنظيم والتأكد عند بدء السيرفر
ensure_directories()
ensure_files()
ensure_data_files()
organize_files()

# دوال تحميل وتخزين الحسابات
def load_admin_accounts():
    with open(ADMIN_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_admin_accounts(data):
    with open(ADMIN_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_user_accounts():
    with open(USER_DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_accounts(data):
    with open(USER_DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    # إعادة التوجيه الافتراضية إلى صفحة تسجيل الدخول الخاصة بالمستخدمين
    return redirect("/user/login.html")

@app.route('/login', methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    # أولاً: التحقق من حسابات الأدمن
    admin_data = load_admin_accounts()
    for admin in admin_data.get("admins", []):
        if admin["email"] == email and admin["password"] == password:
            return "مرحباً أدمن، تم تسجيل الدخول بنجاح."
    # ثانيًا: التحقق من حسابات المستخدمين
    user_data = load_user_accounts()
    for user in user_data.get("users", []):
        if user["email"] == email and user["password"] == password:
            return "مرحباً مستخدم، تم تسجيل الدخول بنجاح."
    return "بيانات الاعتماد غير صحيحة", 401

@app.route('/signup', methods=["POST"])
def signup():
    firstName = request.form.get("firstName")
    lastName = request.form.get("lastName")
    phone = request.form.get("phone")
    email = request.form.get("email")
    password = request.form.get("password")
    confirmPassword = request.form.get("confirmPassword")
    
    if password != confirmPassword:
        return "كلمة المرور غير متطابقة", 400
    
    user_data = load_user_accounts()
    # التأكد من عدم تكرار الايميل في حسابات المستخدم
    for user in user_data.get("users", []):
        if user["email"] == email:
            return "الايميل مستخدم بالفعل", 400

    new_user = {
        "firstName": firstName,
        "lastName": lastName,
        "phone": phone,
        "email": email,
        "password": password  # للتنبيه: يجب تشفير كلمة المرور في الإنتاج
    }
    user_data.setdefault("users", []).append(new_user)
    save_user_accounts(user_data)
    return "تم إنشاء الحساب بنجاح", 200

# خدمة الملفات الثابتة لجميع الملفات في المشروع
@app.route('/<path:filename>')
def serve_file(filename):
    return send_from_directory(BASE_DIR, filename)

if __name__ == "__main__":
    app.run(debug=True)