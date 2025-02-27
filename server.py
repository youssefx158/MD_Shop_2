import os
import json
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__, template_folder=".", static_folder=".")
app.secret_key = 'your_secret_key_here'

# Define required directories and files with their default content.
# For CSS files, we only create the file (content is set below in the file).
REQUIRED_DIRS = {
    'login': {
        'login.html': """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>تسجيل الدخول - MD Shop</title>
  <link rel="stylesheet" href="/login/login.css">
  <script src="/login/login.js" defer></script>
</head>
<body>
  <div class="container">
    <header>
      <h1 class="logo" tabindex="0">MD Shop</h1>
    </header>
    <div class="login-form">
      <h2>تسجيل الدخول</h2>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <div class="messages">
            {% for category, message in messages %}
              <p class="{{ category }}">{{ message }}</p>
            {% endfor %}
          </div>
        {% endif %}
      {% endwith %}
      <form action="/login" method="POST">
        <input type="email" name="email" placeholder="الايميل" required>
        <input type="password" name="password" placeholder="الباسورد" required>
        <button type="submit">دخول</button>
      </form>
      <p class="link">
        <a href="/register">إنشاء حساب جديد</a>
      </p>
    </div>
  </div>
</body>
</html>
""",
        'login.css': "",  # CSS file will be created empty for now.
        'login.js': """// تأثيرات بسيطة على صفحة تسجيل الدخول
document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.logo');
  logo.addEventListener('mouseover', () => {
    logo.style.transform = 'scale(1.1)';
  });
  logo.addEventListener('mouseout', () => {
    logo.style.transform = 'scale(1)';
  });
  logo.addEventListener('click', () => {
    logo.style.transform = 'rotate(360deg)';
    setTimeout(() => {
      logo.style.transform = 'rotate(0deg)';
    }, 300);
  });
});
"""
    },
    'register': {
        'register.html': """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>إنشاء حساب - MD Shop</title>
  <link rel="stylesheet" href="/register/register.css">
  <script src="/register/register.js" defer></script>
</head>
<body>
  <div class="container">
    <header>
      <h1 class="logo" tabindex="0">MD Shop</h1>
    </header>
    <div class="register-form">
      <h2>إنشاء حساب جديد</h2>
      {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
          <div class="messages">
            {% for category, message in messages %}
              <p class="{{ category }}">{{ message }}</p>
            {% endfor %}
          </div>
        {% endif %}
      {% endwith %}
      <form action="/register" method="POST">
        <input type="text" name="first_name" placeholder="الاسم الأول" required>
        <input type="text" name="last_name" placeholder="الاسم الثاني" required>
        <input type="tel" name="phone" placeholder="رقم الهاتف" required>
        <input type="email" name="email" placeholder="الايميل" required>
        <input type="password" name="password" placeholder="الباسورد" required>
        <input type="password" name="confirm_password" placeholder="تأكيد الباسورد" required>
        <button type="submit">إنشاء حساب</button>
      </form>
      <p class="link">
        <a href="/login">العودة لتسجيل الدخول</a>
      </p>
    </div>
  </div>
</body>
</html>
""",
        'register.css': "",  # CSS file will be created empty.
        'register.js': """// تأثيرات بسيطة على صفحة إنشاء الحساب
document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.logo');
  logo.addEventListener('mouseover', () => {
    logo.style.transform = 'scale(1.1)';
  });
  logo.addEventListener('mouseout', () => {
    logo.style.transform = 'scale(1)';
  });
  logo.addEventListener('click', () => {
    logo.style.transform = 'rotate(360deg)';
    setTimeout(() => {
      logo.style.transform = 'rotate(0deg)';
    }, 300);
  });
});
"""
    },
    'data': {
        'admin_accounts.json': json.dumps([
            {
                "email": "admin@example.com",
                "password": "admin123",
                "first_name": "Admin",
                "last_name": "User"
            }
        ], indent=4, ensure_ascii=False),
        'user_accounts.json': json.dumps([], indent=4, ensure_ascii=False)
    }
}

def ensure_files():
    # Check and create required directories and files.
    for folder, files in REQUIRED_DIRS.items():
        if not os.path.exists(folder):
            os.makedirs(folder)
            app.logger.info(f"Created missing folder: {folder}")
        for filename, content in files.items():
            filepath = os.path.join(folder, filename)
            if not os.path.exists(filepath):
                if filename.endswith('.css'):
                    with open(filepath, 'w', encoding='utf-8') as f:
                        # For CSS files, create an empty file.
                        f.write("")
                    app.logger.info(f"Created missing CSS file (empty): {filepath}")
                else:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(content)
                    app.logger.info(f"Created missing file: {filepath}")

@app.before_request
def before_request_func():
    ensure_files()

def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        app.logger.error(f"Error loading {filepath}: {e}")
        return None

def save_json(filepath, data):
    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        app.logger.error(f"Error saving {filepath}: {e}")

DATA_DIR = 'data'
ADMIN_ACCOUNTS_FILE = os.path.join(DATA_DIR, 'admin_accounts.json')
USER_ACCOUNTS_FILE = os.path.join(DATA_DIR, 'user_accounts.json')

def check_credentials(email, password):
    admin_accounts = load_json(ADMIN_ACCOUNTS_FILE)
    if admin_accounts:
        for account in admin_accounts:
            if account.get("email") == email and account.get("password") == password:
                return 'admin'
    user_accounts = load_json(USER_ACCOUNTS_FILE)
    if user_accounts:
        for account in user_accounts:
            if account.get("email") == email and account.get("password") == password:
                return 'user'
    return None

@app.route('/')
def index():
    return redirect(url_for('login_page'))

@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login/login.html")

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    role = check_credentials(email, password)
    if role == 'admin':
        return redirect(url_for('admin_dashboard'))
    elif role == 'user':
        return redirect(url_for('user_dashboard'))
    else:
        flash("بيانات الدخول غير صحيحة!", "error")
        return redirect(url_for('login_page'))

@app.route('/register', methods=['GET'])
def register_page():
    return render_template("register/register.html")

@app.route('/register', methods=['POST'])
def register():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    if password != confirm_password:
        flash("كلمتا المرور غير متطابقتين.", "error")
        return redirect(url_for('register_page'))

    user_accounts = load_json(USER_ACCOUNTS_FILE)
    if user_accounts is None:
        user_accounts = []
    for account in user_accounts:
        if account.get("email") == email:
            flash("هذا الايميل مستخدم مسبقاً.", "error")
            return redirect(url_for('register_page'))

    new_account = {
        "email": email,
        "password": password,
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone
    }
    user_accounts.append(new_account)
    save_json(USER_ACCOUNTS_FILE, user_accounts)
    flash("تم إنشاء الحساب بنجاح.", "success")
    return redirect(url_for('login_page'))

@app.route('/admin')
def admin_dashboard():
    return "<h1>صفحة الأدمن</h1><p>مرحبا بك في لوحة تحكم الأدمن.</p>"

@app.route('/user')
def user_dashboard():
    return "<h1>الصفحة الرئيسية للمستخدم</h1><p>مرحبا بك في الموقع.</p>"

if __name__ == '__main__':
    app.run(debug=True)