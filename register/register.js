// Interactive effects for the MD Shop logo on the Registration page
document.addEventListener('DOMContentLoaded', () => {
  const logo = document.querySelector('.logo');

  logo.addEventListener('mouseover', () => {
    if (!logo.classList.contains('burst')) {
      logo.classList.add('inflated');
    }
  });

  logo.addEventListener('mouseout', () => {
    if (!logo.classList.contains('burst')) {
      logo.classList.remove('inflated');
    }
  });

  logo.addEventListener('click', () => {
    logo.classList.remove('inflated');
    logo.classList.add('burst');
    logo.addEventListener('animationend', () => {
      logo.classList.remove('burst');
    }, { once: true });
  });
});