"""LuthuliScents — Golden Luxury Perfumes.

Composition root: page config, global styling, session init and navigation.
Each screen lives in its own module under ``views/``.
"""

import streamlit as st
from streamlit_option_menu import option_menu

from core.scroll import install_scroll_observer, mark_page
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

NAV_OPTIONS = ["Home", "Shop", "Cart", "About", "Contact"]

nav_index = st.session_state.get("_nav_index", 0)

with st.sidebar:
    st.image("logo.jpeg", width=120)
    cart_count = count()
    page = option_menu(
        menu_title=None,
        options=["Home", "Shop", f"Cart ({cart_count})" if cart_count else "Cart", "About", "Contact"],
        default_index=nav_index,
        key="main_nav",
        styles={
            "container": {"background-color": "transparent", "padding": "0"},
            "nav-link": {"color": "#7A7263", "font-size": "0.8rem", "text-align": "left"},
            "nav-link-selected": {"background-color": "transparent", "color": "#221E17"},
        },
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.link_button("WhatsApp", SOCIAL_LINKS["WhatsApp"])

page = (page or "Home").split(" (")[0]
if page in NAV_OPTIONS:
    st.session_state["_nav_index"] = NAV_OPTIONS.index(page)

if "_booted" in st.session_state:
    if "_scroll_obs" not in st.session_state:
        install_scroll_observer()
        st.session_state["_scroll_obs"] = True
else:
    st.session_state["_booted"] = True
mark_page(page)

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
