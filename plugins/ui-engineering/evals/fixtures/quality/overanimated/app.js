window.addEventListener('scroll', () => {
  document.querySelectorAll('[data-animate]').forEach(el => {
    const r = el.getBoundingClientRect();
    el.classList.toggle('in', r.top < innerHeight);
  });
  document.querySelector('.parallax-layer').style.top = (scrollY * 0.5) + 'px';
});
window.addEventListener('wheel', (event) => { event.preventDefault(); window.scrollBy(0, event.deltaY * 2); }, { passive: false });
