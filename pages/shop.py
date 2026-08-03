"""Shop page: full catalog with scent-family filtering."""

import streamlit as st

from core.ui import render_footer, render_product
from products import FAMILIES, PRODUCTS


def render() -> None:
    st.title(":material/storefront:  The Collection")
    st.caption("Filter by scent family. Every bottle is R180 for 50ml.")

    fam_col, _, _ = st.columns([2, 1, 4])
    with fam_col:
        family = st.selectbox("Scent family", FAMILIES, key="family_filter")

    filtered = [p for p in PRODUCTS if family == "All" or p["family"] == family]

    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, p in zip(cols, filtered[i:i + 3]):
            with col:
                render_product(p, key_prefix="shop")

    st.info(":material/local_fire_department:  Winter Sale: Get **free shipping** on all orders over R500!", icon=":material/local_fire_department:")

    render_footer()
