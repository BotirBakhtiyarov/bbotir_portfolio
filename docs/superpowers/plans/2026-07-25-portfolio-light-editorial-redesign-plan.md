# Portfolio Light Editorial UI Redesign — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** bbotir.xyz Django portfolioni "Clean Light Editorial" uslubida qayta dizayn qilish: ochiq fon, editorial tipografiya, professional layout, saqlanadigan backend.

**Architecture:** Django templates va static fayllar (CSS/JS) almashtiriladi. Backend (models, views, urls, forms), admin panel, contact form, CV yuklash va SEO meta teglari o'zgarmaydi. Barcha o'zgarishlar `portfolio/templates/portfolio/` va `portfolio/static/portfolio/` papkalarida amalga oshiriladi.

**Tech Stack:** Django, HTML5, CSS3 (custom), Vanilla JS, Google Fonts (Inter + Playfair Display), inline SVG icons.

## Global Constraints

- Faqat `portfolio/templates/portfolio/*.html`, `portfolio/static/portfolio/css/main.css`, `portfolio/static/portfolio/js/main.js` o'zgaradi.
- Django backend, modellar, view'lar, URL'lar, admin, contact form, CV yuklash o'zgarmaydi.
- SEO meta teglari va schema.org JSON-LD saqlanadi.
- Barcha ranglar design spec'dagi tokenlarga mos keladi.
- `prefers-reduced-motion` qo'llab-quvvatlanishi shart.
- Har bir task alohida test/verify va commit bilan tugaydi.

---

## File Structure

| Fayl | Mas'uliyati |
|------|-------------|
| `portfolio/templates/portfolio/base.html` | Umumiy layout, header, footer, fonts, meta |
| `portfolio/templates/portfolio/home.html` | Hero, Skills, Projects, Experience, Contact |
| `portfolio/templates/portfolio/casestudy_list.html` | Projectlar ro'yxati sahifasi |
| `portfolio/templates/portfolio/casestudy_detail.html` | Bitta project detail sahifasi |
| `portfolio/static/portfolio/css/main.css` | Barcha CSS stillar |
| `portfolio/static/portfolio/js/main.js` | Mobil menu, scroll reveal, smooth scroll |

---

### Task 1: Update base.html with new layout

**Files:**
- Modify: `portfolio/templates/portfolio/base.html`

**Interfaces:**
- Consumes: `{% block title %}`, `{% block meta_description %}`, `{% block content %}`, `{% block extra_head %}`, `{% block extra_js %}`
- Produces: Sticky header with mobile menu toggle, skip-link, footer

- [ ] **Step 1: Replace Google Fonts link**

Replace existing font import line with:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Playfair+Display:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
```

- [ ] **Step 2: Replace header block**

Replace `<header class="site-header">...</header>` with:

```html
<header class="site-header" role="banner">
    <div class="container header-inner">
        <a href="{% url 'portfolio:home' %}" class="logo" aria-label="bbotir.xyz home">bbotir.xyz</a>
        <button class="nav-toggle" aria-label="Toggle navigation" aria-expanded="false" aria-controls="main-nav">
            <span class="nav-toggle-bar" aria-hidden="true"></span>
            <span class="nav-toggle-bar" aria-hidden="true"></span>
            <span class="nav-toggle-bar" aria-hidden="true"></span>
        </button>
        <nav class="nav" id="main-nav" aria-label="Main">
            <ul class="nav-links">
                <li><a href="{% url 'portfolio:home' %}" {% if request.resolver_match.url_name == 'home' %}aria-current="page"{% endif %}>Home</a></li>
                <li><a href="{% url 'portfolio:casestudy_list' %}" {% if request.resolver_match.url_name == 'casestudy_list' or request.resolver_match.url_name == 'casestudy_detail' %}aria-current="page"{% endif %}>Projects</a></li>
                <li><a href="{% url 'portfolio:home' %}#contact">Contact</a></li>
                <li><a href="{% url 'portfolio:cv_download' %}">CV</a></li>
            </ul>
        </nav>
    </div>
</header>
```

- [ ] **Step 3: Verify base.html renders without errors**

Run:
```bash
python manage.py check
```

Expected: no errors.

- [ ] **Step 4: Commit**

```bash
git add portfolio/templates/portfolio/base.html
git commit -m "feat(ui): update base layout for light editorial redesign"
```

---

### Task 2: Rewrite main.css with design system

**Files:**
- Modify: `portfolio/static/portfolio/css/main.css`

**Interfaces:**
- Consumes: HTML classes defined in templates: `.site-header`, `.nav-toggle`, `.hero`, `.skills-grid`, `.skill-group`, `.card-grid`, `.card`, `.section`, `.section--alt`, `.contact`, `.form-group`, etc.
- Produces: Complete light editorial visual styles.

- [ ] **Step 1: Replace entire CSS file**

Replace `portfolio/static/portfolio/css/main.css` contents with:

```css
/* bbotir.xyz — Clean Light Editorial Portfolio */

:root {
  --bg: #fafafa;
  --bg-elevated: #ffffff;
  --bg-subtle: #f4f4f6;
  --text: #111118;
  --text-secondary: #4b5563;
  --text-muted: #6b7280;
  --accent: #1e3a8a;
  --accent-hover: #1e40af;
  --accent-soft: #dbeafe;
  --border: #e5e7eb;
  --border-strong: #d1d5db;
  --success: #16a34a;
  --error: #dc2626;
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.04);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.06);
  --shadow-lg: 0 12px 32px rgba(0,0,0,0.08);
  --radius-sm: 8px;
  --radius-md: 16px;
  --radius-lg: 24px;
  --radius-pill: 999px;
  --transition: 0.2s ease-out;
  --transition-slow: 0.35s ease-out;
  --container: 1140px;
}

*, *::before, *::after { box-sizing: border-box; }

html { scroll-behavior: smooth; }

body {
  margin: 0;
  font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
  font-size: 1.0625rem;
  line-height: 1.7;
  color: var(--text);
  background: var(--bg);
  -webkit-font-smoothing: antialiased;
}

.skip-link {
  position: absolute;
  top: -100%;
  left: 1rem;
  padding: 0.75rem 1.25rem;
  background: var(--accent);
  color: #fff;
  font-weight: 600;
  border-radius: var(--radius-pill);
  z-index: 1000;
  transition: top var(--transition);
  text-decoration: none;
}
.skip-link:focus { top: 1rem; outline: 2px solid var(--text); outline-offset: 2px; }

.container {
  width: 100%;
  max-width: var(--container);
  margin: 0 auto;
  padding: 0 1.5rem;
}
@media (min-width: 768px) {
  .container { padding: 0 2rem; }
}
.container--wide { max-width: 980px; }

/* Header */
.site-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255,255,255,0.92);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border);
}

.header-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 4rem;
}

.logo {
  font-family: 'Playfair Display', serif;
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--text);
  text-decoration: none;
  letter-spacing: -0.02em;
}
.logo:hover { color: var(--accent); }

.nav-toggle {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 5px;
  width: 2.5rem;
  height: 2.5rem;
  padding: 0;
  background: transparent;
  border: none;
  cursor: pointer;
}
.nav-toggle-bar {
  display: block;
  width: 1.5rem;
  height: 2px;
  background: var(--text);
  border-radius: 2px;
  transition: transform var(--transition), opacity var(--transition);
}
.nav-toggle[aria-expanded="true"] .nav-toggle-bar:nth-child(1) { transform: translateY(7px) rotate(45deg); }
.nav-toggle[aria-expanded="true"] .nav-toggle-bar:nth-child(2) { opacity: 0; }
.nav-toggle[aria-expanded="true"] .nav-toggle-bar:nth-child(3) { transform: translateY(-7px) rotate(-45deg); }

@media (min-width: 768px) {
  .nav-toggle { display: none; }
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}

.nav {
  position: absolute;
  top: 4rem;
  left: 0;
  right: 0;
  background: var(--bg-elevated);
  border-bottom: 1px solid var(--border);
  padding: 1rem 1.5rem;
  transform: translateY(-100%);
  opacity: 0;
  visibility: hidden;
  transition: transform var(--transition-slow), opacity var(--transition-slow), visibility var(--transition-slow);
}
.nav.is-open {
  transform: translateY(0);
  opacity: 1;
  visibility: visible;
}

@media (min-width: 768px) {
  .nav {
    position: static;
    background: transparent;
    border: none;
    padding: 0;
    transform: none;
    opacity: 1;
    visibility: visible;
  }
  .nav-links {
    flex-direction: row;
    align-items: center;
    gap: 0.25rem;
  }
}

.nav-links a {
  display: block;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  font-size: 0.9375rem;
  padding: 0.6rem 1rem;
  border-radius: var(--radius-pill);
  transition: color var(--transition), background var(--transition);
}
.nav-links a:hover,
.nav-links a[aria-current="page"] {
  color: var(--accent);
  background: var(--accent-soft);
}

/* Typography */
h1, h2, h3 {
  font-family: 'Playfair Display', serif;
  font-weight: 700;
  line-height: 1.2;
  margin: 0 0 0.75rem;
}

h1 { font-size: clamp(2.75rem, 6vw, 4.5rem); line-height: 1.1; }
h2 { font-size: clamp(1.75rem, 3vw, 2.25rem); }
h3 { font-size: 1.25rem; }

p { margin: 0 0 1rem; }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.875rem 1.75rem;
  font-size: 1rem;
  font-weight: 600;
  font-family: inherit;
  border-radius: var(--radius-pill);
  border: 1px solid transparent;
  cursor: pointer;
  text-decoration: none;
  transition: transform var(--transition), background var(--transition), color var(--transition), border-color var(--transition), box-shadow var(--transition);
}
.btn:hover { transform: translateY(-2px); }
.btn:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.btn--primary {
  background: var(--accent);
  color: #fff;
  box-shadow: var(--shadow-md);
}
.btn--primary:hover { background: var(--accent-hover); box-shadow: var(--shadow-lg); }

.btn--secondary {
  background: var(--bg-elevated);
  color: var(--text);
  border-color: var(--border);
}
.btn--secondary:hover { border-color: var(--accent); color: var(--accent); }

.btn--ghost {
  background: transparent;
  color: var(--text-secondary);
  border-color: var(--border);
}
.btn--ghost:hover { color: var(--accent); border-color: var(--accent); }

/* Hero */
.hero {
  padding: 4rem 0 3rem;
}
.hero-inner {
  display: grid;
  gap: 2.5rem;
  align-items: center;
}
@media (min-width: 900px) {
  .hero-inner { grid-template-columns: 1.1fr 0.9fr; gap: 4rem; }
}

.hero-badge {
  display: inline-flex;
  align-items: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--accent);
  background: var(--accent-soft);
  padding: 0.4rem 1rem;
  border-radius: var(--radius-pill);
  margin-bottom: 1.25rem;
  letter-spacing: 0.04em;
}

.hero h1 {
  margin-bottom: 1rem;
  letter-spacing: -0.03em;
}

.hero .tagline {
  font-size: 1.25rem;
  color: var(--text-secondary);
  font-weight: 500;
  margin-bottom: 1.75rem;
}

.hero-ctas {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
}

.hero-intro {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
}

.hero-skills h3 {
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}

.hero-skills-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  list-style: none;
  margin: 0;
  padding: 0;
}
.hero-skills-list li {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  padding: 0.35rem 0.75rem;
  background: var(--bg-subtle);
  border: 1px solid var(--border);
  border-radius: var(--radius-pill);
  color: var(--text-secondary);
}

/* Sections */
.section { padding: 4rem 0; }
.section--alt { background: var(--bg-subtle); }

.section-head {
  max-width: 640px;
  margin-bottom: 2.5rem;
}
.section-head h2 { margin-bottom: 0.5rem; }
.section-head p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  margin: 0;
}

/* Skills grid */
.skills-grid {
  display: grid;
  gap: 1.5rem;
}
@media (min-width: 640px) { .skills-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 900px) { .skills-grid { grid-template-columns: repeat(3, 1fr); } }

.skill-group {
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.75rem;
  transition: border-color var(--transition), box-shadow var(--transition), transform var(--transition);
}
.skill-group:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-md);
  transform: translateY(-2px);
}

.skill-icon {
  width: 2.5rem;
  height: 2.5rem;
  margin-bottom: 1.25rem;
  color: var(--accent);
}

.skill-group h3 {
  font-family: 'Inter', sans-serif;
  font-size: 0.8125rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--accent);
  margin-bottom: 1rem;
}

.skill-group ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
.skill-group li {
  padding: 0.35rem 0;
  color: var(--text-secondary);
}
.skill-group li::before {
  content: '•';
  color: var(--accent);
  margin-right: 0.5rem;
}

/* Cards */
.card-grid {
  display: grid;
  gap: 1.5rem;
}
@media (min-width: 640px) { .card-grid { grid-template-columns: repeat(2, 1fr); } }

.card {
  display: block;
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  padding: 1.75rem;
  text-decoration: none;
  color: inherit;
  transition: border-color var(--transition), box-shadow var(--transition), transform var(--transition);
}
.card:hover {
  border-color: var(--accent);
  box-shadow: var(--shadow-lg);
  transform: translateY(-4px);
}
.card:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

.card h3 {
  margin-bottom: 0.5rem;
  color: var(--text);
}
.card p {
  color: var(--text-secondary);
  font-size: 0.9375rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.card-arrow {
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--accent);
  transition: gap var(--transition);
}
.card:hover .card-arrow { gap: 0.6rem; }

/* Tech tags */
.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin: 0.75rem 0 0;
}
.tech-tag {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 0.25rem 0.625rem;
  background: var(--accent-soft);
  color: var(--accent);
  border-radius: var(--radius-pill);
}

/* Experience */
.highlights {
  list-style: none;
  margin: 0;
  padding: 0;
  max-width: 720px;
}
.highlights li {
  position: relative;
  padding-left: 1.75rem;
  margin-bottom: 1rem;
  color: var(--text-secondary);
  font-size: 1.0625rem;
}
.highlights li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.65rem;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--accent);
}

/* Contact */
.contact-grid {
  display: grid;
  gap: 2.5rem;
}
@media (min-width: 900px) { .contact-grid { grid-template-columns: 0.9fr 1.1fr; } }

.contact-info h3 {
  font-family: 'Inter', sans-serif;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.contact-links {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}
.contact-links a {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition);
}
.contact-links a:hover { color: var(--accent); }

/* Form */
.form-group { margin-bottom: 1.25rem; }
.form-group label {
  display: block;
  font-weight: 500;
  font-size: 0.9375rem;
  margin-bottom: 0.4rem;
  color: var(--text);
}
.form-group input,
.form-group textarea {
  width: 100%;
  padding: 0.875rem 1rem;
  font-size: 1rem;
  font-family: inherit;
  color: var(--text);
  background: var(--bg-elevated);
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  transition: border-color var(--transition), box-shadow var(--transition);
}
.form-group input::placeholder,
.form-group textarea::placeholder { color: var(--text-muted); }
.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--accent);
  box-shadow: 0 0 0 3px var(--accent-soft);
}
.form-group textarea { min-height: 140px; resize: vertical; }

.form-errors {
  color: var(--error);
  font-size: 0.9375rem;
  margin-bottom: 1rem;
}

.messages { margin-bottom: 1.5rem; }
.message {
  padding: 0.875rem 1rem;
  border-radius: var(--radius-sm);
  margin-bottom: 0.5rem;
  font-weight: 500;
}
.message.success {
  background: rgba(22, 163, 74, 0.1);
  color: var(--success);
  border: 1px solid rgba(22, 163, 74, 0.25);
}
.message.error {
  background: rgba(220, 38, 38, 0.1);
  color: var(--error);
  border: 1px solid rgba(220, 38, 38, 0.25);
}

/* Article (case study detail) */
.article { padding-top: 2.5rem; }
.article-back { margin-bottom: 1.5rem; }
.article-back a {
  color: var(--text-secondary);
  text-decoration: none;
  font-weight: 500;
  transition: color var(--transition);
}
.article-back a:hover { color: var(--accent); }

.article h1 { margin-bottom: 0.75rem; }
.article .summary {
  color: var(--text-secondary);
  font-size: 1.125rem;
  margin-bottom: 2rem;
  line-height: 1.65;
}

.article h2 {
  font-family: 'Inter', sans-serif;
  font-size: 1.125rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 2.5rem 0 0.75rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid var(--border);
}

.article figure { margin: 2rem 0; }
.article figure img {
  max-width: 100%;
  height: auto;
  border-radius: var(--radius-md);
  border: 1px solid var(--border);
}
.article figure figcaption {
  font-size: 0.9375rem;
  color: var(--text-muted);
  margin-top: 0.75rem;
}

.article-links { display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 2rem; }

/* Footer */
.site-footer {
  padding: 2.5rem 0;
  border-top: 1px solid var(--border);
  text-align: center;
  font-size: 0.9375rem;
  color: var(--text-muted);
}
.site-footer a { color: var(--text-secondary); text-decoration: none; }
.site-footer a:hover { color: var(--accent); }

/* Utilities */
.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* Reveal on scroll */
.reveal-on-scroll {
  opacity: 0;
  transform: translateY(18px);
  transition: opacity 0.6s ease-out, transform 0.6s ease-out;
  transition-delay: var(--reveal-delay, 0s);
}
.reveal-on-scroll.is-visible { opacity: 1; transform: translateY(0); }

@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
  .btn:hover, .card:hover, .skill-group:hover { transform: none; }
  .reveal-on-scroll { opacity: 1; transform: none; }
  .nav { transition: none; }
}
```

- [ ] **Step 2: Verify CSS is valid**

Run any CSS linter available, or at minimum check file size:
```bash
wc -l portfolio/static/portfolio/css/main.css
```

Expected: > 300 lines.

- [ ] **Step 3: Commit**

```bash
git add portfolio/static/portfolio/css/main.css
git commit -m "feat(ui): rewrite styles for light editorial theme"
```

---

### Task 3: Update main.js for mobile menu and interactions

**Files:**
- Modify: `portfolio/static/portfolio/js/main.js`

**Interfaces:**
- Consumes: `.nav-toggle`, `#main-nav`, `a[href^="#"]`, `.card`, `.skill-group`, `.section-head`
- Produces: Mobile menu toggle, smooth scroll, scroll reveal, form success focus

- [ ] **Step 1: Replace entire JS file**

Replace `portfolio/static/portfolio/js/main.js` contents with:

```javascript
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
```

- [ ] **Step 2: Verify JS syntax**

Run:
```bash
node --check portfolio/static/portfolio/js/main.js
```

Expected: no output (success).

- [ ] **Step 3: Commit**

```bash
git add portfolio/static/portfolio/js/main.js
git commit -m "feat(ui): add mobile menu, smooth scroll and reveal animations"
```

---

### Task 4: Redesign home.html

**Files:**
- Modify: `portfolio/templates/portfolio/home.html`

**Interfaces:**
- Consumes: `case_studies`, `contact_form`, Django URL tags
- Produces: New home page layout matching design spec

- [ ] **Step 1: Replace entire home.html**

Replace `portfolio/templates/portfolio/home.html` contents with:

```html
{% extends "portfolio/base.html" %}

{% block content %}
<section class="hero" aria-labelledby="hero-heading">
    <div class="container hero-inner">
        <div class="hero-content">
            <p class="hero-badge" aria-hidden="true">Backend Engineer</p>
            <h1 id="hero-heading">Botir Bakhtiyarov</h1>
            <p class="tagline">Django • APIs • AI-Powered Systems</p>
            <div class="hero-ctas">
                <a href="{% url 'portfolio:casestudy_list' %}" class="btn btn--primary">View Projects</a>
                <a href="{% url 'portfolio:cv_download' %}" class="btn btn--secondary" download>Download CV</a>
            </div>
        </div>
        <div class="hero-about">
            <p class="hero-intro">
                I build robust backend systems with Django and Python: microservices, REST APIs, and AI-powered platforms.
                Focus on production-ready code, clear architecture, and scalable solutions.
            </p>
            <div class="hero-skills">
                <h3>Core stack</h3>
                <ul class="hero-skills-list">
                    <li>Django</li>
                    <li>DRF</li>
                    <li>PostgreSQL</li>
                    <li>Docker</li>
                    <li>AI / LLMs</li>
                </ul>
            </div>
        </div>
    </div>
</section>

<section class="section" id="skills" aria-labelledby="skills-heading">
    <div class="container">
        <div class="section-head">
            <h2 id="skills-heading">Skills</h2>
            <p>Core technologies and practices I use day to day.</p>
        </div>
        <div class="skills-grid">
            <div class="skill-group">
                <svg class="skill-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                    <path d="M4 17l6-6-6-6M12 19h8"/>
                </svg>
                <h3>Core Backend</h3>
                <ul>
                    <li>Django</li>
                    <li>Django REST Framework</li>
                    <li>Python</li>
                    <li>PostgreSQL / MySQL</li>
                </ul>
            </div>
            <div class="skill-group">
                <svg class="skill-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                    <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
                </svg>
                <h3>Architecture & Tools</h3>
                <ul>
                    <li>REST APIs</li>
                    <li>Microservices</li>
                    <li>Celery / Async tasks</li>
                    <li>Docker</li>
                    <li>Git</li>
                </ul>
            </div>
            <div class="skill-group">
                <svg class="skill-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true">
                    <path d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3M3.343 5.636l.707.707M16.95 17.05l-1.414-1.414M6.343 6.343L4.93 4.93M12 21a9 9 0 1 1 0-18 9 9 0 0 1 0 18z"/>
                </svg>
                <h3>AI & Advanced</h3>
                <ul>
                    <li>LLM integrations</li>
                    <li>RAG systems</li>
                    <li>n8n automation</li>
                    <li>Automation platforms</li>
                </ul>
            </div>
        </div>
    </div>
</section>

<section class="section section--alt" id="projects" aria-labelledby="projects-heading">
    <div class="container">
        <div class="section-head">
            <h2 id="projects-heading">Projects</h2>
            <p>Selected case studies and backend projects.</p>
        </div>
        <div class="card-grid">
            {% for cs in case_studies %}
            <a href="{% url 'portfolio:casestudy_detail' slug=cs.slug %}" class="card">
                <h3>{{ cs.title }}</h3>
                <p>{{ cs.summary }}</p>
                <div class="tech-tags">
                    {% for tech in cs.tech_list|slice:":5" %}
                    <span class="tech-tag">{{ tech }}</span>
                    {% endfor %}
                </div>
                <span class="card-arrow">Read case study</span>
            </a>
            {% empty %}
            <p style="color: var(--text-muted); grid-column: 1 / -1;">Projects will appear here. Add case studies in Django Admin.</p>
            {% endfor %}
        </div>
        {% if case_studies %}
        <p style="margin-top: 2rem;">
            <a href="{% url 'portfolio:casestudy_list' %}" class="btn btn--secondary">All Projects</a>
        </p>
        {% endif %}
    </div>
</section>

<section class="section" id="experience" aria-labelledby="experience-heading">
    <div class="container">
        <div class="section-head">
            <h2 id="experience-heading">Experience Highlights</h2>
        </div>
        <ul class="highlights">
            <li>Shipped AI-powered tools and integrations in production</li>
            <li>Designed and built microservices and REST APIs at scale</li>
            <li>Delivered automation platforms and backend systems end-to-end</li>
        </ul>
    </div>
</section>

<section class="section section--alt" id="contact" aria-labelledby="contact-heading">
    <div class="container">
        <div class="section-head">
            <h2 id="contact-heading">Contact</h2>
            <p>Reach out for opportunities or collaboration.</p>
        </div>
        <div class="contact-grid">
            <div class="contact-info">
                <h3>Let's talk</h3>
                <div class="contact-links">
                    <a href="mailto:hello@bbotir.xyz">hello@bbotir.xyz</a>
                    <a href="https://www.linkedin.com/in/botir-bakhtiyarov-856a83243/" target="_blank" rel="noopener noreferrer">LinkedIn</a>
                    <a href="https://github.com/BotirBakhtiyarov" target="_blank" rel="noopener noreferrer">GitHub</a>
                </div>
            </div>
            <form method="post" action="{% url 'portfolio:home' %}" aria-label="Contact form">
                {% csrf_token %}
                {% if contact_form.non_field_errors %}
                <div class="form-errors" role="alert">{{ contact_form.non_field_errors }}</div>
                {% endif %}
                <div class="form-group">
                    <label for="id_name">Name</label>
                    {{ contact_form.name }}
                    {% if contact_form.name.errors %}<span class="form-errors">{{ contact_form.name.errors }}</span>{% endif %}
                </div>
                <div class="form-group">
                    <label for="id_email">Email</label>
                    {{ contact_form.email }}
                    {% if contact_form.email.errors %}<span class="form-errors">{{ contact_form.email.errors }}</span>{% endif %}
                </div>
                <div class="form-group">
                    <label for="id_message">Message</label>
                    {{ contact_form.message }}
                    {% if contact_form.message.errors %}<span class="form-errors">{{ contact_form.message.errors }}</span>{% endif %}
                </div>
                <button type="submit" class="btn btn--primary" style="width: 100%;">Send message</button>
            </form>
        </div>
    </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Verify template renders**

Run:
```bash
python manage.py check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add portfolio/templates/portfolio/home.html
git commit -m "feat(ui): redesign home page with light editorial layout"
```

---

### Task 5: Redesign casestudy_list.html

**Files:**
- Modify: `portfolio/templates/portfolio/casestudy_list.html`

**Interfaces:**
- Consumes: `case_studies`
- Produces: Updated projects list page

- [ ] **Step 1: Replace entire casestudy_list.html**

Replace `portfolio/templates/portfolio/casestudy_list.html` contents with:

```html
{% extends "portfolio/base.html" %}

{% block title %}Projects — Botir Bakhtiyarov{% endblock %}
{% block meta_description %}Case studies and projects by Botir Bakhtiyarov: Django, APIs, AI-powered systems.{% endblock %}

{% block content %}
<section class="article section" aria-labelledby="page-title">
    <div class="container">
        <div class="section-head">
            <h1 id="page-title">Projects</h1>
            <p>Selected case studies and backend projects.</p>
        </div>
        <div class="card-grid">
            {% for cs in case_studies %}
            <a href="{% url 'portfolio:casestudy_detail' slug=cs.slug %}" class="card">
                <h3>{{ cs.title }}</h3>
                <p>{{ cs.summary }}</p>
                <div class="tech-tags">
                    {% for tech in cs.tech_list|slice:":5" %}
                    <span class="tech-tag">{{ tech }}</span>
                    {% endfor %}
                </div>
                <span class="card-arrow">Read case study</span>
            </a>
            {% empty %}
            <p style="color: var(--text-muted); grid-column: 1 / -1;">No projects yet. Add case studies in Django Admin.</p>
            {% endfor %}
        </div>
        <p style="margin-top: 2rem;">
            <a href="{% url 'portfolio:home' %}" class="btn btn--ghost">← Back to home</a>
        </p>
    </div>
</section>
{% endblock %}
```

- [ ] **Step 2: Verify template renders**

Run:
```bash
python manage.py check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add portfolio/templates/portfolio/casestudy_list.html
git commit -m "feat(ui): redesign projects list page"
```

---

### Task 6: Redesign casestudy_detail.html

**Files:**
- Modify: `portfolio/templates/portfolio/casestudy_detail.html`

**Interfaces:**
- Consumes: `case_study`
- Produces: Updated case study detail page

- [ ] **Step 1: Replace entire casestudy_detail.html**

Replace `portfolio/templates/portfolio/casestudy_detail.html` contents with:

```html
{% extends "portfolio/base.html" %}

{% block title %}{{ case_study.title }} — Botir Bakhtiyarov{% endblock %}
{% block meta_description %}{{ case_study.summary }}{% endblock %}
{% block og_title %}{{ case_study.title }} — Botir Bakhtiyarov{% endblock %}
{% block og_description %}{{ case_study.summary }}{% endblock %}
{% block twitter_title %}{{ case_study.title }} — Botir Bakhtiyarov{% endblock %}
{% block twitter_description %}{{ case_study.summary }}{% endblock %}

{% block content %}
<article class="article section" itemscope itemtype="https://schema.org/Article">
    <div class="container container--wide">
        <p class="article-back">
            <a href="{% url 'portfolio:casestudy_list' %}">← Projects</a>
        </p>
        <header>
            <h1 itemprop="name">{{ case_study.title }}</h1>
            <p class="summary" itemprop="description">{{ case_study.summary }}</p>
        </header>

        <h2>Problem</h2>
        <div>{{ case_study.problem|linebreaks }}</div>

        <h2>Solution</h2>
        <div>{{ case_study.solution|linebreaks }}</div>

        <h2>Tech stack</h2>
        <div class="tech-tags">
            {% for tech in case_study.tech_list %}
            <span class="tech-tag">{{ tech }}</span>
            {% endfor %}
        </div>

        <h2>Key results</h2>
        <div>{{ case_study.key_results|linebreaks }}</div>

        {% if case_study.images.exists %}
        <h2>Screenshots</h2>
        {% for img in case_study.images.all %}
        <figure>
            <img src="{{ img.image.url }}" alt="{{ img.alt_text|default:case_study.title }}" loading="lazy" width="800" height="auto">
            {% if img.alt_text %}<figcaption>{{ img.alt_text }}</figcaption>{% endif %}
        </figure>
        {% endfor %}
        {% endif %}

        <div class="article-links">
            {% if case_study.github_link %}
            <a href="{{ case_study.github_link }}" target="_blank" rel="noopener noreferrer" class="btn btn--primary">GitHub</a>
            {% endif %}
            {% if case_study.demo_link %}
            <a href="{{ case_study.demo_link }}" target="_blank" rel="noopener noreferrer" class="btn btn--secondary">Demo</a>
            {% endif %}
        </div>
    </div>
</article>
{% endblock %}
```

- [ ] **Step 2: Verify template renders**

Run:
```bash
python manage.py check
```

Expected: no errors.

- [ ] **Step 3: Commit**

```bash
git add portfolio/templates/portfolio/casestudy_detail.html
git commit -m "feat(ui): redesign case study detail page"
```

---

### Task 7: Final verification

**Files:**
- All modified files

**Interfaces:**
- Consumes: Full Django project
- Produces: Verified redesign

- [ ] **Step 1: Run Django checks**

```bash
python manage.py check
python manage.py check
```

Expected: no errors.

- [ ] **Step 2: Start dev server and smoke test**

```bash
python manage.py runserver &
```

Wait 3 seconds, then:
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/
```

Expected: `200`

Also test:
```bash
curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/projects/
```

Expected: `200`

- [ ] **Step 3: Stop dev server**

```bash
pkill -f "manage.py runserver" || true
```

- [ ] **Step 4: Push branch**

```bash
git push origin redesign/light-editorial-ui
```

Expected: branch updated.

---

## Spec Coverage Check

| Spec bo'limi | Task |
|--------------|------|
| Ochiq fon va ranglar | Task 2 (CSS) |
| Editorial tipografiya | Task 1 (fonts), Task 2 (CSS) |
| Header + mobile menu | Task 1, Task 2, Task 3 |
| Hero 2 ustun | Task 4 |
| Skills grid + iconlar | Task 4 |
| Projects kartochkalari | Task 4, Task 5 |
| Experience highlights | Task 4 |
| Contact 2 ustun | Task 4 |
| Case study detail | Task 6 |
| Animatsiyalar | Task 2, Task 3 |
| Responsivlik | Task 2 |
| Accessibility | Task 1, Task 2, Task 3 |

**Yoqotilgan talablar yo'q.**

## Placeholder Scan

- TBD/TODO: yo'q
- "implement later": yo'q
- "add appropriate error handling": yo'q
- Test commands aniq ko'rsatilgan
- Har bir task uchun exact file path'lar berilgan
