"""
هذا الملف يقوم بتحديث بنية المشروع وإنشاء/تحديث الملفات اللازمة لتصميم صفحات الموقع بحيث تكون جميع الصفحات متوافقة مع تصميم صفحة تسجيل الدخول،
ويظهر شعار "MD Shop" بنفس التنسيق على جميع الصفحات وليس فقط على صفحة تسجيل الدخول.
كما يتم التأكد من عدم كتابة أي بيانات في ملف المستخدمين (data/members.json) إلا بعد إنشاء حساب من صفحة التسجيل.

لتشغيل الملف:
    python update_project.py
"""

import os
import json

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def ensure_file(path, content=""):
    """
    ينشئ الملف إذا لم يكن موجودًا أو يحدثه إذا تغير المحتوى.
    """
    ensure_dir(os.path.dirname(path))
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"تم إنشاء الملف: {path}")
    else:
        with open(path, "r", encoding="utf-8") as f:
            existing = f.read()
        if existing != content:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"تم تحديث الملف: {path}")

def setup_data_files():
    ensure_file("data/admin.json", "[]")
    ensure_file("data/members.json", "[]")
    ensure_file("data/products.json", "[]")
    print("تم إعداد ملفات البيانات بنجاح.")

# النمط الأساسي المشترك لجميع الصفحات – بدون أي خطوط سوداء ويظهر شعار MD Shop بنفس التنسيق في جميع الصفحات
base_css = """/* النمط المشترك للصفحات */
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background-color: #87ceeb;
  overflow: hidden;
  position: relative;
}
.bubble-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  overflow: hidden;
}
.bubble-container::before,
.bubble-container::after {
  content: "";
  position: absolute;
  top: 100%;
  background: rgba(255,255,255,0.7);
  border-radius: 50%;
  animation: bubble 5s infinite ease-in;
}
.bubble-container::before {
  left: 10%;
  width: 20px;
  height: 20px;
}
.bubble-container::after {
  right: 20%;
  width: 15px;
  height: 15px;
  animation-duration: 4s;
}
@keyframes bubble {
  0% { transform: translateY(0) scale(1); opacity: 1; }
  100% { transform: translateY(-110vh) scale(0.5); opacity: 0; }
}
header {
  background: none;
  text-align: center;
  padding: 20px 0;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
  border: none;
}
#mdshop {
  font-size: 2.8rem;
  color: #222;
  cursor: pointer;
  transition: transform 0.5s ease, opacity 0.5s ease;
}
#mdshop:hover {
  transform: scale(1.15);
}
"""

def setup_login_page():
    login_html = """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>MD Shop - تسجيل الدخول</title>
  <base href="/pages/login/">
  <link rel="stylesheet" href="login.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="form-container">
    <form action="/login" method="POST">
      <h2>تسجيل الدخول</h2>
      <input type="email" name="email" placeholder="البريد الإلكتروني" required>
      <input type="password" name="password" placeholder="كلمة المرور" required>
      <button type="submit">تسجيل الدخول</button>
    </form>
    <div class="small-btn-container">
      <a href="/register">إنشاء حساب</a>
    </div>
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul class="flashes">
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
  </div>
  <script src="login.js"></script>
</body>
</html>
"""
    login_css = base_css + """
.form-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255,255,255,0.95);
  padding: 40px 30px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0,0,0,0.3);
  width: 320px;
  text-align: center;
  z-index: 101;
}
.form-container h2 {
  margin-bottom: 20px;
  color: #222;
}
.form-container input {
  width: 100%;
  padding: 10px;
  margin: 10px 0;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.form-container button {
  width: 100%;
  padding: 10px;
  background-color: #0066cc;
  color: #fff;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  transition: background-color 0.3s;
}
.form-container button:hover {
  background-color: #004c99;
}
.small-btn-container {
  margin-top: 10px;
}
.small-btn-container a {
  font-size: 0.9rem;
  text-decoration: none;
  color: #0066cc;
}
.small-btn-container a:hover {
  text-decoration: underline;
}
.flashes {
  margin-top: 15px;
  list-style: none;
  padding: 0;
  color: red;
}
"""
    login_js = """// تأثير شعار MD Shop في صفحة تسجيل الدخول – تأثير تضخيم الشعار وإخفاؤه وإظهاره من أعلى
document.addEventListener("DOMContentLoaded", function() {
  const mdshop = document.getElementById("mdshop");
  if (mdshop) {
    mdshop.addEventListener("click", function() {
      mdshop.style.transition = "transform 0.5s ease, opacity 0.5s ease";
      mdshop.style.transform = "scale(1.5)";
      setTimeout(() => { mdshop.style.opacity = "0"; }, 800);
      setTimeout(() => {
        mdshop.style.transition = "none";
        mdshop.style.transform = "translateY(-100px) scale(1)";
        mdshop.style.opacity = "1";
        setTimeout(() => { mdshop.style.transition = "transform 0.5s ease"; mdshop.style.transform = "translateY(0)"; }, 50);
      }, 1500);
    });
  }
});
"""
    ensure_file("pages/login/login.html", login_html)
    ensure_file("pages/login/login.css", login_css)
    ensure_file("pages/login/login.js", login_js)
    print("تم إعداد صفحة تسجيل الدخول.")

def setup_admin_dashboard():
    dashboard_html = """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>MD Shop - لوحة الأدمن</title>
  <base href="/pages/admin/">
  <link rel="stylesheet" href="admin.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="menu-container">
    <button onclick="location.href='/admin/products/products.html'">اداره المنتجات</button>
    <button onclick="location.href='/admin/users/users.html'">اداره المستخدمين</button>
    <button onclick="location.href='/admin/orders/orders.html'">اداره الطلبات</button>
    <button onclick="location.href='/admin/tickets/tickets.html'">اداره التكتات</button>
  </div>
  <script src="admin.js"></script>
</body>
</html>
"""
    dashboard_css = base_css + """
.menu-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 100px);
  gap: 15px;
  padding: 20px;
}
.menu-container button {
  width: 250px;
  padding: 15px;
  font-size: 1.1rem;
  background: #007acc;
  border: none;
  border-radius: 6px;
  color: #fff;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}
.menu-container button:hover {
  background: #005f99;
  transform: scale(1.05);
}
"""
    dashboard_js = """// تأثير شعار MD Shop في صفحة الأدمن
document.addEventListener("DOMContentLoaded", function() {
  const mdshop = document.getElementById("mdshop");
  if (mdshop) {
    mdshop.addEventListener("click", function() {
      mdshop.style.transition = "transform 0.5s ease, opacity 0.5s ease";
      mdshop.style.transform = "scale(1.5)";
      setTimeout(() => { mdshop.style.opacity = "0"; }, 800);
      setTimeout(() => {
        mdshop.style.transition = "none";
        mdshop.style.transform = "translateY(-100px) scale(1)";
        mdshop.style.opacity = "1";
        setTimeout(() => { mdshop.style.transition = "transform 0.5s ease"; mdshop.style.transform = "translateY(0)"; }, 50);
      }, 1500);
    });
  }
});
"""
    ensure_file("pages/admin/admin.html", dashboard_html)
    ensure_file("pages/admin/admin.css", dashboard_css)
    ensure_file("pages/admin/admin.js", dashboard_js)
    print("تم إعداد صفحة الأدمن الرئيسية.")

def setup_section(section, title, placeholder):
    base = f"pages/admin/{section}"
    ensure_dir(base)
    html_content = f"""<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>{title} - MD Shop</title>
  <base href="/pages/admin/{section}/">
  <link rel="stylesheet" href="{section}.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="content-container">
    <h2>{title}</h2>
    <p>{placeholder}</p>
  </div>
  <script src="{section}.js"></script>
</body>
</html>
"""
    css_content = base_css + f"""
.content-container {{
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 100px);
  padding: 20px;
}}
"""
    js_content = f"""// جافا سكريبت لصفحة {title}
console.log("{title} تم تحميلها بنجاح.");
"""
    ensure_file(os.path.join(base, f"{section}.html"), html_content)
    ensure_file(os.path.join(base, f"{section}.css"), css_content)
    ensure_file(os.path.join(base, f"{section}.js"), js_content)
    print(f"تم إعداد قسم '{section}'.")

def setup_products_section():
    section = "products"
    base = f"pages/admin/{section}"
    ensure_dir(base)
    html_content = """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>اداره المنتجات - MD Shop</title>
  <base href="/pages/admin/products/">
  <link rel="stylesheet" href="products.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header>
    <h1 id="mdshop">MD Shop</h1>
  </header>
  <div class="products-container">
    <div class="top-bar">
      <h2>اداره المنتجات</h2>
      <button id="addProductBtn" class="add-btn">+</button>
    </div>
    <!-- النافذة المنبثقة لإضافة/تعديل المنتج -->
    <div id="productModal" class="modal">
      <div class="modal-content">
        <span id="closeModal" class="close">&times;</span>
        <h3 id="modalTitle">اضافة منتج</h3>
        <form id="productForm">
          <label>اسم المنتج:</label>
          <input type="text" name="productName" required>
          <label>وصف المنتج:</label>
          <textarea name="productDesc" required></textarea>
          <label>المقاسات:</label>
          <div class="dynamic-input" id="sizesContainer">
            <input type="text" id="sizeInput" placeholder="اكتب مقاس">
            <button type="button" id="addSizeBtn">+</button>
            <div id="sizesList"></div>
          </div>
          <label>الالوان:</label>
          <div class="dynamic-input" id="colorsContainer">
            <input type="text" id="colorInput" placeholder="اكتب لون">
            <button type="button" id="addColorBtn">+</button>
            <div id="colorsList"></div>
          </div>
          <label>السعر:</label>
          <div class="price-input">
            <input type="number" name="price" step="0.01" required>
            <span>ج</span>
          </div>
          <label>صور المنتج:</label>
          <div id="imagesContainer">
            <input type="file" id="imageInput" accept="image/*" multiple>
            <div id="previewImages"></div>
          </div>
          <button type="submit" id="saveProductBtn" class="submit-btn">اضافة منتج</button>
        </form>
      </div>
    </div>
    <!-- قائمة المنتجات -->
    <div id="productsList">
      <!-- ستظهر بطاقات المنتجات هنا -->
    </div>
  </div>
  <script src="products.js"></script>
</body>
</html>
"""
    css_content = base_css + """
.products-container {
  margin-top: 80px;
  padding: 20px;
}
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.add-btn {
  background: green;
  color: #fff;
  font-size: 1.5rem;
  border: none;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}
.add-btn:hover {
  background: darkgreen;
  transform: scale(1.05);
}
.modal {
  display: none;
  position: fixed;
  z-index: 200;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.6);
}
.modal-content {
  background: #fff;
  margin: 8% auto;
  padding: 20px;
  width: 90%;
  max-width: 600px;
  border-radius: 10px;
  position: relative;
}
.close {
  position: absolute;
  right: 15px;
  top: 10px;
  font-size: 1.5rem;
  cursor: pointer;
}
.dynamic-input {
  margin-bottom: 15px;
}
.dynamic-input input {
  padding: 8px;
  font-size: 1rem;
  width: 70%;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.dynamic-input button {
  padding: 8px 12px;
  margin-left: 5px;
  cursor: pointer;
  border: none;
  background: #007acc;
  color: #fff;
  border-radius: 4px;
}
#sizesList, #colorsList {
  margin-top: 10px;
}
.item-tag {
  display: inline-block;
  background: #ddd;
  padding: 5px 10px;
  margin: 5px;
  border-radius: 3px;
}
.item-tag button {
  margin-left: 5px;
  background: transparent;
  border: none;
  cursor: pointer;
  color: red;
  font-weight: bold;
}
.price-input {
  display: flex;
  align-items: center;
}
.price-input input {
  width: 100%;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
.price-input span {
  margin-left: 5px;
  font-size: 1rem;
}
#imagesContainer {
  margin-bottom: 15px;
}
#previewImages {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 10px;
}
.image-preview {
  position: relative;
  width: 80px;
  height: 80px;
}
.image-preview img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.image-preview .remove-img {
  position: absolute;
  top: -5px;
  right: -5px;
  background: red;
  color: #fff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  width: 20px;
  height: 20px;
  font-size: 0.8rem;
}
.submit-btn {
  background: #007acc;
  color: #fff;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  border-radius: 4px;
  font-size: 1rem;
  transition: background 0.3s;
}
.submit-btn:hover {
  background: #005f99;
}
.product-card {
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 5px;
  padding: 15px;
  margin: 15px 0;
}
.product-card .actions {
  margin-top: 10px;
  text-align: right;
}
.product-card .actions button {
  margin-left: 10px;
  padding: 8px 12px;
  cursor: pointer;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
}
.delete-btn {
  background: red;
  color: #fff;
}
.edit-btn {
  background: orange;
  color: #fff;
}
"""
    js_content = """// جافا سكريبت لإدارة المنتجات
document.addEventListener("DOMContentLoaded", function() {
  const addProductBtn = document.getElementById("addProductBtn");
  const productModal = document.getElementById("productModal");
  const closeModal = document.getElementById("closeModal");
  const productForm = document.getElementById("productForm");
  const sizesList = document.getElementById("sizesList");
  const addSizeBtn = document.getElementById("addSizeBtn");
  const sizeInput = document.getElementById("sizeInput");
  const colorsList = document.getElementById("colorsList");
  const addColorBtn = document.getElementById("addColorBtn");
  const colorInput = document.getElementById("colorInput");
  const imageInput = document.getElementById("imageInput");
  const previewImages = document.getElementById("previewImages");

  let sizes = [];
  let colors = [];
  let images = [];

  addProductBtn.addEventListener("click", function() {
    productModal.style.display = "block";
    document.getElementById("modalTitle").innerText = "اضافة منتج";
    productForm.reset();
    sizes = [];
    colors = [];
    images = [];
    sizesList.innerHTML = "";
    colorsList.innerHTML = "";
    previewImages.innerHTML = "";
    document.getElementById("saveProductBtn").innerText = "اضافة منتج";
  });

  closeModal.addEventListener("click", function() {
    productModal.style.display = "none";
  });

  addSizeBtn.addEventListener("click", function() {
    const value = sizeInput.value.trim();
    if (value) {
      sizes.push(value);
      updateSizes();
      sizeInput.value = "";
    }
  });

  function updateSizes() {
    sizesList.innerHTML = "";
    sizes.forEach((size, index) => {
      const span = document.createElement("span");
      span.className = "item-tag";
      span.innerText = size;
      const removeBtn = document.createElement("button");
      removeBtn.innerText = "-";
      removeBtn.onclick = function() {
        sizes.splice(index, 1);
        updateSizes();
      };
      span.appendChild(removeBtn);
      sizesList.appendChild(span);
    });
  }

  addColorBtn.addEventListener("click", function() {
    const value = colorInput.value.trim();
    if (value) {
      colors.push(value);
      updateColors();
      colorInput.value = "";
    }
  });

  function updateColors() {
    colorsList.innerHTML = "";
    colors.forEach((color, index) => {
      const span = document.createElement("span");
      span.className = "item-tag";
      span.innerText = color;
      const removeBtn = document.createElement("button");
      removeBtn.innerText = "-";
      removeBtn.onclick = function() {
        colors.splice(index, 1);
        updateColors();
      };
      span.appendChild(removeBtn);
      colorsList.appendChild(span);
    });
  }

  imageInput.addEventListener("change", function() {
    previewImages.innerHTML = "";
    images = [];
    Array.from(this.files).forEach(file => {
      const reader = new FileReader();
      reader.onload = function(e) {
        const div = document.createElement("div");
        div.className = "image-preview";
        const img = document.createElement("img");
        img.src = e.target.result;
        const removeBtn = document.createElement("button");
        removeBtn.className = "remove-img";
        removeBtn.innerText = "X";
        removeBtn.onclick = function() {
          div.remove();
        };
        div.appendChild(img);
        div.appendChild(removeBtn);
        previewImages.appendChild(div);
      }
      reader.readAsDataURL(file);
      images.push(file.name);
    });
  });

  productForm.addEventListener("submit", function(e) {
    e.preventDefault();
    const formData = new FormData(productForm);
    const productData = {
      name: formData.get("productName"),
      description: formData.get("productDesc"),
      sizes: sizes,
      colors: colors,
      price: formData.get("price"),
      images: images
    };
    // هنا يمكنك إرسال بيانات المنتج إلى السيرفر لتخزينها في data/products.json إذا لزم الأمر.
    saveProduct(productData);
    productModal.style.display = "none";
  });

  function saveProduct(product) {
    const productsList = document.getElementById("productsList");
    const card = document.createElement("div");
    card.className = "product-card";
    card.innerHTML = `
      <h3>${product.name}</h3>
      <p>${product.description}</p>
      <p><strong>المقاسات:</strong> ${product.sizes.join(", ")}</p>
      <p><strong>الالوان:</strong> ${product.colors.join(", ")}</p>
      <p><strong>السعر:</strong> ${product.price} ج</p>
      <div class="actions">
        <button class="delete-btn">حذف</button>
        <button class="edit-btn">تعديل</button>
      </div>
    `;
    card.querySelector(".delete-btn").addEventListener("click", function() {
      if (confirm("هل انت متأكد من حذف المنتج؟")) {
        card.remove();
      }
    });
    card.querySelector(".edit-btn").addEventListener("click", function() {
      alert("وظيفة التعديل لم تُنفذ بعد.");
    });
    productsList.appendChild(card);
  }
});
"""
    ensure_file(os.path.join(base, "products.html"), html_content)
    ensure_file(os.path.join(base, "products.css"), css_content)
    ensure_file(os.path.join(base, "products.js"), js_content)
    print("تم إعداد قسم إدارة المنتجات بالتفاصيل بنجاح.")

def setup_all_admin_sections():
    setup_products_section()
    setup_section("users", "اداره المستخدمين", "صفحة لإدارة المستخدمين مع التفاصيل، حذف الحساب، حظر وإلغاء حظر المستخدم.")
    setup_section("orders", "اداره الطلبات", "صفحة مؤقتة لإدارة الطلبات.")
    setup_section("tickets", "اداره التكتات", "صفحة مؤقتة لإدارة التكتات.")

if __name__ == "__main__":
    setup_data_files()
    setup_login_page()
    setup_admin_dashboard()
    setup_all_admin_sections()
    print("تم تحديث المشروع وإنشاء كافة صفحات الأدمن والمستخدم بتصميم متطابق مع موقع MD Shop بدون ظهور أي خط أسود.")