"""
هذا هو ملف السيرفر الرئيسي المُحسن.
يعمل على ربط كافة الصفحات والروابط الخاصة بكل زر بشكل صحيح،
ويضمن أن حسابات الأدمن محفوظة في data/admin.json وحسابات المستخدمين محفوظة في data/members.json.
لاحظ أنه لن يتم إنشاء بيانات للمستخدم تلقائياً أثناء تسجيل الدخول؛ يجب إنشاء الحساب من صفحة التسجيل.
تأكد من تشغيل الملف بـ:
    python server.py
"""

from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import os
import json

app = Flask(__name__, template_folder="pages")
app.secret_key = "سري جداً"  # يرجى تغييره في البيئات الإنتاجية

# خدمة ملفات الصفحات الثابتة
@app.route("/pages/<path:filename>")
def pages_files(filename):
    return send_from_directory("pages", filename)

# الصفحة الرئيسية: صفحة تسجيل الدخول
@app.route("/")
def home():
    return render_template("login/login.html")

# تسجيل الدخول: التحقق من حسابات الأدمن أو المستخدم (لن يتم إنشاء حساب جديد هنا)
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    # التحقق من حسابات الأدمن
    try:
        with open("data/admin.json", "r", encoding="utf-8") as f:
            admin_data = json.load(f)
    except Exception as e:
        admin_data = []
        print("خطأ في قراءة data/admin.json:", e)
    
    for admin in admin_data:
        if admin.get("email") == email and admin.get("password") == password:
            return redirect(url_for("admin_page"))
    
    # التحقق من حسابات المستخدمين
    try:
        with open("data/members.json", "r", encoding="utf-8") as f:
            members = json.load(f)
    except Exception as e:
        members = []
        print("خطأ في قراءة data/members.json:", e)
    
    for member in members:
        if member.get("username") == email:
            if member.get("password") == password:
                return redirect(url_for("user_page"))
            else:
                flash("كلمة المرور غير صحيحة.")
                return redirect(url_for("home"))
    
    flash("الحساب غير موجود. يرجى إنشاء حساب من صفحة التسجيل.")
    return redirect(url_for("home"))

# صفحة التسجيل: هنا يتم إنشاء الحساب وكتابة بياناته في ملف المستخدمين
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
        except Exception as e:
            members = []
            print("خطأ في قراءة data/members.json:", e)
        
        new_member = {
            "first_name": first_name,
            "last_name": last_name,
            "phone": phone,
            "email": email,
            "username": email,
            "password": password
        }
        members.append(new_member)
        try:
            with open("data/members.json", "w", encoding="utf-8") as f:
                json.dump(members, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("خطأ في حفظ data/members.json:", e)
        flash("تم إنشاء الحساب بنجاح. الرجاء تسجيل الدخول.")
        return redirect(url_for("home"))
    
    return render_template("register/register.html")

# صفحة الأدمن الرئيسية
@app.route("/admin")
def admin_page():
    return render_template("admin/admin.html")

# صفحة إدارة المنتجات
@app.route("/admin/products")
def admin_products():
    return render_template("admin/products/products.html")

# صفحة إدارة المستخدمين
@app.route("/admin/users")
def admin_users():
    return render_template("admin/users/users.html")

# صفحة إدارة الطلبات
@app.route("/admin/orders")
def admin_orders():
    return render_template("admin/orders/orders.html")

# صفحة إدارة التكتات
@app.route("/admin/tickets")
def admin_tickets():
    return render_template("admin/tickets/tickets.html")

# صفحة المستخدم الرئيسي
@app.route("/user")
def user_page():
    return render_template("user/user.html")

if __name__ == "__main__":
    app.run(debug=True)