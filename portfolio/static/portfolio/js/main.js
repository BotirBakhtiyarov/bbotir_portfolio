/**
 * bbotir.xyz — Lightweight UX: smooth scroll, focus management, contact form polish.
 */
(function () {
  'use strict';

  // Smooth scroll for anchor links (respects prefers-reduced-motion in CSS)
  document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
    var id = anchor.getAttribute('href');
    if (id === '#') return;
    anchor.addEventListener('click', function (e) {
      var target = document.querySelector(id);
      if (target) {
        e.preventDefault();
        target.setAttribute('tabindex', '-1');
        target.focus({ preventScroll: true });
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // After form submit success, focus the first heading or contact section for screen readers
  var messages = document.querySelector('.message.success');
  if (messages) {
    var main = document.querySelector('main');
    if (main) {
      var firstHeading = main.querySelector('h1, h2');
      if (firstHeading) {
        firstHeading.setAttribute('tabindex', '-1');
        firstHeading.focus();
      }
    }
  }

  // Staggered reveal on scroll (2026-style)
  if (typeof IntersectionObserver !== 'undefined' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, { rootMargin: '0px 0px -50px 0px', threshold: 0 });

    document.querySelectorAll('.card, .skill-group, .section-head').forEach(function (el, i) {
      el.classList.add('reveal-on-scroll');
      el.style.setProperty('--reveal-delay', (i * 0.06) + 's');
      observer.observe(el);
    });
  }
})();
