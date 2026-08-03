"""Home page: hero, value props, signature collection, testimonials, newsletter."""

import streamlit as st

from core.ui import feature_box, page_header, quote, render_footer, render_product, section_title
from products import PRODUCTS


def render() -> None:
    page_header()

    hero_l, hero_r = st.columns([1, 1.2], gap="large")
    with hero_l:
        st.image("logo.jpeg", width=300)
        st.markdown(
            """
            ### 🌸 Discover your signature scent
            We make our perfumes **from scratch** — every bottle is blended and
            matured by hand. Our scents welcome all genders and fit every occasion.
            """
        )
        c1, c2 = st.columns(2)
        with c1:
            st.button("Shop the collection", type="primary", key="hero_shop", icon=":material/storefront:")
        with c2:
            st.link_button("Order on Yoco", PRODUCTS[0]["pay_link"], icon=":material/bolt:")
    with hero_r:
        st.image("WhatsApp Image 2026-05-27 at 09.05.30.jpeg", width=340)

    section_title("workspace_premium", "Why LuthuliScents?")
    fc1, fc2, fc3, fc4 = st.columns(4)
    for col, (ic, title, desc) in zip(
        [fc1, fc2, fc3, fc4],
        [
            ("brush", "Made from scratch", "Every scent is hand-blended and matured in-house."),
            ("timer", "Long-lasting", "Wear it from morning to night without re-spraying."),
            ("diversity_3", "For everyone", "Female, male and unisex collections for every style."),
            ("local_shipping", "Ships nationwide", "Tracked delivery across South Africa via trusted couriers."),
        ],
    ):
        with col:
            feature_box(ic, title, desc)

    section_title("star", "Signature collection")
    featured = [p for p in PRODUCTS if p.get("featured")]
    for i in range(0, len(featured), 3):
        cols = st.columns(3)
        for col, p in zip(cols, featured[i:i + 3]):
            with col:
                render_product(p, key_prefix="home")

    section_title("favorite", "What our customers say")
    for text, who in [
        ("“My Rosie has lasted an entire wedding day — I only re-sprayed once. Obsessed!”", "Thandeka M. — Johannesburg"),
        ("“Bought Sweetapple as a gift; the smell is so classy my sister won't share it.”", "Bongani K. — Durban"),
        ("“Finally a local scent that smells like it costs triple the price.”", "Anelisa S. — Cape Town"),
    ]:
        quote(text, who)

    st.markdown("---")
    st.subheader(":material/mail:  Join the VIP list")
    st.write("Get early access to new drops, restocks and secret sales.")
    nl1, nl2, nl3 = st.columns([2, 1, 1])
    email = nl1.text_input("Email address", key="newsletter_email", placeholder="you@example.com")
    if nl2.button("Subscribe", key="newsletter_btn", type="primary", icon=":material/notifications_active:"):
        if email and "@" in email:
            st.success("Welcome to the LuthuliScents VIP list! 🌸")
        else:
            st.warning("Please enter a valid email address.")

    render_footer()
