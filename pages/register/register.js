// تأثيرات صفحة إنشاء الحساب لتعديل سلوك شعار MD Shop
document.addEventListener("DOMContentLoaded", function() {
    const mdshop = document.getElementById("mdshop");
    if (mdshop) {
      mdshop.addEventListener("click", function() {
        mdshop.style.transition = "transform 0.5s";
        mdshop.style.transform = "translateX(300px) scale(0.2)";
        setTimeout(() => {
          mdshop.style.transform = "translateX(0) scale(1)";
        }, 500);
      });
    }
  });