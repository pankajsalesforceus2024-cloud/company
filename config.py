# =============================================================================
# SUMAN INFO — SEED / DEFAULT CONFIGURATION
# -----------------------------------------------------------------------------
# IMPORTANT: These values are only used ONCE, to seed the SQLite database the
# very first time the app runs (when its tables are empty). After that, the
# live site content (company info, contact details, theme, products, team) is
# stored in the database and is fully editable from the Admin Panel at
# /admin — NOT by editing this file. Changing values here later will have no
# effect on an already-seeded database.
#
# Only ADMIN and SECRET_KEY below are still read directly from this file on
# every request (they are not editable from the UI, for security).
# =============================================================================

# -----------------------------------------------------------------------------
# 1) COMPANY / BRAND  -->  Seed values only (see note above). Edit live via
#    Admin Panel → Site Settings after first run.
# -----------------------------------------------------------------------------
COMPANY = {
    "name": "Suman Info",
    "short_name": "Suman",           # Used in compact/mobile logo
    "logo_initials": "SI",           # Used in the generated SVG logo mark
    "tagline": "Engineering Tomorrow's Software, Today.",
    "founded_year": 2016,
    "about": (
        "Suman Info is a software engineering studio that designs, builds, and "
        "scales digital products for ambitious teams. From cloud-native platforms "
        "to immersive 3D web experiences, we turn complex problems into elegant, "
        "reliable software."
    ),
    "stats": [
        {"label": "Years of Experience", "value": 8, "suffix": "+"},
        {"label": "Projects Delivered", "value": 120, "suffix": "+"},
        {"label": "Happy Clients", "value": 60, "suffix": "+"},
        {"label": "Team Experts", "value": 25, "suffix": "+"},
    ],
}

# -----------------------------------------------------------------------------
# 1b) ADMIN PANEL  -->  Change this password before deploying anywhere public!
#     Contact form messages are viewable at /admin after logging in here.
#     SECRET_KEY signs the login session cookie — replace with a long random
#     value in production (e.g. `python -c "import secrets; print(secrets.token_hex(32))"`).
# -----------------------------------------------------------------------------
ADMIN = {
    "username": "admin",
    "password": "changeme123",   # TODO: change this before deploying
}
SECRET_KEY = "dev-secret-key-change-me"  # TODO: replace in production

# -----------------------------------------------------------------------------
# 2) CONTACT DETAILS  -->  Seed values only. Edit live via Admin Panel →
#    Site Settings after first run.
# -----------------------------------------------------------------------------
CONTACT = {
    "email": "hello@sumaninfo.example",
    "phone": "+1 (555) 010-2030",
    "address": "123 Innovation Drive, Tech Park, Bengaluru, India",
    "socials": {
        "twitter": "https://twitter.com/",
        "linkedin": "https://linkedin.com/",
        "github": "https://github.com/",
        "instagram": "https://instagram.com/",
    },
}

# -----------------------------------------------------------------------------
# 3) NAVIGATION  -->  Add/remove sections here; IDs must match section ids
#    in templates/index.html.
# -----------------------------------------------------------------------------
NAV_LINKS = [
    {"label": "Home", "id": "hero"},
    {"label": "About", "id": "about"},
    {"label": "Services", "id": "services"},
    {"label": "Team", "id": "team"},
    {"label": "Contact", "id": "contact"},
]

# -----------------------------------------------------------------------------
# 4) SERVICES / PRODUCTS  -->  Seed values only. Edit live via Admin Panel →
#    Products after first run. "icon" selects a self-drawn SVG glyph from
#    static/img/icons.svg (no external images used — see ASSETS.md).
# -----------------------------------------------------------------------------
PRODUCTS = [
    {
        "name": "CloudForge Platform",
        "tagline": "Cloud Infrastructure",
        "description": "A managed cloud-native platform for deploying, scaling, "
                        "and monitoring microservices with zero-downtime releases.",
        "price": "$499/mo",
        "icon": "cloud",
        "color": "#5b8cff",
    },
    {
        "name": "PixelSuite 3D",
        "tagline": "Web 3D Engine",
        "description": "A drag-and-drop toolkit for building interactive 3D "
                        "product configurators and web experiences.",
        "price": "$299/mo",
        "icon": "cube",
        "color": "#7c5cff",
    },
    {
        "name": "DataPulse Analytics",
        "tagline": "Business Intelligence",
        "description": "Real-time dashboards and predictive analytics to help "
                        "teams make faster, data-driven decisions.",
        "price": "$199/mo",
        "icon": "chart",
        "color": "#22d3c8",
    },
    {
        "name": "SecureGate Auth",
        "tagline": "Identity & Security",
        "description": "Enterprise-grade authentication, SSO, and access "
                        "control that plugs into any stack in minutes.",
        "price": "$149/mo",
        "icon": "shield",
        "color": "#ff7a5c",
    },
    {
        "name": "SwiftAPI Gateway",
        "tagline": "API Management",
        "description": "A high-performance API gateway with rate-limiting, "
                        "analytics, and developer-friendly documentation.",
        "price": "$249/mo",
        "icon": "bolt",
        "color": "#ffb545",
    },
    {
        "name": "MobileFlow SDK",
        "tagline": "Mobile Development",
        "description": "Cross-platform SDK for building buttery-smooth native "
                        "mobile experiences with a single codebase.",
        "price": "$179/mo",
        "icon": "mobile",
        "color": "#4dd67a",
    },
]

# -----------------------------------------------------------------------------
# 5) TEAM  -->  Seed values only. Edit live via Admin Panel → Team after
#    first run. Avatars are generated locally (initials + gradient) so no
#    external/copyrighted photos are required — see ASSETS.md.
# -----------------------------------------------------------------------------
TEAM = [
    {"name": "Ananya Sharma", "role": "Founder & CEO", "initials": "AS", "color": "#5b8cff"},
    {"name": "Rohan Mehta", "role": "CTO", "initials": "RM", "color": "#7c5cff"},
    {"name": "Priya Nair", "role": "Lead 3D Engineer", "initials": "PN", "color": "#22d3c8"},
    {"name": "Karan Verma", "role": "Product Designer", "initials": "KV", "color": "#ff7a5c"},
    {"name": "Isha Kapoor", "role": "Backend Engineer", "initials": "IK", "color": "#ffb545"},
    {"name": "Dev Patel", "role": "DevOps Engineer", "initials": "DP", "color": "#4dd67a"},
]

# -----------------------------------------------------------------------------
# 6) THEME  -->  Seed values only. Edit live via Admin Panel → Site Settings
#    after first run.
# -----------------------------------------------------------------------------
THEME = {
    "primary": "#5b8cff",
    "secondary": "#7c5cff",
    "accent": "#22d3c8",
    "dark_bg": "#0a0e17",
}
