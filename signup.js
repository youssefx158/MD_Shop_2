// تأثير MD Shop عند النقر كما في صفحة تسجيل الدخول
document.getElementById("mdshop").addEventListener("click", function() {
  const mdshop = this;
  mdshop.style.transition = "transform 0.5s ease";
  mdshop.style.transform = "translateX(-100px) scale(0.8)";
  setTimeout(() => {
    mdshop.style.transform = "translateX(0) scale(1)";
  }, 500);
});

// إنشاء فقاعات خلفية ديناميكية
function createBubble() {
  const bubble = document.createElement("div");
  bubble.classList.add("bubble");
  const size = Math.random() * 50 + 20;
  bubble.style.width = `${size}px`;
  bubble.style.height = `${size}px`;
  bubble.style.left = Math.random() * window.innerWidth + "px";
  bubble.style.animationDuration = Math.random() * 5 + 5 + "s";
  document.body.appendChild(bubble);
  setTimeout(() => {
    bubble.remove();
  }, 10000);
}
setInterval(createBubble, 500);