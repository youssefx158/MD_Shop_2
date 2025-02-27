// تأثير شعار MD Shop في صفحة تسجيل الدخول – تأثير تضخيم الشعار وإخفاؤه وإظهاره من أعلى
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
