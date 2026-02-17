# bbotir.xyz — Personal Portfolio

Minimal, HR-friendly portfolio for **Botir Bakhtiyarov**: Backend Engineer | Django • APIs • AI-Powered Systems.

- **Stack:** Django (backend) + simple HTML/CSS (no heavy frontend).
- **Features:** Hero, skills, dynamic projects (case studies from Admin), experience highlights, contact form, CV download, SEO-friendly URLs.

---

## Quick start (local)

```bash
cd bbotir_portfolio
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Site: http://127.0.0.1:8000/  
- Admin: http://127.0.0.1:8000/admin/

---

## Add your CV

Place your PDF in:

```
static/cv/Botir_Bakhtiyarov_CV.pdf
```

The "Download CV" button will serve this file.

---

## Projects (case studies)

All projects are managed in **Django Admin**:

1. Go to **Admin → Portfolio → Case studies**.
2. Add a case study: title, summary, problem, solution, tech stack, key results, optional GitHub/demo links, optional images (via inline).
3. Set **Order** and **Is published** as needed.

They appear on the home page and under **/projects/**.

---

## Contact form

The contact form sends email to the address set in settings. For local dev, emails are printed to the console. For production, set SMTP in `.env` (see `.env.example`).

---

## Deployment (Docker)

1. Copy `.env.example` to `.env` and set `DJANGO_SECRET_KEY`, `ALLOWED_HOSTS`, `CONTACT_EMAIL`, and email backend if needed.
2. Put your CV at `static/cv/Botir_Bakhtiyarov_CV.pdf`.
3. Run:

```bash
docker-compose up -d
```

The app is served on port 8000. Put a reverse proxy (e.g. Nginx/Caddy) in front for HTTPS and map the domain **bbotir.xyz**.

### Production checklist

- Set `DEBUG=False` and a strong `DJANGO_SECRET_KEY`.
- Set `ALLOWED_HOSTS=bbotir.xyz,www.bbotir.xyz`.
- Configure SMTP for the contact form.
- Optional: use PostgreSQL by changing `DATABASES` in `settings.py` and adding a `db` service in `docker-compose.yml`.
- Add analytics script in `portfolio/templates/portfolio/base.html` (placeholder comment is present).

---

## URL structure

| URL | Description |
|-----|-------------|
| `/` | Home (hero, skills, projects preview, experience, contact) |
| `/projects/` | All case studies |
| `/projects/<slug>/` | Case study detail |
| `/cv/` | Download CV PDF |
| `/admin/` | Django Admin |

---

## License

Private use. © Botir Bakhtiyarov.
