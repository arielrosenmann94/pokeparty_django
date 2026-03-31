/* PokéParty — Party-specific JS */
document.addEventListener('DOMContentLoaded', () => {

  /* ── Capture button loading state ── */
  const captureForm = document.getElementById('capture-form');
  const captureBtn  = document.getElementById('capture-btn');

  if (captureForm && captureBtn) {
    captureForm.addEventListener('submit', () => {
      captureBtn.disabled = true;
      captureBtn.innerHTML = '<span class="loading">⏳</span> Capturando...';
    });
  }

  /* ── Highlight selected type badge ── */
  const typeBadges = document.querySelectorAll('.type-badge');
  typeBadges.forEach(badge => {
    const radio = badge.querySelector('input[type="radio"]');
    if (!radio) return;

    // Sync initial state
    if (radio.checked) badge.classList.add('is-selected');

    badge.addEventListener('click', () => {
      typeBadges.forEach(b => b.classList.remove('is-selected'));
      badge.classList.add('is-selected');
    });
  });

  /* ── Pokemon card entrance animation ── */
  const cards = document.querySelectorAll('.pokemon-card:not(.pokemon-card--empty)');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => {
      if (entry.isIntersecting) {
        setTimeout(() => {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
        }, i * 60);
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  cards.forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(16px)';
    card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
    observer.observe(card);
  });

  /* ── Animate stat bars on load ── */
  const statBars = document.querySelectorAll('.stat-bar');
  statBars.forEach(bar => {
    const target = bar.style.getPropertyValue('--val');
    bar.style.setProperty('--val', '0');
    setTimeout(() => {
      bar.style.setProperty('--val', target);
    }, 200);
  });

});
