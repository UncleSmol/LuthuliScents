"""Design system: global CSS injected once at app start."""

import streamlit as st

_FONT_IMPORT = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Poppins:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');
"""

_CSS = """
.stApp {
    background:
        radial-gradient(circle at 12% 8%, rgba(212,175,55,0.18), transparent 26%),
        radial-gradient(circle at 88% 92%, rgba(139,69,19,0.22), transparent 32%),
        linear-gradient(135deg, #120a06 0%, #23150c 45%, #462a15 100%);
    color: #f7e7c6;
    font-family: 'Poppins', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
    color: #f2d27b !important;
    letter-spacing: 0.5px;
}

.block-container {
    padding-top: 1.6rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}

div[data-testid="stSidebar"] { background: #1a0f08; }

/* ---------- Material Symbols icons ---------- */
.material-symbols-rounded {
    font-family: 'Material Symbols Rounded';
    font-weight: normal;
    font-style: normal;
    display: inline-block;
    line-height: 1;
    letter-spacing: normal;
    text-transform: none;
    vertical-align: middle;
    -webkit-font-smoothing: antialiased;
}
.ls-icon { margin-right: 4px; }

/* ---------- nav ---------- */
.nav-pills .nav-link {
    color: #f7e7c6 !important;
    border-radius: 999px !important;
    margin: 0 4px;
    font-weight: 500;
    transition: all .2s ease;
}
.nav-pills .nav-link.active {
    background: linear-gradient(135deg, #c9a24b, #f2d27b) !important;
    color: #1a140f !important;
}

/* ---------- buttons ---------- */
.stButton > button, .stFormSubmitButton > button {
    background: linear-gradient(135deg, #3a2a1d, #5a3a21);
    color: #f8ead2;
    border: 1px solid #c9a24b;
    border-radius: 999px;
    font-weight: 500;
    transition: all .2s ease;
    box-shadow: 0 6px 16px rgba(0,0,0,.18);
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    background: linear-gradient(135deg, #c9a24b, #f2d27b) !important;
    color: #1a140f !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #c9a24b, #f2d27b);
    color: #1a140f;
    border: none;
}
.stLinkButton > a {
    background: linear-gradient(135deg, #3a2a1d, #5a3a21);
    color: #f8ead2 !important;
    border: 1px solid #c9a24b;
    border-radius: 999px;
    font-weight: 500;
    transition: all .2s ease;
    box-shadow: 0 6px 16px rgba(0,0,0,.18);
}
.stLinkButton > a:hover {
    background: linear-gradient(135deg, #c9a24b, #f2d27b) !important;
    color: #1a140f !important;
    transform: translateY(-1px);
}

/* ---------- inputs ---------- */
.stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"] > div,
.stTextArea textarea {
    background: rgba(255,255,255,0.05) !important;
    color: #f8ead2 !important;
    border: 1px solid #c9a24b !important;
    border-radius: 10px !important;
}

/* ---------- containers ---------- */
div[data-testid="stExpander"] {
    border: 1px solid rgba(212,175,55,.22);
    border-radius: 16px;
    background: rgba(255,255,255,.03);
}
.stAlert, .stSuccess, .stWarning, .stInfo, .stError { border-radius: 12px; }

img { border-radius: 16px; box-shadow: 0 14px 34px rgba(0,0,0,.28); }

/* ---------- hero ---------- */
.hero {
    text-align: center;
    padding: 46px 30px 40px;
    margin: 0 auto 26px;
    border: 1px solid rgba(212,175,55,.3);
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(255,255,255,.06), rgba(212,175,55,.13));
    box-shadow: 0 18px 44px rgba(0,0,0,.3);
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: "";
    position: absolute; top: -60%; left: -30%;
    width: 60%; height: 260%;
    background: linear-gradient(90deg, transparent, rgba(242,210,123,.14), transparent);
    transform: rotate(20deg);
    animation: sheen 7s linear infinite;
}
@keyframes sheen { 0% {left: -60%;} 100% {left: 130%;} }
.hero .eyebrow {
    display: inline-block; padding: 6px 16px; border-radius: 999px;
    background: rgba(212,175,55,.16); color: #f2d27b;
    font-size: .75rem; letter-spacing: .28em; text-transform: uppercase; margin-bottom: 12px;
}
.hero h1 { font-size: 2.8rem; margin: 0 0 10px; }
.hero p { font-size: 1.08rem; color: #f6e8c9; max-width: 640px; margin: 0 auto; line-height: 1.7; }

/* ---------- product cards ---------- */
.p-card {
    border: 1px solid rgba(212,175,55,.25);
    border-radius: 20px;
    padding: 16px;
    text-align: center;
    background: rgba(255,255,255,.045);
    box-shadow: 0 12px 28px rgba(0,0,0,.22);
    transition: transform .25s ease, box-shadow .25s ease;
    height: 100%;
}
.p-card:hover { transform: translateY(-6px); box-shadow: 0 22px 44px rgba(0,0,0,.34); }
.p-card img { width: 100%; height: 230px; object-fit: cover; border-radius: 14px; }
.p-badge {
    position: relative; top: 14px; z-index: 2; margin: -40px auto 0;
    width: fit-content; padding: 3px 12px; border-radius: 999px;
    background: linear-gradient(135deg, #c9a24b, #f2d27b); color: #1a140f;
    font-size: .72rem; font-weight: 600; letter-spacing: .06em;
}
.p-name { font-family: 'Playfair Display', serif; font-size: 1.25rem; color: #f2d27b; margin: 8px 0 2px; }
.p-family { font-size: .72rem; letter-spacing: .18em; text-transform: uppercase; color: #c9a24b; }
.p-tag { font-size: .86rem; color: #f6e8c9; margin: 6px 0; line-height: 1.5; }
.p-notes { font-size: .78rem; color: #d8c49a; margin: 4px 0; }
.p-price { font-size: 1.35rem; font-weight: 600; color: #f2d27b; margin: 8px 0; }

/* ---------- feature boxes ---------- */
.feature-box {
    border: 1px solid rgba(212,175,55,.22); border-radius: 18px; padding: 20px 16px;
    background: rgba(255,255,255,.04); text-align: center; height: 100%;
}
.feature-box .icon { font-size: 2rem; color: #f2d27b; margin-bottom: 8px; }
.feature-box .ft { font-family: 'Playfair Display', serif; font-size: 1.05rem; color: #f2d27b; margin: 6px 0 4px; }
.feature-box .fd { font-size: .82rem; color: #e6d5ab; line-height: 1.55; }

/* ---------- quotes ---------- */
.quote {
    border-left: 3px solid #c9a24b; padding: 10px 18px; margin: 10px 0;
    background: rgba(255,255,255,.03); border-radius: 0 12px 12px 0;
    color: #f6e8c9; font-style: italic;
}
.quote .who { font-style: normal; font-size: .8rem; color: #c9a24b; margin-top: 6px; }

/* ---------- footer ---------- */
.footer {
    margin-top: 40px; padding: 26px 20px; text-align: center;
    border-top: 1px solid rgba(212,175,55,.25);
    color: #c9b688; font-size: .85rem;
}
.footer a { color: #f2d27b; text-decoration: none; margin: 0 8px; }
"""


def inject_css() -> None:
    st.markdown(f"<style>{_FONT_IMPORT}\n{_CSS}</style>", unsafe_allow_html=True)
