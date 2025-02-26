document.addEventListener("DOMContentLoaded", function(){
  // إنشاء فقاعات الخلفية
  const bubblesContainer = document.getElementById("bubblesContainer");
  if (bubblesContainer) {
    const bubbleCount = 20;
    for (let i = 0; i < bubbleCount; i++) {
      const bubble = document.createElement("div");
      bubble.classList.add("bubble");
      bubble.style.left = Math.random() * 100 + "%";
      const duration = 8 + Math.random() * 5;
      bubble.style.animationDuration = duration + "s";
      const size = 20 + Math.random() * 40;
      bubble.style.width = size + "px";
      bubble.style.height = size + "px";
      bubblesContainer.appendChild(bubble);
    }
  }
});

// تأثير الشعار MD Shop عند النقر
const mdShopLogo = document.getElementById("mdShopLogo");
if (mdShopLogo) {
  mdShopLogo.addEventListener("click", () => {
    mdShopLogo.style.animation = "popEffect 0.5s forwards";
    setTimeout(() => {
      mdShopLogo.style.display = "none";
      mdShopLogo.style.animation = "";
    }, 500);
    setTimeout(() => {
      mdShopLogo.style.display = "block";
      mdShopLogo.style.animation = "slideInFromRight 1s forwards";
      setTimeout(() => {
        mdShopLogo.style.animation = "";
        mdShopLogo.style.left = "50%";
        mdShopLogo.style.transform = "translateX(-50%)";
      }, 1000);
    }, 700);
  });
}

// متغيرات لتخزين المقاسات والألوان
let sizesArray = [];
function addSize() {
  const sizeInput = document.getElementById("sizeInput");
  if (sizeInput.value.trim() !== "") {
    sizesArray.push(sizeInput.value.trim());
    updateSizesList();
    sizeInput.value = "";
  }
}
function updateSizesList() {
  const sizesList = document.getElementById("sizesList");
  sizesList.innerHTML = "";
  sizesArray.forEach((size, index) => {
    const div = document.createElement("div");
    div.style.marginBottom = "5px";
    const span = document.createElement("span");
    span.innerText = size;
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.innerText = "حذف";
    removeBtn.classList.add("add-btn");
    removeBtn.style.marginLeft = "10px";
    removeBtn.onclick = function() {
      sizesArray.splice(index, 1);
      updateSizesList();
    };
    div.appendChild(span);
    div.appendChild(removeBtn);
    sizesList.appendChild(div);
  });
  document.getElementById("sizesHidden").value = JSON.stringify(sizesArray);
}

let colorsArray = [];
function addColor() {
  const colorInput = document.getElementById("colorInput");
  if (colorInput.value.trim() !== "") {
    colorsArray.push(colorInput.value.trim());
    updateColorsList();
    colorInput.value = "";
  }
}
function updateColorsList() {
  const colorsList = document.getElementById("colorsList");
  colorsList.innerHTML = "";
  colorsArray.forEach((color, index) => {
    const div = document.createElement("div");
    div.style.marginBottom = "5px";
    const span = document.createElement("span");
    span.innerText = color;
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.innerText = "حذف";
    removeBtn.classList.add("add-btn");
    removeBtn.style.marginLeft = "10px";
    removeBtn.onclick = function() {
      colorsArray.splice(index, 1);
      updateColorsList();
    };
    div.appendChild(span);
    div.appendChild(removeBtn);
    colorsList.appendChild(div);
  });
  document.getElementById("colorsHidden").value = JSON.stringify(colorsArray);
}

// معاينة الصور عند اختيارها
const productImagesInput = document.getElementById("productImages");
if(productImagesInput){
  productImagesInput.addEventListener("change", function(event){
    const imagesPreview = document.getElementById("imagesPreview");
    imagesPreview.innerHTML = "";
    Array.from(event.target.files).forEach((file) => {
      const reader = new FileReader();
      reader.onload = function(e){
        const imgDiv = document.createElement("div");
        const img = document.createElement("img");
        img.src = e.target.result;
        const removeBtn = document.createElement("button");
        removeBtn.innerText = "X";
        removeBtn.onclick = function(){
          imgDiv.remove();
        };
        imgDiv.appendChild(img);
        imgDiv.appendChild(removeBtn);
        imagesPreview.appendChild(imgDiv);
      };
      reader.readAsDataURL(file);
    });
  });
}

// فتح النافذة لإضافة منتج
function openAddProductModal() {
  document.getElementById("productForm").reset();
  document.getElementById("sizesList").innerHTML = "";
  document.getElementById("colorsList").innerHTML = "";
  document.getElementById("imagesPreview").innerHTML = "";
  sizesArray = [];
  colorsArray = [];
  document.getElementById("productId").value = "";
  document.getElementById("modalTitle").innerText = "إضافة منتج جديد";
  document.getElementById("submitProductBtn").innerText = "إضافة المنتج";
  document.getElementById("productForm").action = "{{ url_for('add_product') }}";
  document.getElementById("productModal").style.display = "block";
}
function closeProductModal() {
  document.getElementById("productModal").style.display = "none";
}

// فتح النافذة في وضع التعديل
function editProduct(productId) {
  const product = productsData.find(item => item.id === productId);
  if (!product) {
    alert("لم يتم العثور على بيانات المنتج");
    return;
  }
  document.getElementById("productId").value = product.id;
  document.getElementById("productName").value = product.name;
  document.getElementById("productDescription").value = product.description;
  document.getElementById("productPrice").value = product.price;
  sizesArray = product.sizes || [];
  updateSizesList();
  colorsArray = product.colors || [];
  updateColorsList();
  const imagesPreview = document.getElementById("imagesPreview");
  imagesPreview.innerHTML = "";
  if (product.images && product.images.length > 0) {
    product.images.forEach(imgUrl => {
      const imgDiv = document.createElement("div");
      const img = document.createElement("img");
      img.src = imgUrl;
      const removeBtn = document.createElement("button");
      removeBtn.innerText = "X";
      removeBtn.onclick = function(){
        imgDiv.remove();
      };
      imgDiv.appendChild(img);
      imgDiv.appendChild(removeBtn);
      imagesPreview.appendChild(imgDiv);
    });
  }
  document.getElementById("modalTitle").innerText = "تعديل المنتج";
  document.getElementById("submitProductBtn").innerText = "حفظ التعديلات";
  document.getElementById("productForm").action = "{{ url_for('update_product') }}";
  document.getElementById("productModal").style.display = "block";
}

// حذف المنتج باستخدام AJAX
function deleteProduct(productId) {
  if(confirm("هل أنت متأكد من حذف هذا المنتج؟")) {
    fetch("/admin/delete_product/" + productId, {
      method: "DELETE"
    })
    .then(response => response.json())
    .then(data => {
      if(data.success) {
        location.reload();
      } else {
        alert(data.message || "فشل حذف المنتج.");
      }
    })
    .catch(err => {
      console.error(err);
      alert("حدث خطأ أثناء حذف المنتج.");
    });
  }
}
