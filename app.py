"""LuthuliScents — Golden Luxury Perfumes.

Composition root: page config, global styling, session init and navigation.
Each screen lives in its own module under ``views/``.
"""

import streamlit as st
from streamlit_option_menu import option_menu

from core.session import count, init
from core.styles import inject_css
from products import SOCIAL_LINKS

from views import about, cart, contact, home, shop

st.set_page_config(
    page_title="LuthuliScents — Golden Luxury Perfumes",
    page_icon="logo.jpeg",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
init()

with st.sidebar:
    st.image("logo.jpeg", width=120)
    cart_count = count()
    page = option_menu(
        menu_title=None,
        options=["Home", "Shop", "Cart", "About", "Contact"],
        default_index=0,
        key="main_nav",
        styles={
            "container": {"background-color": "transparent", "padding": "0"},
            "nav-link": {"color": "#7A7263", "font-size": "0.8rem", "text-align": "left"},
            "nav-link-selected": {"background-color": "transparent", "color": "#221E17"},
        },
    )
    if cart_count:
        st.caption(f"Cart: {cart_count} item{'s' if cart_count != 1 else ''}")
    st.markdown("<hr>", unsafe_allow_html=True)
    st.link_button("WhatsApp", SOCIAL_LINKS["WhatsApp"])

page = (page or "Home").split(" (")[0]

if page == "Home":
    home.render()
elif page == "Shop":
    shop.render()
elif page == "Cart":
    cart.render()
elif page == "About":
    about.render()
elif page == "Contact":
    contact.render()
