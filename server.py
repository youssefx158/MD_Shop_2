import os
import json
from flask import Flask, request, render_template, redirect, url_for, flash, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, template_folder="pages")
app.secret_key = "سري جداً"  # Change this secret key for production use

# Configure upload folder and allowed extensions.
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the uploads folder exists.
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    print("Uploads folder created.")

# Serve static files from the pages folder.
@app.route("/pages/<path:filename>")
def pages_files(filename):
    return send_from_directory("pages", filename)

# Data file paths.
DATA_DIR = "data"
ADMIN_FILE = os.path.join(DATA_DIR, "admin.json")
MEMBERS_FILE = os.path.join(DATA_DIR, "members.json")
PRODUCTS_FILE = os.path.join(DATA_DIR, "products.json")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Serve uploaded images.
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# Home page: Login page.
@app.route("/")
def home():
    return render_template("login/login.html")

# Login route: verifies admin and member credentials.
@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "").strip()

    # Check admin credentials.
    try:
        with open(ADMIN_FILE, "r", encoding="utf-8") as f:
            admin_data = json.load(f)
    except Exception as e:
        admin_data = []
        print("Error reading data/admin.json:", e)
    
    for admin in admin_data:
        if admin.get("email") == email and admin.get("password") == password:
            return redirect(url_for("admin_page"))
    
    # Check member credentials.
    try:
        with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
            members = json.load(f)
    except Exception as e:
        members = []
        print("Error reading data/members.json:", e)
    
    for member in members:
        # In this version, member username is stored as their email.
        if member.get("username") == email or member.get("email") == email:
            if member.get("password") == password:
                return redirect(url_for("user_page"))
            else:
                flash("كلمة المرور غير صحيحة.")
                return redirect(url_for("home"))
    
    flash("الحساب غير موجود. يرجى إنشاء حساب من صفحة التسجيل.")
    return redirect(url_for("home"))

# Registration route: creates a new account.
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
            with open(MEMBERS_FILE, "r", encoding="utf-8") as f:
                members = json.load(f)
        except Exception as e:
            members = []
            print("Error reading data/members.json:", e)
        
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
            with open(MEMBERS_FILE, "w", encoding="utf-8") as f:
                json.dump(members, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("Error writing data/members.json:", e)
        flash("تم إنشاء الحساب بنجاح. الرجاء تسجيل الدخول.")
        return redirect(url_for("home"))
    
    return render_template("register/register.html")

# Admin dashboard.
@app.route("/admin")
def admin_page():
    return render_template("admin/admin.html")

# Admin subsections.
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

# User page.
@app.route("/user")
def user_page():
    return render_template("user/user.html")

# API endpoint: Save product data (expects JSON).
@app.route("/api/save_product", methods=["POST"])
def save_product():
    try:
        product = request.get_json()
    except Exception as e:
        return jsonify({"success": False, "error": "بيانات JSON غير صالحة"}), 400

    try:
        with open(PRODUCTS_FILE, "r", encoding="utf-8") as f:
            products = json.load(f)
    except Exception as e:
        products = []
    
    products.append(product)
    
    with open(PRODUCTS_FILE, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=4)
    
    return jsonify({"success": True}), 200

# API endpoint: Upload an image.
@app.route("/api/upload_image", methods=["POST"])
def upload_image():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "لا يوجد ملف في الطلب"}), 400
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"success": False, "error": "لم يتم اختيار أي ملف"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        counter = 1
        # Rename file if it exists.
        while os.path.exists(filepath):
            name, ext = os.path.splitext(filename)
            filename = f"{name}_{counter}{ext}"
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            counter += 1
        file.save(filepath)
        return jsonify({"success": True, "filename": filename}), 200
    else:
        return jsonify({"success": False, "error": "نوع الملف غير مسموح"}), 400

if __name__ == "__main__":
    app.run(debug=True)