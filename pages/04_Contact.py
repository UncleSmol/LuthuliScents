import streamlit as st

cart_count = len(st.session_state.get("cart", []))
nav_html = f'''
<div style="display:flex; justify-content:center; gap:10px; margin:12px 0;">
  <a href="/" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Home</a>
  <a href="/?script=/pages/02_About.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">About</a>
  <a href="/?script=/pages/03_Products.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Products</a>
  <a href="/?script=/pages/04_Contact.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.7);">Contact</a>
  <a href="/?script=/pages/05_Cart.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(212,175,55,0.12);">Cart ({cart_count})</a>
</div>
'''
st.markdown(nav_html, unsafe_allow_html=True)

st.title("Contact Us")
st.write("We make long-lasting scents that feel luxurious without being overly expensive.")
st.write("Follow us:")
st.link_button("TikTok", "https://www.tiktok.com/@sthandiwe386?is_from_webapp=1&sender_device=pc")
st.link_button("Instagram", "https://www.instagram.com/luthuliscents?igsh=NzJvNDNxbDJsY3Jv")
st.link_button("WhatsApp", "https://wa.me/27692380796")
st.link_button("X / Twitter", "https://x.com/L68220Luthuli")
st.link_button("Email Us", "mailto:sthandiweluthuli322@gmail.com")
st.link_button("Facebook", "https://www.facebook.com/profile.php?id=61583709642144")
