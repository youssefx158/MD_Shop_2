// جافا سكريبت لإدارة المنتجات
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
