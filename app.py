# =============================================================================
# SUMAN INFO — FLASK APPLICATION ENTRY POINT
# -----------------------------------------------------------------------------
# Run with:  python app.py
# All brandable content lives in config.py — edit that file, not this one,
# for company info, contact details, products, team data, and admin login.
#
# Contact form messages are saved to a local SQLite database
# (contact_submissions.db) and can be viewed at /admin after logging in
# with the credentials set in config.py -> ADMIN.
# =============================================================================
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

import config
import db

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

db.init_db()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


# =============================================================================
# SUMAN INFO — FLASK APPLICATION ENTRY POINT
# -----------------------------------------------------------------------------
# Run with:  python app.py
#
# All LIVE site content (company info, contact details, theme colors,
# products, team) is stored in the SQLite database and is fully editable
# from the Admin Panel at /admin — see db.py. config.py only supplies the
# one-time seed values (first run) plus the admin username/password/secret
# key.
# =============================================================================
from datetime import datetime
from functools import wraps

from flask import Flask, render_template, request, jsonify, session, redirect, url_for

import config
import db

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

db.init_db()
db.seed_defaults({
    "company": config.COMPANY,
    "contact": config.CONTACT,
    "theme": config.THEME,
    "nav_links": config.NAV_LINKS,
    "products": config.PRODUCTS,
    "team": config.TEAM,
})

# Icon choices available to product cards (drawn in static/img/icons.svg).
PRODUCT_ICONS = ["cloud", "cube", "chart", "shield", "bolt", "mobile"]


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin_login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def index():
    """Render the single-page site using live content from the database."""
    return render_template(
        "index.html",
        company=db.get_setting("company", config.COMPANY),
        contact=db.get_setting("contact", config.CONTACT),
        nav_links=db.get_setting("nav_links", config.NAV_LINKS),
        products=db.get_products(),
        team=db.get_team(),
        # Theme colors are fixed (not admin-editable for now) — see config.py THEME.
        theme=config.THEME,
        year=datetime.now().year,
    )


@app.route("/contact", methods=["POST"])
def contact():
    """Handle the contact form submission (AJAX). Validates and saves it to SQLite.

    View submitted messages at /admin/messages (login required).
    TODO: Optionally also hook this up to a real email service (SMTP, SendGrid, etc.).
    """
    data = request.get_json(silent=True) or request.form

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    phone = (data.get("phone") or "").strip()
    message = (data.get("message") or "").strip()

    errors = {}
    if not name:
        errors["name"] = "Please enter your name."
    if not email or "@" not in email or "." not in email.split("@")[-1]:
        errors["email"] = "Please enter a valid email address."
    digits = "".join(ch for ch in phone if ch.isdigit())
    if not phone or len(digits) < 7:
        errors["phone"] = "Please enter a valid contact number."
    if not message or len(message) < 10:
        errors["message"] = "Message should be at least 10 characters."

    if errors:
        return jsonify({"success": False, "errors": errors}), 400

    db.add_submission(name, email, phone, message, datetime.utcnow().isoformat())
    app.logger.info("New contact submission from %s <%s> (%s)", name, email, phone)

    return jsonify({"success": True, "message": "Thanks! We'll be in touch soon."})


# =============================================================================
# ADMIN PANEL — login required for everything under /admin
# =============================================================================
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("is_admin"):
        return redirect(url_for("admin_dashboard"))

    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""
        if username == config.ADMIN["username"] and password == config.ADMIN["password"]:
            session.clear()
            session["is_admin"] = True
            session["admin_username"] = username
            next_url = request.args.get("next") or url_for("admin_dashboard")
            return redirect(next_url)
        error = "Invalid username or password."

    return render_template("admin_login.html", company=db.get_setting("company", config.COMPANY), error=error)


@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/admin")
@login_required
def admin_dashboard():
    return render_template(
        "admin_dashboard.html",
        company=db.get_setting("company", config.COMPANY),
        admin_username=session.get("admin_username"),
        unread_count=db.count_unread(),
        product_count=len(db.get_products()),
        team_count=len(db.get_team()),
    )


# ---------- Contact messages ----------
@app.route("/admin/messages")
@login_required
def admin_messages():
    return render_template(
        "admin_messages.html",
        company=db.get_setting("company", config.COMPANY),
        submissions=db.get_all_submissions(),
        admin_username=session.get("admin_username"),
    )


@app.route("/admin/messages/<int:submission_id>/read", methods=["POST"])
@login_required
def admin_mark_read(submission_id):
    db.mark_as_read(submission_id)
    return redirect(url_for("admin_messages"))


@app.route("/admin/messages/<int:submission_id>/delete", methods=["POST"])
@login_required
def admin_delete(submission_id):
    db.delete_submission(submission_id)
    return redirect(url_for("admin_messages"))


# ---------- Site settings (company / contact / theme) ----------
@app.route("/admin/settings", methods=["GET", "POST"])
@login_required
def admin_settings():
    if request.method == "POST":
        form = request.form

        company = {
            "name": form.get("company_name", "").strip(),
            "short_name": form.get("short_name", "").strip(),
            "logo_initials": form.get("logo_initials", "").strip(),
            "tagline": form.get("tagline", "").strip(),
            "founded_year": int(form.get("founded_year") or 0),
            "about": form.get("about", "").strip(),
            "stats": [
                {
                    "label": form.get(f"stat_label_{i}", "").strip(),
                    "value": int(form.get(f"stat_value_{i}") or 0),
                    "suffix": form.get(f"stat_suffix_{i}", "").strip(),
                }
                for i in range(4)
                if form.get(f"stat_label_{i}", "").strip()
            ],
        }
        contact = {
            "email": form.get("email", "").strip(),
            "phone": form.get("phone", "").strip(),
            "address": form.get("address", "").strip(),
            "socials": {
                "twitter": form.get("twitter", "").strip(),
                "linkedin": form.get("linkedin", "").strip(),
                "github": form.get("github", "").strip(),
                "instagram": form.get("instagram", "").strip(),
            },
        }

        db.set_setting("company", company)
        db.set_setting("contact", contact)
        return redirect(url_for("admin_settings", saved=1))

    return render_template(
        "admin_settings.html",
        company=db.get_setting("company", config.COMPANY),
        contact=db.get_setting("contact", config.CONTACT),
        admin_username=session.get("admin_username"),
        saved=request.args.get("saved"),
    )


# ---------- Products ----------
@app.route("/admin/products")
@login_required
def admin_products():
    return render_template(
        "admin_products.html",
        company=db.get_setting("company", config.COMPANY),
        products=db.get_products(),
        admin_username=session.get("admin_username"),
    )


def _product_form_to_dict(form):
    return {
        "name": form.get("name", "").strip(),
        "tagline": form.get("tagline", "").strip(),
        "description": form.get("description", "").strip(),
        "price": form.get("price", "").strip(),
        "icon": form.get("icon", "cube").strip(),
        "color": form.get("color", "#5b8cff").strip(),
        "sort_order": int(form.get("sort_order") or 0),
    }


@app.route("/admin/products/new", methods=["GET", "POST"])
@login_required
def admin_product_new():
    if request.method == "POST":
        db.add_product(_product_form_to_dict(request.form))
        return redirect(url_for("admin_products"))
    return render_template(
        "admin_product_form.html",
        company=db.get_setting("company", config.COMPANY),
        product=None,
        icons=PRODUCT_ICONS,
        admin_username=session.get("admin_username"),
    )


@app.route("/admin/products/<int:product_id>/edit", methods=["GET", "POST"])
@login_required
def admin_product_edit(product_id):
    product = db.get_product(product_id)
    if not product:
        return redirect(url_for("admin_products"))
    if request.method == "POST":
        db.update_product(product_id, _product_form_to_dict(request.form))
        return redirect(url_for("admin_products"))
    return render_template(
        "admin_product_form.html",
        company=db.get_setting("company", config.COMPANY),
        product=product,
        icons=PRODUCT_ICONS,
        admin_username=session.get("admin_username"),
    )


@app.route("/admin/products/<int:product_id>/delete", methods=["POST"])
@login_required
def admin_product_delete(product_id):
    db.delete_product(product_id)
    return redirect(url_for("admin_products"))


# ---------- Team ----------
@app.route("/admin/team")
@login_required
def admin_team():
    return render_template(
        "admin_team.html",
        company=db.get_setting("company", config.COMPANY),
        team=db.get_team(),
        admin_username=session.get("admin_username"),
    )


def _team_form_to_dict(form):
    return {
        "name": form.get("name", "").strip(),
        "role": form.get("role", "").strip(),
        "initials": form.get("initials", "").strip().upper()[:3],
        "color": form.get("color", "#5b8cff").strip(),
        "sort_order": int(form.get("sort_order") or 0),
    }


@app.route("/admin/team/new", methods=["GET", "POST"])
@login_required
def admin_team_new():
    if request.method == "POST":
        db.add_team_member(_team_form_to_dict(request.form))
        return redirect(url_for("admin_team"))
    return render_template(
        "admin_team_form.html",
        company=db.get_setting("company", config.COMPANY),
        member=None,
        admin_username=session.get("admin_username"),
    )


@app.route("/admin/team/<int:member_id>/edit", methods=["GET", "POST"])
@login_required
def admin_team_edit(member_id):
    member = db.get_team_member(member_id)
    if not member:
        return redirect(url_for("admin_team"))
    if request.method == "POST":
        db.update_team_member(member_id, _team_form_to_dict(request.form))
        return redirect(url_for("admin_team"))
    return render_template(
        "admin_team_form.html",
        company=db.get_setting("company", config.COMPANY),
        member=member,
        admin_username=session.get("admin_username"),
    )


@app.route("/admin/team/<int:member_id>/delete", methods=["POST"])
@login_required
def admin_team_delete(member_id):
    db.delete_team_member(member_id)
    return redirect(url_for("admin_team"))


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

