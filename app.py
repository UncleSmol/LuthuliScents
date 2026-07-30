import streamlit as st
import requests
import re
#1.
st.markdown("""
<div style="text-align:center; padding:28px 24px 20px; margin:0 auto 18px; max-width:980px; border:1px solid rgba(212, 175, 55, 0.3); border-radius:24px; background:linear-gradient(135deg, rgba(255,255,255,0.08), rgba(212,175,55,0.12)); box-shadow:0 12px 30px rgba(0,0,0,0.24);">
    <div style="display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(212,175,55,0.16); color:#f2d27b; font-size:0.8rem; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:10px;">Luxury fragrance house</div>
    <h1 style="margin:0 0 8px; color:#f4d98d; font-size:2.3rem; font-weight:700;">✨ GOLDEN LUXURY PERFUMES</h1>
    <p style="margin:0; color:#f6e8c9; font-size:1.05rem; line-height:1.6;">Experience our hand-crafted, artisan scents designed to feel timeless, bold, and unforgettable.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(212, 175, 55, 0.16), transparent 24%),
            radial-gradient(circle at bottom right, rgba(139, 69, 19, 0.2), transparent 30%),
            linear-gradient(135deg, #140c07 0%, #23150c 45%, #4a2b16 100%);
        color: #f7e7c6;
    }

    .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
        color: #f2d27b;
    }

    .stApp p, .stApp div, .stApp label, .stApp .stTextInput > label, .stApp .stSelectbox > label {
        color: #f8ead2;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(212, 175, 55, 0.18);
        border-radius: 24px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.28);
    }

    .stTextInput > div > div, .stSelectbox > div > div, .stButton > button {
        background: linear-gradient(135deg, #3a2a1d 0%, #5a3a21 100%);
        color: #f8ead2;
        border: 1px solid #c9a24b;
        border-radius: 10px;
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.16);
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #c9a24b 0%, #f2d27b 100%);
        color: #1a140f;
        border: 1px solid #f2d27b;
        transform: translateY(-1px);
    }

    .stAlert, .stSuccess, .stWarning, .stInfo, .stError {
        border-radius: 12px;
        border: 1px solid rgba(212, 175, 55, 0.25);
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.16);
    }

    div[data-testid="stExpander"] {
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        background: rgba(255, 255, 255, 0.04);
    }

    img {
        border-radius: 16px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.24);
    }
</style>
""", unsafe_allow_html=True)
st.set_page_config(
    page_title="LuthuliScents",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)
# subheader
st.title("✨LUTHULISCENTS")
st.subheader(" Discover your signature scent")
st.image("logo.jpeg", width=220)
with st.expander("about us"):
    st.subheader("welcome to LUTHULISCENTS  `🧴` ")
st.markdown("""
- We make our perfumes from scratch.
- These scents are inspired by various scents.
- The scents accommodate all genders as long as you love perfumes.
- We have male scents, female scents and unisex.
- You can wear these scents on various occasions depending on the scents.
""")
#---- load assets ----
with st.expander("contact us"):
    st.write("We make long lasting scents, smell expensive without spending much.")
    st.write("follow us:")
    st.link_button("Tiktok", "https://www.tiktok.com/@sthandiwe386?is_from_webapp=1&sender_device=pc")
    st.link_button(" instagram","https://www.instagram.com/luthuliscents?igsh=NzJvNDNxbDJsY3Jv")
    st.link_button(" WhatsApp", "https://wa.me/27692380796")
    st.link_button(" X/ Twitter", "https://x.com/L68220Luthuli")
    st.link_button(" Email Us" ,"mailto:sthandiweluthuli322@gmail.com")
    st.link_button(" Facebook","https://www.facebook.com/profile.php?id=61583709642144")

#ADD YOUR PICTURE
col1, col2= st.columns(2, gap="large")
with col1:
    st.image("WhatsApp Image 2026-05-27 at 09.07.42.jpeg", width=220)
    st.subheader("our signature scents.female")
    st.write("Rosie. longlasting")
    st.markdown("[order now](https://pay.yoco.com/r/7KEK5q)")
    st.write("**R180-50ml**")

with col2:
    st.image("WhatsApp Image 2026-05-27 at 09.05.30.jpeg",width=220)
    st.subheader("our signature scents")
    st.write("Sweetapple. long lasting.unisex")
    st.markdown("[order now](https://pay.yoco.com/r/mEbKMD)")
    st.write("**R180-50ml**")
    st.info("ℹ️ Winter Sale: Get free shipping on all orders over R500!", icon="ℹ️")

    st.write("---")
    st.subheader("🚚 calculate shipping rates")

    with st.form("shipping_form"):
        st.markdown("#### Customer details")
        cust_col1, cust_col2 = st.columns(2)
        with cust_col1:
            customer_name = st.text_input("Full name", "")
            customer_email = st.text_input("Email address", "")
        with cust_col2:
            customer_phone = st.text_input("Phone number", "")

        st.markdown("#### Product selection")
        product_options = {
            "Rosie (female) - R180": 180.00,
            "Sweetapple (unisex) - R180": 180.00
        }
        selected_product = st.selectbox("Choose your perfume", list(product_options.keys()))
        product_price = product_options[selected_product]

        st.markdown("#### Delivery address")
        del_col1, del_col2 = st.columns(2)
        with del_col1:
            delivery_address_line = st.text_input("Delivery address line", "456 Delivery Road")
            delivery_suburb = st.text_input("Delivery suburb", "Rosebank")
        with del_col2:
            delivery_city = st.text_input("Delivery city", "Johannesburg")
            delivery_postal_code = st.text_input("Delivery postal code", "2001")

        submit_button = st.form_submit_button("Find shipping & checkout")

    API_KEY = "4b63fa75f2214611a0d97c2e3da57aff"
    HEADERS = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    if submit_button:
        if not delivery_postal_code.strip():
            st.warning("Please enter a delivery postal code before checking shipping rates.")
        else:
            URL = "https://api.sandbox.bobgo.co.za/rates"
            payload = {
                "collection_address": {
                    "address_line_1": "123 Main Street",
                    "suburb": "Sandton",
                    "city": "Johannesburg",
                    "postal_code": "2001",
                    "country_code": "ZA"
                },
                "delivery_address": {
                    "address_line_1": delivery_address_line,
                    "suburb": delivery_suburb,
                    "city": delivery_city,
                    "postal_code": delivery_postal_code.strip(),
                    "country_code": "ZA"
                },
                "parcels": [
                    {
                        "weight": 0.5,
                        "length": 10,
                        "width": 8,
                        "height": 8
                    }
                ]
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
                        st.write(f"**Product:** {selected_product}")
                        st.write(f"**Shipping option:** {selected_shipping}")
                        st.write(f"**Product price:** R{product_price:.2f}")
                        st.write(f"**Shipping fee:** R{shipping_cost:.2f}")
                        st.write(f"**Total to pay:** R{total_amount:.2f}")

                        description = selected_product.replace(" ", "+")
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

                elif response.status_code == 403:
                    st.error("Shipping service rejected the request: the sandbox endpoint does not support POST on /rates. Check the API URL or provider docs.")
                    st.write(response.text)
                else:
                    st.error(f"Server Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {str(e)}")
 
