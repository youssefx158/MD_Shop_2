// Updated logo behaviors for the login page
document.addEventListener("DOMContentLoaded", function() {
    const mdshop = document.getElementById("mdshop");
    if (mdshop) {
      // On hover, inflate (scale up)
      mdshop.addEventListener("mouseover", function() {
        mdshop.style.transform = "scale(1.2)";
        mdshop.style.color = "#ff4500";  // Change color on hover
      });
      mdshop.addEventListener("mouseout", function() {
        mdshop.style.transform = "scale(1)";
        mdshop.style.color = "#2a2a2a";  // Original color
      });
      // On click, animate pop effect: move right then return to original position
      mdshop.addEventListener("click", function() {
        mdshop.style.transition = "transform 0.5s";
        mdshop.style.transform = "translateX(300px) scale(0.2)";
        setTimeout(() => {
          mdshop.style.transform = "translateX(0) scale(1)";
        }, 500);
      });
    }
  });