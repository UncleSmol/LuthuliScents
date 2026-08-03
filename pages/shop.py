"""Shop page: full catalog with scent-family filtering."""

import streamlit as st

from core.ui import render_footer, render_product
from products import FAMILIES, PRODUCTS


def render() -> None:
    st.title("The Collection")
    st.caption("Every bottle is R180 for 50ml. Filter by scent family.")

    fam_col, _, _ = st.columns([2, 1, 4])
    with fam_col:
        family = st.selectbox("Scent family", FAMILIES, key="family_filter")

    filtered = [p for p in PRODUCTS if family == "All" or p["family"] == family]

    for i in range(0, len(filtered), 3):
        cols = st.columns(3)
        for col, p in zip(cols, filtered[i:i + 3]):
            with col:
                render_product(p, key_prefix="shop")

    st.caption("Winter sale: free shipping on all orders over R500.")

    render_footer()
