# Suman Info — Interactive 3D Website

A complete, production-ready, interactive 3D animated website built with
**Flask** (Python) + **Three.js**. Ships with a placeholder company name/logo
("Suman Info") and dummy product/team data — everything is designed to be
swapped out for your real branding in minutes.

## Features

- Full-screen interactive 3D hero scene (Three.js) — drag to rotate, mouse
  parallax, hover glow, and click-to-burst particle animation
- Smooth-scrolling single-page navigation with responsive mobile menu
- About section with animated stat counters
- Services/Products grid with 3D tilt-on-hover cards, driven by configurable
  data
- Team section with generated (no external images) avatar cards
- Contact form with client + server-side validation (AJAX to Flask backend)
- Contact messages persisted in a local **SQLite** database
- Password-protected **Admin Panel** (`/admin`) to view/manage contact messages
- Scroll-reveal animations, loading screen, fully responsive layout
- 100% royalty-free / self-authored visual assets (see `ASSETS.md`)

## Requirements

- Python 3.9+

## Setup & Run

```powershell
# 1. Create and activate a virtual environment (recommended)
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Then open **http://localhost:5000** in your browser.

## Project Structure

```
SumanInfo/
├── app.py                       # Flask app & routes (/, /contact, /admin/*)
├── db.py                         # SQLite data layer (contact submissions)
├── config.py                     # ALL brandable content + admin credentials
├── requirements.txt
├── ASSETS.md                      # Asset source & license documentation
├── contact_submissions.db          # SQLite database (auto-created on first run)
├── templates/
│   ├── index.html                 # Single-page site template
│   ├── admin_login.html            # Admin login form
│   └── admin_dashboard.html         # Admin inbox (view/mark-read/delete)
└── static/
    ├── css/style.css              # Styles + CSS variables for theme colors
    ├── js/
    │   ├── scene.js                # Three.js 3D hero scene
    │   └── main.js                  # Nav, scroll, tilt cards, contact form
    └── img/
        └── icons.svg                # Self-authored SVG icon sprite
```

## Where to Customize

| What to change                                            | File                                                         |
| --------------------------------------------------------- | ------------------------------------------------------------ |
| Company name, logo initials, tagline, about text, stats   | `config.py` → `COMPANY`                                      |
| Contact email/phone/address/socials                       | `config.py` → `CONTACT`                                      |
| Navigation links                                          | `config.py` → `NAV_LINKS`                                    |
| Products/services (name, description, price, icon, color) | `config.py` → `PRODUCTS`                                     |
| Team members (name, role, initials, color)                | `config.py` → `TEAM`                                         |
| Brand colors (primary/secondary/accent)                   | `config.py` → `THEME` **and** `static/css/style.css` `:root` |
| Favicon / logo mark                                       | inline SVG in `templates/index.html` `<head>`                |
| 3D hero scene behavior/colors                             | `static/js/scene.js`                                         |
| Contact form backend logic (e.g. real email sending)      | `app.py` → `/contact` route (see `TODO` comment)             |
| Admin username/password, session secret key               | `config.py` → `ADMIN`, `SECRET_KEY`                          |

No HTML/CSS/JS editing is required for basic rebranding — everything text
and data related flows from `config.py` into the page via Jinja templating.

## Contact Form Behavior & Where to See Messages

When a visitor submits the Contact form, the `/contact` POST route
validates the input and saves it to a local **SQLite** database file
(`contact_submissions.db`, auto-created on first run — see `db.py`).

**To read submitted messages/queries:**

1. Go to **http://localhost:5000/admin/login**
2. Log in with the credentials from `config.py` → `ADMIN` (default:
   `admin` / `changeme123` — **change this before deploying**)
3. You'll land on the **Admin Panel** (`/admin`) showing every message sent
   via the Contact form, with the sender's name, email, message, and
   timestamp. New/unread messages are highlighted; you can mark them read
   or delete them.

`/admin` and its sub-routes are protected by a login-required session check
(`app.py` → `login_required`) — visiting them without logging in redirects
to the login page.

To also forward messages by email, extend the `/contact` route in `app.py`
with a real email service (SMTP, SendGrid, etc.) in addition to the SQLite
write.

## Assets & Licensing

See [ASSETS.md](ASSETS.md) for a full list of every visual asset used and
its source/license. Summary: all icons, logo marks, and team avatars are
self-authored (drawn directly in SVG/CSS for this project) and Three.js is
loaded via CDN under the MIT License. No third-party photos or copyrighted
media are used anywhere in this project.

## Deploying

For production, run behind a WSGI server such as `waitress` or `gunicorn`
and disable Flask debug mode (`app.run(debug=False)`), e.g.:

```powershell
pip install waitress
waitress-serve --listen=0.0.0.0:8000 app:app
```
