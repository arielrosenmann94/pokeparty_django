/* Auto-dismiss messages after 4s */
document.addEventListener('DOMContentLoaded', () => {
  const messages = document.querySelectorAll('.message');
  messages.forEach((msg, i) => {
    setTimeout(() => {
      msg.style.transition = 'opacity 0.4s, transform 0.4s';
      msg.style.opacity = '0';
      msg.style.transform = 'translateX(110%)';
      setTimeout(() => msg.remove(), 400);
    }, 4000 + i * 300);
  });
});
