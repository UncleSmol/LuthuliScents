"""Design system: global CSS injected once at app start.

Minimal luxury aesthetic — ivory palette, serif display type, generous
whitespace, restrained gold accents. No emojis, sparse iconography.
"""

import streamlit as st

_FONT_IMPORT = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');
"""

_CSS = """
.stApp {
    background: #FAF7F0;
    color: #221E17;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Playfair Display', serif;
    color: #1F1B14 !important;
    letter-spacing: .01em;
}

a { color: #221E17; }

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 1160px;
}

div[data-testid="stSidebar"] { background: #F4F0E6; }

/* ---------- navigation ---------- */
.nav-pills .nav-link {
    color: #7A7263 !important;
    font-size: .8rem !important;
    letter-spacing: .1em !important;
    text-transform: uppercase !important;
    padding: 10px 14px !important;
    border-radius: 0 !important;
    border-bottom: 2px solid transparent;
    transition: color .2s ease;
}
.nav-pills .nav-link:hover { color: #221E17 !important; background: transparent !important; }
.nav-pills .nav-link.active {
    color: #221E17 !important;
    background: transparent !important;
    border-bottom-color: #A98A4C;
}

/* ---------- buttons ---------- */
.stButton > button, .stFormSubmitButton > button, .stLinkButton > a {
    background: transparent !important;
    color: #221E17 !important;
    border: 1px solid #C9BEA6 !important;
    border-radius: 2px !important;
    font-size: .76rem !important;
    letter-spacing: .16em !important;
    text-transform: uppercase !important;
    font-weight: 500 !important;
    padding: .6rem 1.5rem !important;
    box-shadow: none !important;
    transition: background .2s ease, color .2s ease, border-color .2s ease !important;
}
.stButton > button *, .stFormSubmitButton > button *, .stLinkButton > a * {
    color: inherit !important;
}
.stButton > button:hover, .stFormSubmitButton > button:hover, .stLinkButton > a:hover {
    background: #221E17 !important;
    color: #FAF7F0 !important;
    border-color: #221E17 !important;
}
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] {
    background: #221E17 !important;
    color: #FAF7F0 !important;
    border-color: #221E17 !important;
}
.stButton > button[kind="primary"] * , .stFormSubmitButton > button[kind="primary"] * {
    color: inherit !important;
}
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover {
    background: #A98A4C !important;
    border-color: #A98A4C !important;
    color: #FAF7F0 !important;
}

/* ---------- inputs ---------- */
.stTextInput input, .stNumberInput input, .stTextArea textarea {
    background: transparent !important;
    color: #221E17 !important;
    border: 1px solid #E3DBC8 !important;
    border-radius: 2px !important;
}
.stTextInput input:focus, .stNumberInput input:focus, .stTextArea textarea:focus {
    border-color: #A98A4C !important;
    box-shadow: none !important;
}
.stSelectbox div[data-baseweb="select"] > div {
    background: transparent;
    border: 1px solid #E3DBC8;
    border-radius: 2px;
    color: #221E17;
}

/* ---------- containers ---------- */
div[data-testid="stExpander"] {
    border: 1px solid #E7E0D0;
    border-radius: 8px;
    background: #FFFFFF;
}
.stAlert, .stSuccess, .stWarning, .stInfo, .stError {
    background: #FFFFFF;
    border: 1px solid #E7E0D0;
    border-radius: 6px;
    color: #221E17;
}

img { border-radius: 8px; box-shadow: 0 8px 24px rgba(31,27,20,.08); }

hr { border: none; border-top: 1px solid #E7E0D0; margin: 36px 0; }

/* ---------- masthead ---------- */
.masthead {
    text-align: center;
    padding: 60px 24px 44px;
    margin: 0 0 40px;
    border-bottom: 1px solid #E7E0D0;
}
.masthead .eyebrow {
    font-size: .68rem;
    letter-spacing: .36em;
    text-transform: uppercase;
    color: #A98A4C;
    margin-bottom: 18px;
}
.masthead h1 { font-size: 2.6rem; margin: 0 0 16px; font-weight: 600; }
.masthead p {
    color: #7A7263;
    font-size: 1rem;
    max-width: 560px;
    margin: 0 auto;
    line-height: 1.8;
    font-weight: 300;
}

/* ---------- section headings ---------- */
.sec-head { margin: 52px 0 30px; text-align: center; }
.sec-head .label {
    font-size: .66rem;
    letter-spacing: .34em;
    text-transform: uppercase;
    color: #A98A4C;
    margin-bottom: 10px;
}
.sec-head h2 { font-size: 1.8rem; margin: 0; font-weight: 600; }

/* ---------- statement ---------- */
.statement {
    margin: 56px auto 16px;
    max-width: 720px;
    text-align: center;
    border-top: 1px solid #E7E0D0;
    border-bottom: 1px solid #E7E0D0;
    padding: 44px 24px;
    color: #4A4438;
    font-size: 1.02rem;
    line-height: 2;
    font-weight: 300;
}
.statement .mark { color: #A98A4C; }

/* ---------- product cards ---------- */
.p-card { text-align: center; }
.p-card img {
    width: 100%;
    height: 320px;
    object-fit: cover;
    border-radius: 8px;
    transition: transform .3s ease;
}
.p-card:hover img { transform: translateY(-4px); }
.p-badge {
    display: inline-block;
    margin-top: 16px;
    padding: 3px 12px;
    border: 1px solid #D9C9A5;
    border-radius: 999px;
    color: #A98A4C;
    font-size: .6rem;
    letter-spacing: .2em;
    text-transform: uppercase;
}
.p-name { font-family: 'Playfair Display', serif; font-size: 1.15rem; color: #221E17; margin: 16px 0 2px; }
.p-family { font-size: .66rem; letter-spacing: .24em; text-transform: uppercase; color: #A98A4C; }
.p-notes { font-size: .8rem; color: #7A7263; margin: 10px 0; line-height: 1.6; }
.p-price { font-size: 1.02rem; font-weight: 500; color: #221E17; margin: 12px 0; }

/* ---------- quotes ---------- */
.quote {
    border-left: 1px solid #C9BEA6;
    padding: 4px 0 4px 22px;
    margin: 22px 0;
    color: #4A4438;
    font-size: .95rem;
    font-style: italic;
    line-height: 1.8;
}
.quote .who {
    font-style: normal;
    font-size: .72rem;
    letter-spacing: .14em;
    text-transform: uppercase;
    color: #A98A4C;
    margin-top: 10px;
}

/* ---------- footer ---------- */
.footer {
    margin-top: 56px;
    padding: 36px 20px;
    text-align: center;
    border-top: 1px solid #E7E0D0;
    color: #7A7263;
    font-size: .8rem;
    letter-spacing: .03em;
}
.footer .brand { font-family: 'Playfair Display', serif; font-size: 1rem; color: #221E17; letter-spacing: .1em; }
.footer .links { margin: 16px 0; }
.footer a {
    color: #221E17;
    text-decoration: none;
    margin: 0 12px;
    font-size: .72rem;
    letter-spacing: .12em;
    text-transform: uppercase;
}
.footer a:hover { color: #A98A4C; }
.footer .fine { color: #A39A87; font-size: .74rem; margin-top: 14px; }

/* ---------- material symbols (sparingly) ---------- */
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
.ls-icon { margin-right: 6px; }
"""


def inject_css() -> None:
    st.markdown(f"<style>{_FONT_IMPORT}\n{_CSS}</style>", unsafe_allow_html=True)
