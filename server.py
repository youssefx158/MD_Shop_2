from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import data
import os

app = Flask(__name__)
app.secret_key = "SUPER_SECRET_KEY"

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        success, role_or_msg = data.check_login(email, password)
        if success:
            session["email"] = email
            session["role"] = role_or_msg
            if role_or_msg == "admin":
                return redirect(url_for("admin_products"))
            else:
                return redirect(url_for("user_page"))
        else:
            flash(role_or_msg)
            return redirect(url_for("login"))
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # يمكن إضافة منطق التسجيل هنا
    if request.method == "POST":
        flash("تم إنشاء الحساب بنجاح.")
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/admin/products", methods=["GET"])
def admin_products():
    if "role" in session and session["role"] == "admin":
        products = list(data.load_products().values())
        return render_template("admin_products.html", products=products)
    else:
        flash("يجب تسجيل الدخول كأدمن للوصول لهذه الصفحة.")
        return redirect(url_for("login"))

@app.route("/admin/add_product", methods=["POST"])
def add_product():
    if "role" in session and session["role"] == "admin":
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        import json
        try:
            sizes = json.loads(request.form.get("sizes", "[]"))
        except:
            sizes = []
        try:
            colors = json.loads(request.form.get("colors", "[]"))
        except:
            colors = []
        # معالجة الصور
        images_files = request.files.getlist("images")
        saved_images = []
        images_folder = os.path.join("static", "uploads")
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        for file in images_files:
            if file and file.filename:
                filename = file.filename
                filepath = os.path.join(images_folder, filename)
                file.save(filepath)
                saved_images.append(url_for("static", filename="uploads/" + filename))
        product = {
            "name": name,
            "description": description,
            "price": price,
            "sizes": sizes,
            "colors": colors,
            "images": saved_images
        }
        data.add_product(product)
        flash("تم إضافة المنتج بنجاح.")
        return redirect(url_for("admin_products"))
    else:
        flash("يجب تسجيل الدخول كأدمن.")
        return redirect(url_for("login"))

@app.route("/admin/update_product", methods=["POST"])
def update_product():
    if "role" in session and session["role"] == "admin":
        product_id = request.form.get("productId")
        if not product_id:
            flash("معرف المنتج غير موجود.")
            return redirect(url_for("admin_products"))
        name = request.form.get("name")
        description = request.form.get("description")
        price = request.form.get("price")
        import json
        try:
            sizes = json.loads(request.form.get("sizes", "[]"))
        except:
            sizes = []
        try:
            colors = json.loads(request.form.get("colors", "[]"))
        except:
            colors = []
        images_files = request.files.getlist("images")
        saved_images = []
        images_folder = os.path.join("static", "uploads")
        if not os.path.exists(images_folder):
            os.makedirs(images_folder)
        for file in images_files:
            if file and file.filename:
                filename = file.filename
                filepath = os.path.join(images_folder, filename)
                file.save(filepath)
                saved_images.append(url_for("static", filename="uploads/" + filename))
        products = data.load_products()
        if product_id not in products:
            flash("المنتج غير موجود.")
            return redirect(url_for("admin_products"))
        products[product_id]["name"] = name
        products[product_id]["description"] = description
        products[product_id]["price"] = price
        products[product_id]["sizes"] = sizes
        products[product_id]["colors"] = colors
        if saved_images:
            products[product_id]["images"] = saved_images
        data.save_products(products)
        flash("تم حفظ التعديلات بنجاح.")
        return redirect(url_for("admin_products"))
    else:
        flash("يجب تسجيل الدخول كأدمن.")
        return redirect(url_for("login"))

@app.route("/admin/delete_product/<product_id>", methods=["DELETE"])
def delete_product(product_id):
    if "role" in session and session["role"] == "admin":
        products = data.load_products()
        if product_id in products:
            del products[product_id]
            data.save_products(products)
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "message": "المنتج غير موجود."})
    else:
        return jsonify({"success": False, "message": "غير مصرح."})

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/user")
def user_page():
    return "صفحة المستخدم - لم يتم التطوير بعد."

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    app.run(debug=True)
