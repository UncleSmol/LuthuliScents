"""LuthuliScents — Golden Luxury Perfumes.

Composition root: page config, global styling, session init and navigation.
Each screen lives in its own module under ``pages/``.
"""

import streamlit as st
from streamlit_option_menu import option_menu

from core.session import count, init
from core.styles import inject_css
from products import SOCIAL_LINKS

from pages import about, cart, contact, home, shop

st.set_page_config(
    page_title="Golden Luxury Perfumes — LuthuliScents",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

inject_css()
init()

with st.sidebar:
    st.image("logo.jpeg", width=140)
    cart_count = count()
    cart_label = f"Cart ({cart_count})" if cart_count else "Cart"
    page = option_menu(
        menu_title="LuthuliScents",
        options=["Home", "Shop", cart_label, "About", "Contact"],
        icons=["house-fill", "bag-fill", "cart-fill", "stars", "envelope-fill"],
        default_index=0,
        key="main_nav",
        styles={
            "container": {"background-color": "#1a0f08", "border": "1px solid rgba(212,175,55,.2)", "border-radius": "14px"},
            "icon": {"color": "#c9a24b"},
            "nav-link": {"color": "#f7e7c6", "font-size": "0.95rem", "text-align": "left"},
            "nav-link-selected": {"background-color": "#c9a24b", "color": "#1a140f"},
        },
    )
    st.markdown("---")
    st.markdown("**Need help?**")
    st.link_button("Chat on WhatsApp", SOCIAL_LINKS["WhatsApp"], icon=":material/chat:")

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
