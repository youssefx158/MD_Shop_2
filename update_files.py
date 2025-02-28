"""
This file updates the MD Shop project repository files to improve the product management page.
Improvements:
  - The "Add Image" button is the visible control for adding images. The file input is hidden.
  - When images are selected, previews appear above the "Add Image" button.
  - Images are expected to be stored in the "uploads" folder.
  - In the product cards, images are displayed using the URL path "/uploads/<filename>".
  - An "uploads" folder is automatically created if not present.
  - Product information is stored in data/products.json.
  
To run:
    python update_project.py
"""

import os
import json

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def create_file_if_not_exists(path, content):
    ensure_dir(os.path.dirname(path))
    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

def ensure_file(path, content):
    ensure_dir(os.path.dirname(path))
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated file: {path}")

def setup_data_files():
    # Ensure default admin, members, and products files exist.
    default_admin = json.dumps([
        {"email": "admin@example.com", "password": "admin123"}
    ], ensure_ascii=False, indent=4)
    create_file_if_not_exists("data/admin.json", default_admin)
    create_file_if_not_exists("data/members.json", "[]")
    create_file_if_not_exists("data/products.json", "[]")
    print("Data files set up (existing accounts and products remain).")

def create_uploads_folder():
    ensure_dir("uploads")
    print("Uploads folder ensured.")

# Shared base CSS for all pages.
base_css = """/* Shared CSS for all pages */
body {
  margin: 0;
  padding: 0;
  font-family: Arial, sans-serif;
  background-color: #87ceeb;
  overflow-y: auto;
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
}
#mdshop {
  font-size: 2.8rem;
  color: #fff;
  cursor: pointer;
  transition: transform 1s ease, opacity 0.5s ease;
}
#mdshop:hover {
  transform: scale(1.1);
}
"""

# MD Shop logo effect JavaScript.
mdshop_effect_js = """// MD Shop logo effect
document.addEventListener("DOMContentLoaded", function() {
  const mdshop = document.getElementById("mdshop");
  if(mdshop) {
    mdshop.addEventListener("click", function() {
      mdshop.style.transition = "transform 1s ease, opacity 0.5s ease";
      mdshop.style.transform = "scale(2)";
      mdshop.style.opacity = "0.5";
      setTimeout(() => { mdshop.style.opacity = "0"; }, 800);
      setTimeout(() => {
        mdshop.style.transition = "none";
        mdshop.style.transform = "translateY(-100px) scale(0.5)";
        mdshop.style.opacity = "0";
        setTimeout(() => {
          mdshop.style.transition = "transform 1s ease, opacity 0.5s ease";
          mdshop.style.transform = "translateY(0) scale(1)";
          mdshop.style.opacity = "1";
        }, 100);
      }, 1500);
    });
  }
});
"""

# Setup the admin products section with improved image handling.
def setup_products_section():
    base = "pages/admin/products"
    ensure_dir(base)
    
    products_html = """<!DOCTYPE html>
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
    <!-- Product add/edit modal -->
    <div id="productModal" class="modal">
      <div class="modal-content">
        <span id="closeModal" class="close">&times;</span>
        <h3 id="modalTitle">اضافة منتج</h3>
        <form id="productForm" enctype="multipart/form-data">
          <div class="form-group">
            <label>اسم المنتج:</label>
            <input type="text" name="productName" required>
          </div>
          <div class="form-group">
            <label>تفاصيل المنتج:</label>
            <textarea name="productDesc" required></textarea>
          </div>
          <div class="form-group">
            <label>المقاسات:</label>
            <div class="dynamic-input">
              <input type="text" id="sizeInput" placeholder="اكتب مقاس">
              <button type="button" id="addSizeBtn">+</button>
            </div>
            <div id="sizesList"></div>
          </div>
          <div class="form-group">
            <label>الالوان:</label>
            <div class="dynamic-input">
              <input type="text" id="colorInput" placeholder="اكتب لون">
              <button type="button" id="addColorBtn">+</button>
            </div>
            <div id="colorsList"></div>
          </div>
          <div class="form-group">
            <label>السعر:</label>
            <div class="price-input">
              <input type="number" name="price" step="0.01" required>
              <span>ج</span>
            </div>
          </div>
          <div class="form-group">
            <label>صور المنتج:</label>
            <div id="previewImages"></div>
            <div id="imagesContainer">
              <input type="file" id="imageInput" accept="image/*" multiple style="display: none;">
              <button type="button" id="addImageBtn" class="image-btn">اختر صورة</button>
            </div>
          </div>
          <div class="form-group">
            <button type="submit" id="saveProductBtn" class="submit-btn">اضافة منتج</button>
          </div>
        </form>
      </div>
    </div>
    <!-- Products list -->
    <div id="productsList"></div>
  </div>
  <script src="products.js"></script>
</body>
</html>
"""
    products_css = base_css + """
/* Product Management Styles */
.products-container {
  margin-top: 100px;
  padding: 20px;
}
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.form-group {
  margin-bottom: 15px;
  display: flex;
  flex-direction: column;
}
.form-group label {
  margin-bottom: 5px;
  font-weight: bold;
}
.form-group input,
.form-group textarea {
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.price-input {
  display: flex;
  align-items: center;
}
.price-input input {
  flex: 1;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.price-input span {
  margin-left: 5px;
  font-size: 1rem;
}
.add-btn {
  background: green;
  color: #fff;
  font-size: 1.5rem;
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  cursor: pointer;
  transition: background 0.3s, transform 0.3s;
}
.add-btn:hover {
  background: darkgreen;
  transform: scale(1.1);
}
.modal {
  display: none;
  position: fixed;
  z-index: 300;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0,0,0,0.6);
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
  display: flex;
  align-items: center;
  margin-bottom: 5px;
}
.dynamic-input input {
  flex: 1;
  padding: 8px;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.dynamic-input button {
  margin-left: 5px;
  padding: 8px 12px;
  cursor: pointer;
  background: #007acc;
  color: #fff;
  border: none;
  border-radius: 5px;
}
#sizesList, #colorsList {
  margin-top: 8px;
}
.item-tag {
  display: inline-block;
  background: #ddd;
  padding: 5px 10px;
  margin: 3px;
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
#imagesContainer {
  margin-top: 5px;
  display: flex;
  align-items: center;
}
.image-btn {
  background: #007acc;
  color: #fff;
  border: none;
  border-radius: 5px;
  padding: 8px 12px;
  margin-left: 10px;
  cursor: pointer;
  transition: background 0.3s;
}
.image-btn:hover {
  background: #005f99;
}
#previewImages {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 10px;
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
  border-radius: 5px;
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
  margin-bottom: 15px;
}
.product-card h3 {
  margin: 0 0 10px 0;
}
.product-card p {
  margin: 5px 0;
}
.product-card .product-images {
  display: flex;
  gap: 10px;
  margin-bottom: 10px;
}
.product-card .product-images img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border: 1px solid #ccc;
  border-radius: 5px;
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
  border-radius: 5px;
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
    products_js = """// JavaScript for the admin products page
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
  const saveProductBtn = document.getElementById("saveProductBtn");
  const modalTitle = document.getElementById("modalTitle");
  const addImageBtn = document.getElementById("addImageBtn");

  let sizes = [];
  let colors = [];
  let images = [];
  let editingIndex = null; // null means add new; otherwise edit
  let products = []; // Array to hold product objects

  // Open modal for adding a new product.
  function openModalForAdd() {
    modalTitle.innerText = "اضافة منتج";
    saveProductBtn.innerText = "اضافة منتج";
    productForm.reset();
    sizes = [];
    colors = [];
    images = [];
    sizesList.innerHTML = "";
    colorsList.innerHTML = "";
    previewImages.innerHTML = "";
    editingIndex = null;
    productModal.style.display = "block";
  }

  // Open modal for editing an existing product.
  function openModalForEdit(index) {
    const product = products[index];
    editingIndex = index;
    modalTitle.innerText = "تعديل منتج";
    saveProductBtn.innerText = "حفظ التعديلات";
    productForm.elements["productName"].value = product.name;
    productForm.elements["productDesc"].value = product.description;
    productForm.elements["price"].value = product.price;
    sizes = [...product.sizes];
    colors = [...product.colors];
    images = [...product.images];
    updateSizes();
    updateColors();
    updateImagePreviews();
    productModal.style.display = "block";
  }

  // Update sizes UI.
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

  // Update colors UI.
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

  // Update image previews in the form.
  function updateImagePreviews() {
    previewImages.innerHTML = "";
    images.forEach((imgName, index) => {
      const div = document.createElement("div");
      div.className = "image-preview";
      const img = document.createElement("img");
      // Display image from the uploads folder.
      img.src = "/uploads/" + encodeURIComponent(imgName);
      img.alt = imgName;
      const removeBtn = document.createElement("button");
      removeBtn.className = "remove-img";
      removeBtn.innerText = "X";
      removeBtn.onclick = function() {
        images.splice(index, 1);
        updateImagePreviews();
      };
      div.appendChild(img);
      div.appendChild(removeBtn);
      previewImages.appendChild(div);
    });
  }

  // Event listener for adding sizes.
  addSizeBtn.addEventListener("click", function() {
    const value = sizeInput.value.trim();
    if (value) {
      sizes.push(value);
      updateSizes();
      sizeInput.value = "";
    }
  });

  // Event listener for adding colors.
  addColorBtn.addEventListener("click", function() {
    const value = colorInput.value.trim();
    if (value) {
      colors.push(value);
      updateColors();
      colorInput.value = "";
    }
  });

  // When images are selected, update images array.
  imageInput.addEventListener("change", function() {
    images = [];
    Array.from(this.files).forEach(function(file) {
      images.push(file.name);
    });
    updateImagePreviews();
  });

  // When the "Add Image" button is clicked, trigger the file input.
  addImageBtn.addEventListener("click", function() {
    imageInput.click();
  });

  // Handle form submission for product add/edit.
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
    if (editingIndex === null) {
      products.push(productData);
    } else {
      products[editingIndex] = productData;
    }
    renderProducts();
    productModal.style.display = "none";
  });

  // Render product cards.
  function renderProducts() {
    const productsList = document.getElementById("productsList");
    productsList.innerHTML = "";
    products.forEach(function(product, index) {
      const card = document.createElement("div");
      card.className = "product-card";
      let imagesHtml = "";
      if (product.images && product.images.length > 0) {
        imagesHtml = '<div class="product-images">';
        product.images.forEach(function(imgName) {
          imagesHtml += '<img src="/uploads/' + encodeURIComponent(imgName) +
                        '" alt="' + imgName + '">';
        });
        imagesHtml += '</div>';
      }
      card.innerHTML = `
        <h3>${product.name}</h3>
        ${imagesHtml}
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
          products.splice(index, 1);
          renderProducts();
        }
      });
      card.querySelector(".edit-btn").addEventListener("click", function() {
        openModalForEdit(index);
      });
      productsList.appendChild(card);
    });
  }

  // Open modal when the green "+" button is clicked.
  addProductBtn.addEventListener("click", openModalForAdd);
});
"""
    ensure_file(os.path.join(base, "products.html"), products_html)
    ensure_file(os.path.join(base, "products.css"), products_css)
    ensure_file(os.path.join(base, "products.js"), products_js)
    print("Products section updated with improved image handling and storage using /uploads folder.")

# Setup other simple admin sections.
def setup_all_admin_sections():
    def setup_simple_section(section, title, placeholder):
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
  <header><h1 id="mdshop">MD Shop</h1></header>
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
        js_content = mdshop_effect_js + f"""
console.log("{title} loaded successfully.");
"""
        ensure_file(os.path.join(base, f"{section}.html"), html_content)
        ensure_file(os.path.join(base, f"{section}.css"), css_content)
        ensure_file(os.path.join(base, f"{section}.js"), js_content)
    setup_products_section()
    setup_simple_section("users", "اداره المستخدمين", "صفحة لإدارة المستخدمين مع التفاصيل.")
    setup_simple_section("orders", "اداره الطلبات", "صفحة مؤقتة لإدارة الطلبات.")
    setup_simple_section("tickets", "اداره التكتات", "صفحة مؤقتة لإدارة التكتات.")

# Setup the registration page.
def setup_register_page():
    base = "pages/register"
    ensure_dir(base)
    register_html = """<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>MD Shop - إنشاء حساب</title>
  <base href="/pages/register/">
  <link rel="stylesheet" href="register.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header><h1 id="mdshop">MD Shop</h1></header>
  <div class="register-container">
    <h2>إنشاء حساب</h2>
    <form action="/register" method="POST">
      <input type="text" name="first_name" placeholder="الاسم الأول" required>
      <input type="text" name="last_name" placeholder="اسم العائلة" required>
      <input type="text" name="phone" placeholder="رقم الهاتف" required>
      <input type="email" name="email" placeholder="البريد الإلكتروني" required>
      <input type="password" name="password" placeholder="كلمة المرور" required>
      <input type="password" name="confirm_password" placeholder="تأكيد كلمة المرور" required>
      <button type="submit">إنشاء الحساب</button>
    </form>
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
  <script src="register.js"></script>
</body>
</html>
"""
    register_css = base_css + """
.register-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255,255,255,0.95);
  padding: 40px 30px;
  border-radius: 10px;
  box-shadow: 0 0 15px rgba(0,0,0,0.3);
  width: 350px;
  text-align: center;
  z-index: 101;
}
.register-container h2 {
  margin-bottom: 20px;
  color: #222;
}
.register-container input {
  width: 100%;
  padding: 10px;
  margin: 8px 0;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}
.register-container button {
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
.register-container button:hover {
  background-color: #004c99;
}
.flashes {
  margin-top: 15px;
  list-style: none;
  padding: 0;
  color: red;
}
"""
    register_js = mdshop_effect_js
    ensure_file(os.path.join(base, "register.html"), register_html)
    ensure_file(os.path.join(base, "register.css"), register_css)
    ensure_file(os.path.join(base, "register.js"), register_js)

if __name__ == "__main__":
    setup_data_files()
    create_uploads_folder()
    # Setup login, admin, user, register pages, and admin sections.
    ensure_file("pages/login/login.html", 
"""<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>MD Shop - تسجيل الدخول</title>
  <base href="/pages/login/">
  <link rel="stylesheet" href="login.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header><h1 id="mdshop">MD Shop</h1></header>
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
    {% with messages = get_flashed_messages() %}{% if messages %}
      <ul class="flashes">{% for message in messages %}<li>{{ message }}</li>{% endfor %}</ul>
    {% endif %}{% endwith %}
  </div>
  <script src="login.js"></script>
</body>
</html>
""")
    ensure_file("pages/login/login.css", base_css + """
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
.form-container h2 { margin-bottom: 20px; color: #222; }
.form-container input { width: 100%; padding: 10px; margin: 10px 0; font-size: 1rem; border: 1px solid #ccc; border-radius: 5px; }
.form-container button { width: 100%; padding: 10px; background-color: #0066cc; color: #fff; font-size: 1rem; border: none; border-radius: 5px; cursor: pointer; margin-top: 10px; transition: background-color 0.3s; }
.form-container button:hover { background-color: #004c99; }
.small-btn-container { margin-top: 10px; }
.small-btn-container a { font-size: 0.9rem; text-decoration: none; color: #0066cc; }
.small-btn-container a:hover { text-decoration: underline; }
.flashes { margin-top: 15px; list-style: none; padding: 0; color: red; }
""")
    ensure_file("pages/login/login.js", mdshop_effect_js)
    ensure_file("pages/admin/admin.html",
"""<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>MD Shop - لوحة الأدمن</title>
  <base href="/pages/admin/">
  <link rel="stylesheet" href="admin.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header><h1 id="mdshop">MD Shop</h1></header>
  <div class="menu-container">
    <button onclick="location.href='/admin/products/products.html'">اداره المنتجات</button>
    <button onclick="location.href='/admin/users/users.html'">اداره المستخدمين</button>
    <button onclick="location.href='/admin/orders/orders.html'">اداره الطلبات</button>
    <button onclick="location.href='/admin/tickets/tickets.html'">اداره التكتات</button>
  </div>
  <script src="admin.js"></script>
</body>
</html>
""")
    ensure_file("pages/admin/admin.css", base_css + """
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
.menu-container button:hover { background: #005f99; transform: scale(1.05); }
""")
    ensure_file("pages/admin/admin.js", mdshop_effect_js)
    ensure_file("pages/user/user.html",
"""<!DOCTYPE html>
<html lang="ar">
<head>
  <meta charset="UTF-8">
  <title>MD Shop - صفحة المستخدم</title>
  <base href="/pages/user/">
  <link rel="stylesheet" href="user.css">
</head>
<body>
  <div class="bubble-container"></div>
  <header><h1 id="mdshop">MD Shop</h1></header>
  <div class="user-container">
    <h2>مرحبا بك في صفحة المستخدم</h2>
    <p>يمكنك هنا استعراض منتجاتنا وإجراء طلبات الشراء.</p>
  </div>
  <script src="user.js"></script>
</body>
</html>
""")
    ensure_file("pages/user/user.css", base_css + """
.user-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(255,255,255,0.95);
  padding: 30px 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0,0,0,0.3);
  text-align: center;
  z-index: 101;
}
.user-container h2 { margin-bottom: 15px; color: #222; }
.user-container p { font-size: 1rem; color: #333; }
""")
    ensure_file("pages/user/user.js", mdshop_effect_js)
    setup_register_page()
    setup_all_admin_sections()
    print("Project updated: All files have been updated with improved product image handling and product storage.")