import os
import streamlit as st
import requests
import re

cart_count = len(st.session_state.get("cart", []))
nav_html = f'''
<div style="display:flex; justify-content:center; gap:10px; margin:12px 0;">
    <a href="/" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Home</a>
    <a href="/?script=/pages/02_About.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">About</a>
    <a href="/?script=/pages/03_Products.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.7);">Products</a>
    <a href="/?script=/pages/04_Contact.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(20,12,7,0.3);">Contact</a>
    <a href="/?script=/pages/05_Cart.py" style="color:#f8ead2; text-decoration:none; padding:8px 12px; border-radius:999px; background:rgba(212,175,55,0.12);">Cart ({cart_count})</a>
</div>
'''
st.markdown(nav_html, unsafe_allow_html=True)

st.title("Our Products")
st.info("ℹ️ Winter Sale: Get free shipping on all orders over R500!", icon="ℹ️")

if "cart" not in st.session_state:
    st.session_state.cart = []

def add_to_cart(product_code: str, product_name: str, product_price: float) -> None:
    for item in st.session_state.cart:
        if item["code"] == product_code:
            item["quantity"] += 1
            return
    st.session_state.cart.append({"code": product_code, "name": product_name, "price": product_price, "quantity": 1})

def remove_from_cart(index: int) -> None:
    st.session_state.cart.pop(index)

products = {
    "rosie": {"name": "Rosie", "price": 180.0, "image": "../WhatsApp Image 2026-05-27 at 09.07.42.jpeg", "description": "Longlasting feminine fragrance"},
    "sweetapple": {"name": "Sweetapple", "price": 180.0, "image": "../WhatsApp Image 2026-05-27 at 09.05.30.jpeg", "description": "Long lasting unisex fragrance"},
}

col1, col2 = st.columns(2, gap="large")
for column, product_code in zip((col1, col2), products.keys()):
    product = products[product_code]
    with column:
        st.image(product["image"], width=220)
        st.subheader(product["name"])
        st.write(product["description"])
        st.write(f"**R{product['price']:.2f} - 50ml**")
        if st.button(f"Add {product['name']} to cart", key=f"add_{product_code}"):
            add_to_cart(product_code, product["name"], product["price"])

st.write("---")
st.subheader("🛒 Your cart")
cart = st.session_state.cart
if not cart:
    st.info("Your cart is empty. Add a perfume to begin your order.")
else:
    total_price = 0.0
    for index, item in enumerate(cart):
        item_total = item["price"] * item["quantity"]
        total_price += item_total
        col_a, col_b, col_c = st.columns([3, 1.2, 1])
        with col_a:
            st.write(f"{item['name']} x{item['quantity']}")
        with col_b:
            st.write(f"R{item_total:.2f}")
        with col_c:
            if st.button("Remove", key=f"remove_{index}"):
                remove_from_cart(index)
    st.write(f"**Cart total:** R{total_price:.2f}")

st.write("---")
st.subheader("🚚 Calculate shipping rates")

if not cart:
    st.caption("Add at least one perfume to the cart before checking shipping.")
else:
    with st.form("shipping_form"):
        st.markdown("#### Customer details")
        cust_col1, cust_col2 = st.columns(2)
        with cust_col1:
            customer_name = st.text_input("Full name", "")
            customer_email = st.text_input("Email address", "")
        with cust_col2:
            customer_phone = st.text_input("Phone number", "")

        st.markdown("#### Delivery address")
        del_col1, del_col2 = st.columns(2)
        with del_col1:
            delivery_address_line = st.text_input("Delivery address line", "456 Delivery Road")
            delivery_suburb = st.text_input("Delivery suburb", "Rosebank")
        with del_col2:
            delivery_city = st.text_input("Delivery city", "Johannesburg")
            delivery_postal_code = st.text_input("Delivery postal code", "2001")

        submit_button = st.form_submit_button("Find shipping & checkout")

    API_KEY = None
    try:
        API_KEY = st.secrets.get("BOBGO_API_KEY")
    except Exception:
        API_KEY = None

    if not API_KEY:
        API_KEY = os.environ.get("BOBGO_API_KEY")

    if not API_KEY:
        st.error("Shipping API key is missing. Set BOBGO_API_KEY in Streamlit secrets or environment variables.")
    else:
        HEADERS = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }

        if submit_button:
            if not delivery_postal_code.strip():
                st.warning("Please enter a delivery postal code before checking shipping rates.")
            else:
                product_price = sum(item["price"] * item["quantity"] for item in cart)
                URL = "https://api.sandbox.bobgo.co.za/rates"
                payload = {
                    "collection_address": {
                        "address_line_1": "123 Main Street",
                        "suburb": "Sandton",
                        "city": "Johannesburg",
                        "postal_code": "2001",
                        "country_code": "ZA",
                    },
                    "delivery_address": {
                        "address_line_1": delivery_address_line,
                        "suburb": delivery_suburb,
                        "city": delivery_city,
                        "postal_code": delivery_postal_code.strip(),
                        "country_code": "ZA",
                    },
                    "parcels": [
                        {
                            "weight": 0.5,
                            "length": 10,
                            "width": 8,
                            "height": 8,
                        }
                    ],
                }
                try:
                    response = requests.post(URL, json=payload, headers=HEADERS, timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        options = []

                        rates = data.get("rates", [])
                        if rates:
                            options = [f"{r['courier_name']} ({r['service_level']}) - R{r['price']}" for r in rates]
                        else:
                            for provider in data.get("provider_rate_requests", []):
                                provider_name = provider.get("provider_name", "")
                                for resp in provider.get("responses", []):
                                    if resp.get("status") != "success":
                                        continue
                                    service_name = resp.get("service_level", {}).get("name") or resp.get("service_level_code", "Service")
                                    amount = resp.get("rate_amount") or resp.get("rate_amount_excl_vat")
                                    if amount is None:
                                        continue
                                    label = f"{service_name} - R{amount}"
                                    if provider_name:
                                        label = f"{provider_name}: {label}"
                                    options.append(label)

                        if options:
                            selected_shipping = st.selectbox("Select your delivery option:", options, key="shipping_option")
                            st.success(f"Selected shipping: {selected_shipping}")
                            shipping_cost_match = re.search(r"R([0-9]+\.?[0-9]*)", selected_shipping)
                            shipping_cost = float(shipping_cost_match.group(1)) if shipping_cost_match else 0.0
                            total_amount = product_price + shipping_cost

                            st.markdown("#### Order summary")
                            st.write(f"**Customer:** {customer_name}")
                            st.write(f"**Email:** {customer_email}")
                            st.write(f"**Phone:** {customer_phone}")
                            st.write(f"**Delivery address:** {delivery_address_line}, {delivery_suburb}, {delivery_city}, {delivery_postal_code.strip()}")
                            cart_items_text = ", ".join(f"{item['name']} x{item['quantity']}" for item in cart)
                            st.write(f"**Items in cart:** {cart_items_text}")
                            st.write(f"**Product price:** R{product_price:.2f}")
                            st.write(f"**Shipping fee:** R{shipping_cost:.2f}")
                            st.write(f"**Total to pay:** R{total_amount:.2f}")

                            description = "LuthuliScents+Cart"
                            checkout_url = f"https://pay.yoco.com/r/7KEK5q?amount={int(round(total_amount * 100))}&description={description}"
                            st.markdown("#### Complete your payment")
                            st.markdown(f"[👉 Pay R{total_amount:.2f} through Yoco Checkout]({checkout_url})")
                            st.info("After payment, the order will be processed for shipping.")
                        else:
                            pending = any(
                                provider.get("status") == "pending" or not provider.get("responses")
                                for provider in data.get("provider_rate_requests", [])
                            )
                            if pending:
                                st.warning("Rate requests are pending from the sandbox providers. Try again in a moment.")
                            else:
                                st.warning("No shipping options available for this postal code in sandbox mode.")
                except Exception as e:
                    st.error(f"Connection Failed: {str(e)}")
