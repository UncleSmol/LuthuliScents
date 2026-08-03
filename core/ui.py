"""Reusable UI building blocks shared across pages."""

import base64

import streamlit as st

from core.icons import icon
from core.session import add
from products import SOCIAL_LINKS


@st.cache_data(show_spinner=False)
def img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def page_header() -> None:
    st.markdown(
        """
        <div class="hero">
            <div class="eyebrow">Luxury fragrance house</div>
            <h1>✨ Golden Luxury Perfumes</h1>
            <p>Hand-crafted, artisan scents designed to feel timeless, bold and
            unforgettable. Made from scratch, priced to smell expensive without
            spending much.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(icon_name: str, text: str) -> None:
    st.markdown(
        f"<h3 style='font-family: Playfair Display, serif;'>"
        f"{icon(icon_name, size='1.4rem', color='#f2d27b')} {text}</h3>",
        unsafe_allow_html=True,
    )


def product_card(p: dict) -> str:
    badge = f'<div class="p-badge">{p["badge"]}</div>' if p.get("badge") else ""
    return f"""
    <div class="p-card">
        <img src="data:image/jpeg;base64,{img_b64(p['image'])}" alt="{p['name']}">
        {badge}
        <div class="p-name">{p['name']}</div>
        <div class="p-family">{p['family']} · {p['size']}</div>
        <div class="p-tag">{p['tagline']}</div>
        <div class="p-notes">{p['notes']}</div>
        <div class="p-price">R{p['price']:.2f}</div>
    </div>
    """


def render_product(p: dict, key_prefix: str) -> None:
    st.markdown(product_card(p), unsafe_allow_html=True)
    st.markdown("---")
    b1, b2 = st.columns(2)
    with b1:
        st.button(
            "Add to cart",
            key=f"{key_prefix}_add_{p['key']}",
            icon=":material/add_shopping_cart:",
            on_click=add,
            args=(p["key"],),
        )
    with b2:
        st.link_button("Order now", p["pay_link"])


def feature_box(icon_name: str, title: str, desc: str) -> None:
    st.markdown(
        f'<div class="feature-box"><div class="icon">{icon(icon_name, size="2rem", color="#f2d27b")}</div>'
        f'<div class="ft">{title}</div><div class="fd">{desc}</div></div>',
        unsafe_allow_html=True,
    )


def quote(text: str, who: str) -> None:
    st.markdown(
        f'<div class="quote">{text}<div class="who">— {who}</div></div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    links = "".join(
        f'<a href="{url}" target="_blank">{name}</a>' for name, url in SOCIAL_LINKS.items()
    )
    st.markdown(
        f"""
        <div class="footer">
            <div>{icon('spa', size='1rem', color='#c9a24b')} <b>LUTHULISCENTS</b> — Golden Luxury Perfumes</div>
            <div style="margin-top:8px;">{links}</div>
            <div style="margin-top:10px;">© 2026 LuthuliScents · Hand-made with love in South Africa</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
