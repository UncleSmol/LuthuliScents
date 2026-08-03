"""About page: brand story, values and social links."""

import streamlit as st

from core.ui import page_header, quote, render_footer, section_title
from products import SOCIAL_LINKS


def render() -> None:
    page_header()
    st.title(":material/eco:  About LuthuliScents")

    st.markdown(
        """
        ### Our story
        LuthuliScents started with a simple belief: **smelling expensive shouldn't
        mean spending a fortune.** We hand-craft every perfume from scratch, using
        quality fragrance oils that linger, layered to feel complex and refined.

        Our scents are inspired by everyday life in South Africa — crisp apple
        orchards, warm woody evenings, and bold florals — and blended to suit
        **every gender and every occasion**.
        """
    )

    section_title("diamond", "Our values")
    for title, desc in [
        ("Artisan craft", "Each batch is small, blended and matured by hand."),
        ("Lasting power", "We obsess over longevity so one spray carries you through the day."),
        ("Honest pricing", "Luxury quality without the designer markup."),
    ]:
        quote(title + " — " + desc, "LuthuliScents")

    section_title("filter_vintage", "Scents at a glance")
    fam_data = {
        "Female": "Soft florals, rosy and romantic.",
        "Male": "Bold, woody and grounded.",
        "Unisex": "Crisp, fresh and for everyone.",
    }
    for fam, desc in fam_data.items():
        st.markdown(f"**{fam}:** {desc}")

    section_title("share", "Follow us")
    items = list(SOCIAL_LINKS.items())
    cols1 = st.columns(3)
    for col, (name, url) in zip(cols1, items[:3]):
        with col:
            st.link_button(name, url)
    cols2 = st.columns(3)
    for col, (name, url) in zip(cols2, items[3:]):
        with col:
            st.link_button(name, url)

    render_footer()
