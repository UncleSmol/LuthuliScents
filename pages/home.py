"""Home page: masthead, hero, featured scents, brand statement, notes, VIP list."""

import streamlit as st

from core.ui import masthead, quote, render_footer, render_product, section_heading, statement
from products import PRODUCTS


def render() -> None:
    masthead()

    col_left, col_right = st.columns([1, 1.1], gap="large")
    with col_left:
        st.markdown("### Discover your signature scent")
        st.write(
            "Each bottle is hand-blended and matured in our studio. Our scents "
            "welcome every gender and carry you from morning to evening."
        )
        c1, c2 = st.columns(2)
        with c1:
            st.button("Shop the collection", type="primary", key="hero_shop")
        with c2:
            st.link_button("Order on Yoco", PRODUCTS[0]["pay_link"])
    with col_right:
        st.image("WhatsApp Image 2026-05-27 at 09.05.30.jpeg", width=430)

    statement(
        "Made from scratch, blended by hand and matured slowly — every bottle is "
        "crafted to smell far more expensive than it is.",
        mark="The house standard",
    )

    section_heading("The Collection", "Featured scents")
    featured = [p for p in PRODUCTS if p.get("featured")]
    for i in range(0, len(featured), 3):
        cols = st.columns(3)
        for col, p in zip(cols, featured[i:i + 3]):
            with col:
                render_product(p, key_prefix="home")

    section_heading("From our clients", "Notes & words")
    for text, who in [
        ("My Rosie carried me through an entire wedding day — one spray in the morning was enough.", "Thandeka M., Johannesburg"),
        ("A classy scent that easily passes for something three times the price.", "Bongani K., Durban"),
    ]:
        quote(text, who)

    st.markdown("---")
    section_heading("Stay in touch", "Join the VIP list")
    st.caption("Early access to new drops, restocks and private sales.")
    nl1, nl2, _ = st.columns([2, 1, 1])
    email = nl1.text_input("Email address", key="newsletter_email", placeholder="you@example.com")
    if nl2.button("Subscribe", key="newsletter_btn", type="primary"):
        if email and "@" in email:
            st.success("Welcome to the LuthuliScents VIP list.")
        else:
            st.warning("Please enter a valid email address.")

    render_footer()
