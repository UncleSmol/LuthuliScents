"""Session state management: the shopping cart."""

import streamlit as st

from products import PRODUCTS


def init() -> None:
    """Initialise the cart the first time the app runs in a session."""
    if "cart" not in st.session_state:
        st.session_state.cart = {}


def product_map() -> dict:
    return {p["key"]: p for p in PRODUCTS}


def items() -> list:
    """Return [(product, qty), ...] for the current cart."""
    pm = product_map()
    return [(pm[k], q) for k, q in st.session_state.get("cart", {}).items() if k in pm]


def count() -> int:
    return sum(st.session_state.get("cart", {}).values())


def subtotal(item_list: list | None = None) -> float:
    return round(sum(p["price"] * q for p, q in (item_list or items())), 2)


def add(key: str) -> None:
    st.session_state.cart[key] = st.session_state.cart.get(key, 0) + 1


def increment(key: str) -> None:
    add(key)


def decrement(key: str) -> None:
    if st.session_state.cart.get(key, 0) <= 1:
        st.session_state.cart.pop(key, None)
    else:
        st.session_state.cart[key] -= 1


def remove(key: str) -> None:
    st.session_state.cart.pop(key, None)


def clear() -> None:
    st.session_state.cart = {}
