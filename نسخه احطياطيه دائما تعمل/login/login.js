// تأثيرات تفاعلية لشعار MD Shop
document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.logo');
  
    // عند مرور الماوس على الشعار
    logo.addEventListener('mouseover', () => {
      // تأكد من أنه لا يزال في مكانه الأصلي
      if (!logo.classList.contains('burst')) {
        logo.classList.add('inflated');
      }
    });
  
    // عند مغادرة الماوس للشعار
    logo.addEventListener('mouseout', () => {
      if (!logo.classList.contains('burst')) {
        logo.classList.remove('inflated');
      }
    });
  
    // عند الضغط على الشعار
    logo.addEventListener('click', () => {
      logo.classList.remove('inflated');
      logo.classList.add('burst');
      logo.addEventListener('animationend', () => {
        logo.classList.remove('burst');
      }, { once: true });
    });
  });