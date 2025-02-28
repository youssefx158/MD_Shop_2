// MD Shop logo effect
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

console.log("اداره الطلبات loaded successfully.");
