"""Contact page: enquiry form, FAQs and direct contacts."""

import urllib.parse

import streamlit as st

from core.icons import icon
from core.ui import render_footer, section_heading

WHATSAPP_NUMBER = "27692380796"
CONTACT_EMAIL = "sthandiweluthuli322@gmail.com"

SUBJECTS = [
    "General question",
    "Bulk / wholesale order",
    "Custom fragrance",
    "Order support",
    "Other",
]


def _wa_link(name: str, subject: str, message: str, email: str, phone: str) -> str:
    text = (
        f"Hi LuthuliScents! My name is {name}.\n"
        f"Subject: {subject}\n"
        f"Message: {message}"
        + (f"\nContact: {email}" if email else "")
        + (f" / {phone}" if phone else "")
    )
    return f"https://wa.me/{WHATSAPP_NUMBER}?text={urllib.parse.quote(text)}"


def render() -> None:
    st.title("Contact")
    st.markdown(
        "Questions about a scent, a bulk order or a custom fragrance idea — "
        "send us a message and we will get back to you."
    )

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Your name")
        email = st.text_input("Your email")
        phone = st.text_input("Phone number (optional)")
        subject = st.selectbox("Subject", SUBJECTS)
    with c2:
        message = st.text_area("Message", height=190)

    if st.button("Send via WhatsApp", type="primary"):
        if not name.strip() or not message.strip():
            st.warning("Please add your name and a message.")
        else:
            st.success("Your message is ready to send.")
            st.link_button("Open WhatsApp", _wa_link(name, subject, message, email, phone))

    st.markdown("---")
    section_heading("Support", "Frequently asked questions")
    faqs = [
        ("How long does delivery take?", "Orders ship within 2 business days. Delivery typically takes 2–5 business days depending on your location."),
        ("Do your perfumes suit both men and women?", "Yes — we make female, male and unisex scents. Many of our favourites are unisex."),
        ("Are your perfumes made from scratch?", "Absolutely. Every batch is hand-blended and matured in our studio."),
        ("Do you offer discounts for bulk orders?", "Yes! For weddings, gifting or wholesale, contact us directly for a custom quote."),
    ]
    for q, a in faqs:
        with st.expander(q):
            st.write(a)

    st.markdown("---")
    section_heading("Reach us", "Direct contacts")
    st.markdown(
        f"""
        <p style="margin:8px 0;">{icon('mail', size='1.05rem', color='#A98A4C')}
        <a href="mailto:{CONTACT_EMAIL}" style="color:#221E17;">{CONTACT_EMAIL}</a></p>
        <p style="margin:8px 0;">{icon('chat', size='1.05rem', color='#A98A4C')}
        <a href="https://wa.me/{WHATSAPP_NUMBER}" style="color:#221E17;">+27 69 238 0796</a></p>
        """,
        unsafe_allow_html=True,
    )

    render_footer()
