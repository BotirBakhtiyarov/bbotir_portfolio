# bbotir.xyz Portfolio UI Redesign — Design Spec

## 1. Maqsad va kontekst

Mavjud portfolio (https://github.com/BotirBakhtiyarov/bbotir_portfolio) dark glassmorphism uslubida yaratilgan. Foydalanuvchi bu ko'rinishni "eski" deb baholab, boshqa, professional va ochiq-yorug' UI talab qilmoqda.

**Tanlangan yo'nalish:** Clean Light Editorial — ochiq fon, katta whitespace, editorial tipografiya, professional va HR-do'ston.

## 2. Joriy holat

- **Backend:** Django 5.x, `CaseStudy` va `CaseStudyImage` modellari
- **Sahifalar:** Home, Projects list, Project detail, CV download, Admin
- **Frontend:** Django templates + bitta `main.css` + bitta `main.js`
- **Xususiyatlar:** Contact form, SEO meta teglari, schema.org, responsive

## 3. Dizayn tizimi (Design System)

### 3.1 Ranglar

| Token | Qiymat | Qo'llanishi |
|-------|--------|-------------|
| `--bg` | `#fafafa` | Sahifa foni |
| `--bg-elevated` | `#ffffff` | Kartochkalar, header |
| `--bg-subtle` | `#f4f4f6` | Alternativ sectionlar |
| `--text` | `#111118` | Asosiy matn |
| `--text-secondary` | `#4b5563` | Ikkinchi darajali matn |
| `--text-muted` | `#6b7280` | Yorliqlar, kichik matn |
| `--accent` | `#1e3a8a` | Asosiy accent (deep indigo) |
| `--accent-hover` | `#1e40af` | Hover holatidagi accent |
| `--accent-soft` | `#dbeafe` | Yengil accent foni |
| `--border` | `#e5e7eb` | Chegaralar |
| `--border-strong` | `#d1d5db` | Faol chegaralar |
| `--success` | `#16a34a` | Muvaffaqiyat xabarlari |
| `--error` | `#dc2626` | Xatolik xabarlari |

### 3.2 Tipografiya

- **Sarlavhalar:** `Playfair Display`, serif, 700-800
- **Asosiy matn:** `Inter`, sans-serif, 400-600
- **Kod/tehnik yorliqlar:** `JetBrains Mono`, monospace

O'lchamlar:
- H1 Hero: `clamp(2.75rem, 6vw, 4.5rem)`, line-height 1.1
- H2 Section: `clamp(1.75rem, 3vw, 2.25rem)`, line-height 1.2
- H3 Card: `1.25rem`, line-height 1.3
- Body: `1.0625rem` (17px), line-height 1.7
- Small: `0.9375rem`

### 3.3 Soyalar va radiuslar

- `--shadow-sm`: `0 1px 2px rgba(0,0,0,0.04)`
- `--shadow-md`: `0 4px 12px rgba(0,0,0,0.06)`
- `--shadow-lg`: `0 12px 32px rgba(0,0,0,0.08)`
- `--radius-sm`: `8px`
- `--radius-md`: `16px`
- `--radius-lg`: `24px`
- `--radius-pill`: `999px`

### 3.4 Container va grid

- Maksimal kenglik: `1140px`
- Padding: `0 1.5rem` (mobile), `0 2rem` (desktop)
- Section padding: `5rem 0` (desktop), `3.5rem 0` (mobile)
- Grid: CSS Grid + Flexbox, gap `1.5rem`

## 4. Sahifa tuzilishi

### 4.1 Home (`home.html`)

1. **Header** — sticky, oq fon, pastki border, logotip chapda, navigatsiya o'ngda
2. **Hero** — 2 ustun (desktop):
   - Chap: badge "Backend Engineer", H1 ism, tagline, 2 ta CTA
   - O'ng: qisqa bio (2-3 gap), asosiy ko'nikmalar ro'yxati
3. **Skills** — 3 ustunli grid, har bir karta:
   - Kichik iconka (SVG)
   - Guruh nomi
   - Texnologiyalar ro'yxati
4. **Projects** — 2 ustunli project kartochkalari:
   - Sarlavha
   - Qisqa tavsif
   - Tech stack teglari
   - "Read case study" linki
5. **Experience** — timeline yoki highlights ro'yxati
6. **Contact** — 2 ustun:
   - Chapda: email, LinkedIn, GitHub
   - O'ngda: contact form
7. **Footer** — minimal, copyright + link

### 4.2 Projects list (`casestudy_list.html`)

- Sahifa sarlavhasi va tavsifi
- 2 ustunli project grid
- "Back to home" tugmasi

### 4.3 Project detail (`casestudy_detail.html`)

- "← Projects" ortga qaytish linki
- Sarlavha + summary
- Problem / Solution / Tech stack / Key results bo'limlari
- Screenshots (agar mavjud bo'lsa)
- GitHub / Demo tugmalari

## 5. Komponentlar

### 5.1 Header

```
[bbotir.xyz]        [Home] [Projects] [Contact] [CV]
```

- Sticky, `top: 0`, `z-index: 100`
- Fon: oq + `backdrop-filter: blur(12px)`
- Mobile: hamburger menyuga o'zgaradi

### 5.2 Hero

```
[Backend Engineer]        I build robust backend
Botir Bakhtiyarov         systems with Django and
Django • APIs • AI         Python. Focus on production-
[View Projects]            ready code, clear architecture,
[Download CV]              and scalable solutions.
```

- Hero fon: subtle gradient yoki bo'sh
- CTA: birinchi primary (to'q ko'k), ikkinchi ghost/outline

### 5.3 Skill card

- Oq fon, 1px border, radius 16px
- Kichik indigo iconka
- Kategoriya nomi kichik uppercase
- Texnologiyalar ro'yxati

### 5.4 Project card

- Oq fon, border, radius 16px
- Hover: `translateY(-4px)`, shadow oshadi, border dark-blue
- Tech stack teglari (pill shaklida)

### 5.5 Contact form

- Inputlar: oq fon, border, radius 12px
- Focus: indigo border + yengil glow
- Tugma: to'liq kenglikdagi primary

## 6. Animatsiyalar va interaksiyalar

| Element | Effekt | Maqsad |
|---------|--------|--------|
| Hero matni | `fade-in + translateY(12px)` | Birinchi taassurot |
| Sectionlar | `reveal-on-scroll` | Silliq paydo bo'lish |
| Kartochkalar | hover: ko'tarilish + shadow | Interaktivlik |
| Tugmalar | hover: background o'zgarishi | Feedback |
| Linklar | hover: indigo rang | Navigatsiya |
| Form input | focus: border + glow | Kiritish holati |

Barcha animatsiyalar `prefers-reduced-motion` ni hurmat qiladi.

## 7. Responsivlik

| Breakpoint | O'zgarishlar |
|------------|--------------|
| < 640px | Barcha grid 1 ustun, hero 1 ustun, kichik shriftlar |
| 640px - 1024px | Skills 2 ustun, projects 2 ustun |
| > 1024px | Skills 3 ustun, hero 2 ustun, contact 2 ustun |

## 8. Accessibility

- Semantic HTML (`header`, `main`, `section`, `article`)
- ARIA label'lar formalar va tugmalar uchun
- Skip-to-content linki
- Focus state'larni saqlash
- Rang kontrasti WCAG AA ga javob beradi
- `prefers-reduced-motion` qo'llab-quvvatlanadi

## 9. Texnik yondashuv

### 9.1 O'zgartiriladigan fayllar

- `portfolio/templates/portfolio/base.html` — umumiy layout
- `portfolio/templates/portfolio/home.html` — home sahifasi
- `portfolio/templates/portfolio/casestudy_list.html` — projectlar ro'yxati
- `portfolio/templates/portfolio/casestudy_detail.html` — project detail
- `portfolio/static/portfolio/css/main.css` — barcha stillar
- `portfolio/static/portfolio/js/main.js` — JS (scroll reveal, mobile menu)

### 9.2 Saqlanadigan narsalar

- Django backend, modellar, formalar, view'lar
- URL structure
- Admin panel
- Contact form funksionalligi
- CV yuklash
- SEO meta teglari va schema.org
- Favicon va statik fayllar

### 9.3 Qo'shiladigan assetlar

- Yangi Google Fonts (Inter, Playfair Display)
- SVG iconlar (skills uchun)
- Mobil menyuga kerakli JS

## 10. Chiqarib tashlanadigan narsalar (Out of scope)

- Yangi backend model qo'shish
- Yangi sahifa qo'shish (blog, etc.)
- React/Vue kabi frontend framework o'tkazish
- CMS integratsiyasi
- SEO'dan tashqari marketing vositalari

## 11. Muvaffaqiyat mezoni

- Sayt ochiq-yorug', professional ko'rinishga ega bo'ladi
- Barcha mavjud funksiyalar ishlaydi
- Mobil qurilmalarda to'g'ri ko'rinadi
- Contact form xatolarsiz ishlaydi
- Admin paneli o'zgarmaydi

## 12. Keyingi qadam

Ushbu dizayn tasdiqlangach, `writing-plans` skill orqali implementatsiya rejasini tuzish va keyin kodni yozish.
