import streamlit as st

cart_count = len(st.session_state.get("cart", []))
nav_html = f'''
<div style="display:flex; justify-content:center; gap:10px; margin:12px 0;">
  <a href="/" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.7);">Home</a>
  <a href="/?script=/pages/02_About.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">About</a>
  <a href="/?script=/pages/03_Products.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Products</a>
  <a href="/?script=/pages/04_Contact.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Contact</a>
  <a href="/?script=/pages/05_Cart.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(212,175,55,0.12);">Cart ({cart_count})</a>
</div>
'''
st.markdown(nav_html, unsafe_allow_html=True)

st.title("✨ LUTHULISCENTS")
st.subheader("Discover your signature scent")
st.image("../logo.jpeg", width=220)

st.markdown("""
<div style="text-align:center; padding:28px 24px 20px; margin:0 auto 18px; max-width:980px; border:1px solid rgba(212, 175, 55, 0.3); border-radius:24px; background:linear-gradient(135deg, rgba(255,255,255,0.08), rgba(212,175,55,0.12)); box-shadow:0 12px 30px rgba(0,0,0,0.24);">
    <div style="display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(212,175,55,0.16); color:#f2d27b; font-size:0.8rem; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:10px;">Luxury fragrance house</div>
    <h1 style="margin:0 0 8px; color:#f4d98d; font-size:2.3rem; font-weight:700;">✨ GOLDEN LUXURY PERFUMES</h1>
    <p style="margin:0; color:#f6e8c9; font-size:1.05rem; line-height:1.6;">Experience our hand-crafted, artisan scents designed to feel timeless, bold, and unforgettable.</p>
</div>
""", unsafe_allow_html=True)

st.write("Browse our collection, learn more about our story, and place your order in a few simple steps.")
