document.documentElement.classList.add('js');
const observer = new IntersectionObserver((entries) => {
  for (const entry of entries) {
    if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
  }
}, { rootMargin: '0px 0px -20% 0px' });
document.querySelectorAll('.reveal').forEach((el) => observer.observe(el));
document.addEventListener('keydown', (event) => { if (event.key === 'Escape') document.querySelector('.toast').textContent = ''; });
