"""Icon component built on the Material Symbols library (Google's official icon set).

Material Symbols is bundled with Streamlit, so no extra dependency is required.
It exposes two helpers:

* ``icon()``   -> returns an inline HTML <span> for use inside ``unsafe_allow_html`` blocks.
* ``st_icon()``-> renders a standalone icon into the app.
"""

import streamlit as st

_MATERIAL_CLASS = "material-symbols-rounded"


def icon(
    name: str,
    size: str = "1.25rem",
    color: str = "inherit",
    fill: int = 0,
    weight: int = 400,
    grad: int = 0,
) -> str:
    """Return inline HTML for a Material Symbols icon (snake_case name)."""
    return (
        f'<span class="{_MATERIAL_CLASS} ls-icon" aria-hidden="true" '
        f'style="font-size:{size};color:{color};'
        f"font-variation-settings:'FILL' {fill},'wght' {weight},'GRAD' {grad};\">"
        f"{name}</span>"
    )


def st_icon(
    name: str,
    size: str = "2rem",
    color: str = "#f2d27b",
    fill: int = 0,
    weight: int = 400,
    grad: int = 0,
) -> None:
    """Render a standalone Material Symbols icon."""
    st.markdown(
        f'<div style="line-height:0;">{icon(name, size, color, fill, weight, grad)}</div>',
        unsafe_allow_html=True,
    )


def icon_param(name: str) -> str:
    """Return a ``:material/name:`` shortcode for Streamlit's ``icon`` parameters."""
    return f":material/{name}:"
