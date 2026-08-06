import streamlit as st

if "cart" not in st.session_state:
    st.session_state.cart = []

cart = st.session_state.cart

cart_count = len(cart)
nav_html = f'''
<div style="display:flex; justify-content:center; gap:10px; margin:12px 0;">
  <a href="/" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Home</a>
  <a href="/?script=/pages/02_About.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">About</a>
  <a href="/?script=/pages/03_Products.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Products</a>
  <a href="/?script=/pages/04_Contact.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Contact</a>
  <a href="/?script=/pages/05_Cart.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(212,175,55,0.12);">Cart ({cart_count})</a>
</div>
'''
st.markdown(nav_html, unsafe_allow_html=True)

st.title("Your Cart")
if not cart:
    st.info("Your cart is empty. Add products on the Products page.")
else:
    total = 0.0
    for idx, item in enumerate(cart):
        cols = st.columns([3,1,1])
        with cols[0]:
            st.write(f"{item['name']} x{item['quantity']}")
        with cols[1]:
            st.write(f"R{item['price']*item['quantity']:.2f}")
        with cols[2]:
            if st.button("Remove", key=f"cart_remove_{idx}"):
                cart.pop(idx)
                st.experimental_rerun()
        total += item['price'] * item['quantity']

    st.markdown(f"**Cart total:** R{total:.2f}")
    st.markdown("---")
    st.markdown("### Quick Checkout")
    checkout_url = f"https://pay.yoco.com/r/7KEK5q?amount={int(round(total*100))}&description=LuthuliScents+Cart"
    st.markdown(f"[👉 Pay R{total:.2f} through Yoco Checkout]({checkout_url})")
    st.info("For shipping calculation, go to the Products page and click 'Find shipping & checkout'.")
