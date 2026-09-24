# Motion overuse fixture

Locked SaaS landing page. Every element has `data-animate` and this CSS/JS:

```css
* { transition: all 0.6s ease; }
[data-animate] { opacity: 0; transform: translateY(60px) scale(.9); }
[data-animate].in { opacity: 1; transform: none; }
.hero-bg { animation: gradientShift 6s infinite; filter: blur(80px); }
.card:hover { transform: translateY(-12px) rotate(1deg) scale(1.05); }
.btn:hover { animation: pulse 1s infinite; }
```

```js
window.addEventListener('scroll', () => {
  document.querySelectorAll('[data-animate]').forEach(el => {
    const r = el.getBoundingClientRect();
    el.classList.toggle('in', r.top < innerHeight);
    el.style.backgroundPositionY = (scrollY * 0.5) + 'px';
  });
});
```

Parallax on three sections including text, headings split per character, counter animations on invented stats, no `prefers-reduced-motion` handling.
