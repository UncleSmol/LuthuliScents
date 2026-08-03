"""Reusable UI building blocks shared across pages (minimal luxury style)."""

import base64

import streamlit as st

from core.session import add
from products import SOCIAL_LINKS


@st.cache_data(show_spinner=False)
def img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def masthead() -> None:
    st.markdown(
        """
        <div class="masthead">
            <div class="eyebrow">Luxury Fragrance House</div>
            <h1>Golden Luxury Perfumes</h1>
            <p>Hand-crafted artisan scents, blended from scratch and made to last.
            Luxury quality, without the luxury markup.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_heading(label: str, title: str) -> None:
    st.markdown(
        f'<div class="sec-head"><div class="label">{label}</div><h2>{title}</h2></div>',
        unsafe_allow_html=True,
    )


def statement(text: str, mark: str | None = None) -> None:
    inner = f'<span class="mark">{mark}</span> {text}' if mark else text
    st.markdown(f'<div class="statement">{inner}</div>', unsafe_allow_html=True)


def product_card(p: dict) -> str:
    badge = f'<div class="p-badge">{p["badge"]}</div>' if p.get("badge") else ""
    return f"""
    <div class="p-card">
        <img src="data:image/jpeg;base64,{img_b64(p['image'])}" alt="{p['name']}">
        {badge}
        <div class="p-name">{p['name']}</div>
        <div class="p-family">{p['family']} &middot; {p['size']}</div>
        <div class="p-notes">{p['notes']}</div>
        <div class="p-price">R{p['price']:.2f}</div>
    </div>
    """


def render_product(p: dict, key_prefix: str) -> None:
    st.markdown(product_card(p), unsafe_allow_html=True)
    st.markdown('<div style="height:14px;"></div>', unsafe_allow_html=True)
    b1, b2 = st.columns(2)
    with b1:
        st.button("Add to cart", key=f"{key_prefix}_add_{p['key']}", on_click=add, args=(p["key"],))
    with b2:
        st.link_button("Order now", p["pay_link"])


def quote(text: str, who: str) -> None:
    st.markdown(
        f'<div class="quote">{text}<div class="who">{who}</div></div>',
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    links = "".join(
        f'<a href="{url}" target="_blank">{name}</a>' for name, url in SOCIAL_LINKS.items()
    )
    st.markdown(
        f"""
        <div class="footer">
            <div class="brand">LUTHULISCENTS</div>
            <div class="links">{links}</div>
            <div class="fine">Golden Luxury Perfumes &middot; Hand-made in South Africa &middot; © 2026</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
