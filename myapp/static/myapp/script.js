const toggle = document.getElementById('toggle');
const radar = document.getElementById('radar');

toggle.addEventListener('change', (e) => {
  const animations = radar.querySelectorAll('*');
  animations.forEach(el => {
    if (e.target.checked) {
      el.style.animationPlayState = 'running';
    } else {
      el.style.animationPlayState = 'paused';
    }
  });
});

/*Dark And Light Mode*/

