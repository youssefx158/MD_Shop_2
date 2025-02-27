// تأثيرات بسيطة على صفحة إنشاء الحساب
document.addEventListener('DOMContentLoaded', () => {
    const logo = document.querySelector('.logo');
    logo.addEventListener('mouseover', () => {
      logo.style.transform = 'scale(1.1)';
    });
    logo.addEventListener('mouseout', () => {
      logo.style.transform = 'scale(1)';
    });
    logo.addEventListener('click', () => {
      logo.style.transform = 'rotate(360deg)';
      setTimeout(() => {
        logo.style.transform = 'rotate(0deg)';
      }, 300);
    });
  });