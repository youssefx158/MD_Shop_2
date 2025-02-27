"""
هذا هو ملف السيرفر الرئيسي.
يتأكد من أن حسابات الأدمن محفوظة في data/admin.json 
وحسابات المستخدمين في data/members.json.
يضمن الربط الصحيح مع جميع صفحات الأدمن والمستخدم وفق تصميم الموقع.
لتشغيله، استخدم:
    python server.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import json

app = Flask(__name__, template_folder="pages")
app.secret_key = "سري جداً"  # يجب تغييره في البيئات الإنتاجية

def ensure_file(file_path, default_content=""):
    directory = os.path.dirname(file_path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(default_content)

@app.route("/pages/<path:filename>")
def pages_files(filename):
    return send_from_directory("pages", filename)

@app.route("/")
def home():
    return render_template("login/login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()
    # التحقق من حسابات الأدمن
    try:
        with open("data/admin.json", "r", encoding="utf-8") as f:
            admin_data = json.load(f)
    except:
        admin_data = []
    for admin in admin_data:
        if admin.get("email") == email and admin.get("password") == password:
            return redirect(url_for("admin_page"))
    # التحقق من حسابات المستخدمين
    try:
        with open("data/members.json", "r", encoding="utf-8") as f:
            members = json.load(f)
    except:
        members = []
    for member in members:
        if member.get("username") == email:
            if member.get("password") == password:
                return redirect(url_for("user_page"))
            else:
                flash("كلمة المرور غير صحيحة.")
                return redirect(url_for("home"))
    # إنشاء حساب مستخدم جديد تلقائيًا إذا لم يكن موجودًا (باستثناء الأدمن)
    if email and password:
        if email.lower() == "admin@example.com":
            flash("لا يمكنك إنشاء حساب أدمن عبر صفحة التسجيل. استخدم صفحة تسجيل الدخول.")
            return redirect(url_for("home"))
        new_member = {"username": email, "password": password}
        members.append(new_member)
        with open("data/members.json", "w", encoding="utf-8") as f:
            json.dump(members, f, ensure_ascii=False, indent=4)
        flash("تم تسجيل حساب جديد بنجاح.")
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
        if email.lower() == "admin@example.com":
            flash("لا يمكنك إنشاء حساب أدمن عبر صفحة التسجيل. استخدم صفحة تسجيل الدخول.")
            return redirect(url_for("register"))
        if password != confirm_password:
            flash("كلمة المرور وتأكيدها غير متطابقين.")
            return redirect(url_for("register"))
        try:
            with open("data/members.json", "r", encoding="utf-8") as f:
                members = json.load(f)
        except:
            members = []
        new_member = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "username": email,
            "password": password
        }
        members.append(new_member)
        with open("data/members.json", "w", encoding="utf-8") as f:
            json.dump(members, f, ensure_ascii=False, indent=4)
        flash("تم إنشاء الحساب بنجاح. الرجاء تسجيل الدخول.")
        return redirect(url_for("home"))
    return render_template("register/register.html")

@app.route("/admin")
def admin_page():
    return render_template("admin/admin.html")

@app.route("/admin/products")
def admin_products():
    return render_template("admin/products/products.html")

@app.route("/admin/users")
def admin_users():
    return render_template("admin/users/users.html")

@app.route("/admin/orders")
def admin_orders():
    return render_template("admin/orders/orders.html")

@app.route("/admin/tickets")
def admin_tickets():
    return render_template("admin/tickets/tickets.html")

@app.route("/user")
def user_page():
    return render_template("user/user.html")

if __name__ == "__main__":
    app.run(debug=True)