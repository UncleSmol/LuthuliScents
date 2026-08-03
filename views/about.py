"""About page: brand story, values and social links."""

import streamlit as st

from core.ui import masthead, render_footer, section_heading
from products import SOCIAL_LINKS


def render() -> None:
    masthead()
    st.title("About LuthuliScents")

    st.markdown(
        """
        LuthuliScents began with a simple belief: smelling expensive should not
        mean spending a fortune. Every perfume is hand-crafted from scratch,
        using quality fragrance oils layered to feel complex and refined.

        Our scents are inspired by everyday life in South Africa — crisp apple
        orchards, warm woody evenings and bold florals — and blended to suit
        every gender and every occasion.
        """
    )

    section_heading("Our approach", "Values")
    for title, desc in [
        ("Artisan craft", "Each batch is small, blended and matured by hand."),
        ("Lasting power", "One spray carries you through the day."),
        ("Honest pricing", "Luxury quality without the designer markup."),
    ]:
        st.markdown(f"**{title}** — {desc}")

    section_heading("The range", "Scents at a glance")
    fam_data = {
        "Female": "Soft florals, rosy and romantic.",
        "Male": "Bold, woody and grounded.",
        "Unisex": "Crisp, fresh and for everyone.",
    }
    for fam, desc in fam_data.items():
        st.markdown(f"**{fam}** — {desc}")

    section_heading("Stay connected", "Follow us")
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
