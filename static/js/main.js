const button = document.querySelector('.menu-button');
const nav = document.querySelector('.nav');
button.addEventListener('click', () => {
  const active = nav.classList.toggle('visible');
  button.setAttribute('aria-expanded', active);
});
document.querySelectorAll('.nav a').forEach(link => link.addEventListener('click', () => {
  nav.classList.remove('visible'); button.setAttribute('aria-expanded', 'false');
}));
