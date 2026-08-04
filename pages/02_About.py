import streamlit as st

cart_count = len(st.session_state.get("cart", []))
nav_html = f'''
<div style="display:flex; justify-content:center; gap:10px; margin:12px 0;">
  <a href="/" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Home</a>
  <a href="/?script=/pages/02_About.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.7);">About</a>
  <a href="/?script=/pages/03_Products.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Products</a>
  <a href="/?script=/pages/04_Contact.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Contact</a>
  <a href="/?script=/pages/05_Cart.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(212,175,55,0.12);">Cart ({cart_count})</a>
</div>
'''
st.markdown(nav_html, unsafe_allow_html=True)

st.title("About LuthuliScents")
st.subheader("Welcome to LUTHULISCENTS 🧴")
st.write("We create perfumes from scratch and blend timeless notes that feel elegant, bold, and memorable.")
st.markdown(
    """
    - We make our perfumes from scratch.
    - These scents are inspired by a mix of rich, modern fragrance notes.
    - Our perfumes suit all genders as long as you love beautiful scents.
    - We offer male, female, and unisex fragrances.
    - You can wear them for daily use, special occasions, or whenever you want to stand out.
    """
)
