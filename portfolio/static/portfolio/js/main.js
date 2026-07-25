/**
 * bbotir.xyz — Light editorial portfolio interactions
 */
(function () {
  'use strict';

  // Mobile navigation toggle
  var navToggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('#main-nav');

  if (navToggle && nav) {
    navToggle.addEventListener('click', function () {
      var isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
      navToggle.setAttribute('aria-expanded', String(!isExpanded));
      nav.classList.toggle('is-open');
    });

    // Close mobile menu when a link is clicked
    nav.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navToggle.setAttribute('aria-expanded', 'false');
        nav.classList.remove('is-open');
      });
    });
  }

  // Smooth scroll for anchor links
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

  // After form submit success, focus the first heading
  var successMessage = document.querySelector('.message.success');
  if (successMessage) {
    var main = document.querySelector('main');
    if (main) {
      var firstHeading = main.querySelector('h1, h2');
      if (firstHeading) {
        firstHeading.setAttribute('tabindex', '-1');
        firstHeading.focus();
      }
    }
  }

  // Scroll reveal
  if (typeof IntersectionObserver !== 'undefined' && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
        }
      });
    }, { rootMargin: '0px 0px -60px 0px', threshold: 0 });

    document.querySelectorAll('.card, .skill-group, .section-head, .hero-inner > *').forEach(function (el, i) {
      el.classList.add('reveal-on-scroll');
      el.style.setProperty('--reveal-delay', (i * 0.05) + 's');
      observer.observe(el);
    });
  }
})();
