// JavaScript for the admin products page
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
