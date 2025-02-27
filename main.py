import os
import shutil
import json
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

def ensure_file(required_path):
    """
    يتأكد من وجود الملف في المسار المطلوب.
    إذا وُجد الملف في مسار آخر داخل المشروع فيتم نقله.
    وإذا لم يكن موجودًا، يتم إنشاؤه كملف فارغ.
    """
    directory = os.path.dirname(required_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    if os.path.exists(required_path):
        return

    found_path = None
    for root, dirs, files in os.walk("."):
        if any(part.startswith('.') for part in root.split(os.sep)) or "venv" in root:
            continue
        for file in files:
            if file == os.path.basename(required_path):
                current_path = os.path.join(root, file)
                if os.path.abspath(current_path) != os.path.abspath(required_path):
                    found_path = current_path
                    break
        if found_path:
            break

    if found_path:
        shutil.move(found_path, required_path)
    else:
        with open(required_path, "w", encoding="utf-8") as f:
            pass

def setup_project_structure():
    """
    ينشئ هيكل المشروع المطلوب مع التأكد من وجود الملفات بأماكنها.
    """
    required_files = [
        # ملفات البيانات
        "data/admin.json",
        "data/members.json",
        # صفحة تسجيل الدخول
        "pages/login/login.html",
        "pages/login/login.css",
        "pages/login/login.js",
        # صفحة إنشاء الحساب
        "pages/register/register.html",
        "pages/register/register.css",
        "pages/register/register.js",
        # صفحة الأدمن
        "pages/admin/admin.html",
        "pages/admin/admin.css",
        "pages/admin/admin.js",
        # صفحة المستخدم
        "pages/user/user.html",
        "pages/user/user.css",
        "pages/user/user.js"
    ]
    for path in required_files:
        ensure_file(path)

# التأكد من هيكل المشروع
setup_project_structure()

app = Flask(__name__, template_folder="pages")
app.secret_key = "سري جداً"  # غير المفتاح في الإنتاج

# لتقديم ملفات الصفحات مثل CSS و JS من داخل مجلد pages
@app.route("/pages/<path:filename>")
def pages_files(filename):
    return send_from_directory("pages", filename)

# مسارات ملفات البيانات
ADMIN_DATA = "data/admin.json"
MEMBER_DATA = "data/members.json"

def load_data(filepath):
    if not os.path.exists(filepath):
        return []
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_data(filepath, data):
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

@app.route("/")
def home():
    return render_template("login/login.html")

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    admins = load_data(ADMIN_DATA)
    for admin in admins:
        if admin.get("username") == username and admin.get("password") == password:
            return redirect(url_for("admin_page"))

    members = load_data(MEMBER_DATA)
    for member in members:
        if member.get("username") == username:
            if member.get("password") == password:
                return redirect(url_for("user_page"))
            else:
                flash("كلمة المرور غير صحيحة.")
                return redirect(url_for("home"))
    
    if username and password:
        new_member = {"username": username, "password": password}
        members.append(new_member)
        save_data(MEMBER_DATA, members)
        flash("تم تسجيل حساب جديد بنجاح")
        return redirect(url_for("user_page"))
    
    flash("يرجى إدخال معلومات صحيحة.")
    return redirect(url_for("home"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()
        phone = request.form.get("phone", "").strip()
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm_password", "").strip()

        if password != confirm_password:
            flash("كلمة المرور وتأكيدها غير متطابقين.")
            return redirect(url_for("register"))
        
        members = load_data(MEMBER_DATA)
        new_member = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "username": email,
            "password": password
        }
        members.append(new_member)
        save_data(MEMBER_DATA, members)
        flash("تم إنشاء الحساب بنجاح.")
        return redirect(url_for("user_page"))
    return render_template("register/register.html")

@app.route("/admin")
def admin_page():
    return render_template("admin/admin.html")

@app.route("/user")
def user_page():
    return render_template("user/user.html")

if __name__ == "__main__":
    app.run(debug=True)