/* =============================================================================
   SUMAN INFO — UI INTERACTIVITY
   -----------------------------------------------------------------------
   Handles: loading screen, navbar scroll/mobile menu, smooth scrolling,
   scroll-reveal animations, animated stat counters, product card tilt
   effect, and the contact form (AJAX to /contact).
   ============================================================================= */

// ---------- Loading screen ----------
window.addEventListener("load", () => {
    const loader = document.getElementById("loader");
    setTimeout(() => loader && loader.classList.add("hidden"), 600);
});

// ---------- Navbar: scrolled state + mobile toggle ----------
const navbar = document.getElementById("navbar");
const navToggle = document.getElementById("navToggle");
const navLinksEl = document.getElementById("navLinks");

window.addEventListener("scroll", () => {
    navbar.classList.toggle("scrolled", window.scrollY > 40);
});

navToggle?.addEventListener("click", () => {
    navLinksEl.classList.toggle("open");
});

// ---------- Smooth scrolling for nav / CTA links ----------
document.querySelectorAll("[data-scroll]").forEach((link) => {
    link.addEventListener("click", (e) => {
        const href = link.getAttribute("href");
        if (!href || !href.startsWith("#")) return;
        const target = document.querySelector(href);
        if (!target) return;
        e.preventDefault();
        navLinksEl.classList.remove("open");
        target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
});

// ---------- Scroll-reveal for sections ----------
document.querySelectorAll(".section-heading, .about-grid, .product-card, .team-card, .contact-grid")
    .forEach((el) => el.setAttribute("data-reveal", ""));

const revealObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("in-view");
                revealObserver.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.15 }
);
document.querySelectorAll("[data-reveal]").forEach((el) => revealObserver.observe(el));

// ---------- Animated stat counters ----------
const counterObserver = new IntersectionObserver(
    (entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            const el = entry.target;
            const target = parseInt(el.getAttribute("data-count"), 10) || 0;
            const duration = 1400;
            const start = performance.now();
            function tick(now) {
                const progress = Math.min((now - start) / duration, 1);
                el.textContent = Math.floor(progress * target);
                if (progress < 1) requestAnimationFrame(tick);
                else el.textContent = target;
            }
            requestAnimationFrame(tick);
            counterObserver.unobserve(el);
        });
    },
    { threshold: 0.6 }
);
document.querySelectorAll(".stat-value").forEach((el) => counterObserver.observe(el));

// ---------- Product card 3D tilt-on-hover ----------
document.querySelectorAll(".product-card").forEach((card) => {
    card.addEventListener("mousemove", (e) => {
        const rect = card.getBoundingClientRect();
        const x = (e.clientX - rect.left) / rect.width - 0.5;
        const y = (e.clientY - rect.top) / rect.height - 0.5;
        card.style.transform = `perspective(700px) rotateX(${-y * 10}deg) rotateY(${x * 10}deg) translateY(-4px)`;
    });
    card.addEventListener("mouseleave", () => {
        card.style.transform = "perspective(700px) rotateX(0) rotateY(0) translateY(0)";
    });
    card.addEventListener("click", () => {
        card.style.transform = "perspective(700px) scale(0.97)";
        setTimeout(() => { card.style.transform = "perspective(700px) scale(1)"; }, 180);
    });
});

// ---------- Contact form (AJAX submit) ----------
const form = document.getElementById("contactForm");
const statusEl = document.getElementById("formStatus");

form?.addEventListener("submit", async (e) => {
    e.preventDefault();
    document.querySelectorAll(".form-error").forEach((el) => (el.textContent = ""));
    statusEl.textContent = "";
    statusEl.className = "form-status";

    const submitBtn = form.querySelector("button[type='submit']");
    submitBtn.disabled = true;
    const originalLabel = submitBtn.querySelector(".btn-label").textContent;
    submitBtn.querySelector(".btn-label").textContent = "Sending…";

    const payload = {
        name: form.name.value,
        email: form.email.value,
        phone: form.phone.value,
        message: form.message.value,
    };

    try {
        const res = await fetch("/contact", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const data = await res.json();

        if (res.ok && data.success) {
            statusEl.textContent = data.message;
            statusEl.classList.add("success");
            form.reset();
        } else if (data.errors) {
            Object.entries(data.errors).forEach(([field, msg]) => {
                const el = form.querySelector(`[data-error-for="${field}"]`);
                if (el) el.textContent = msg;
            });
            statusEl.textContent = "Please fix the errors above.";
            statusEl.classList.add("error");
        }
    } catch (err) {
        statusEl.textContent = "Something went wrong. Please try again later.";
        statusEl.classList.add("error");
    } finally {
        submitBtn.disabled = false;
        submitBtn.querySelector(".btn-label").textContent = originalLabel;
    }
});
