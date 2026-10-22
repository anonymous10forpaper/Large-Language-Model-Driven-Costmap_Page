const menuButton = document.querySelector('[data-menu-button]');
const navigation = document.querySelector('[data-nav]');

function closeMenu() {
  if (!menuButton || !navigation) return;
  navigation.classList.remove('open');
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation');
  document.body.classList.remove('menu-open');
}

if (menuButton && navigation) {
  menuButton.addEventListener('click', () => {
    const isOpen = navigation.classList.toggle('open');
    menuButton.setAttribute('aria-expanded', String(isOpen));
    menuButton.setAttribute('aria-label', isOpen ? 'Close navigation' : 'Open navigation');
    document.body.classList.toggle('menu-open', isOpen);
  });

  navigation.querySelectorAll('a').forEach((link) => {
    link.addEventListener('click', closeMenu);
  });

  window.addEventListener('resize', () => {
    if (window.innerWidth > 1020) closeMenu();
  });
  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && navigation.classList.contains('open')) {
      closeMenu();
      menuButton.focus();
    }
  });
}

document.querySelectorAll('[data-tabs]').forEach((tabs) => {
  const buttons = Array.from(tabs.querySelectorAll('[data-tab]'));
  const panels = Array.from(tabs.querySelectorAll('[data-panel]'));

  function activate(name) {
    buttons.forEach((button) => {
      const active = button.dataset.tab === name;
      button.setAttribute('aria-selected', String(active));
      button.tabIndex = active ? 0 : -1;
    });
    panels.forEach((panel) => {
      panel.hidden = panel.dataset.panel !== name;
    });
  }

  buttons.forEach((button, index) => {
    button.addEventListener('click', () => activate(button.dataset.tab));
    button.addEventListener('keydown', (event) => {
      if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
      event.preventDefault();
      const direction = event.key === 'ArrowRight' ? 1 : -1;
      const next = (index + direction + buttons.length) % buttons.length;
      buttons[next].focus();
      activate(buttons[next].dataset.tab);
    });
  });
});

document.querySelectorAll('[data-copy]').forEach((button) => {
  button.addEventListener('click', async () => {
    const target = document.getElementById(button.dataset.copy);
    if (!target) return;
    const originalLabel = button.getAttribute('aria-label');
    try {
      await navigator.clipboard.writeText(target.innerText);
      button.setAttribute('aria-label', 'Copied');
      button.setAttribute('title', 'Copied');
      button.innerHTML = '<i data-lucide="check" aria-hidden="true"></i>';
    } catch (_error) {
      button.setAttribute('aria-label', 'Copy failed');
      button.setAttribute('title', 'Copy failed');
    }
    if (window.lucide) window.lucide.createIcons();
    window.setTimeout(() => {
      button.setAttribute('aria-label', originalLabel || 'Copy commands');
      button.setAttribute('title', 'Copy commands');
      button.innerHTML = '<i data-lucide="copy" aria-hidden="true"></i>';
      if (window.lucide) window.lucide.createIcons();
    }, 1600);
  });
});

document.querySelectorAll('[data-carousel]').forEach((carousel) => {
  const slides = Array.from(carousel.querySelectorAll('[data-carousel-slide]'));
  const dots = Array.from(carousel.querySelectorAll('[data-carousel-dot]'));
  const previous = carousel.querySelector('[data-carousel-prev]');
  const next = carousel.querySelector('[data-carousel-next]');
  const counter = carousel.querySelector('[data-carousel-counter]');
  const title = carousel.querySelector('[data-carousel-title]');
  let current = 0;

  if (!slides.length) return;

  function showSlide(index) {
    current = (index + slides.length) % slides.length;

    slides.forEach((slide, slideIndex) => {
      const active = slideIndex === current;
      slide.classList.toggle('is-active', active);
      slide.setAttribute('aria-hidden', String(!active));
      slide.tabIndex = active ? 0 : -1;
    });

    dots.forEach((dot, dotIndex) => {
      const active = dotIndex === current;
      dot.classList.toggle('is-active', active);
      if (active) dot.setAttribute('aria-current', 'true');
      else dot.removeAttribute('aria-current');
    });

    if (counter) counter.textContent = `${current + 1} / ${slides.length}`;
    if (title) title.textContent = slides[current].dataset.title || '';
  }

  previous?.addEventListener('click', () => showSlide(current - 1));
  next?.addEventListener('click', () => showSlide(current + 1));
  dots.forEach((dot) => {
    dot.addEventListener('click', () => showSlide(Number(dot.dataset.carouselDot)));
  });

  carousel.addEventListener('keydown', (event) => {
    if (!['ArrowLeft', 'ArrowRight'].includes(event.key)) return;
    event.preventDefault();
    showSlide(current + (event.key === 'ArrowRight' ? 1 : -1));
  });

  showSlide(0);
});

window.addEventListener('DOMContentLoaded', () => {
  if (window.lucide) window.lucide.createIcons();
});
