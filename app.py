import os
try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args, **kwargs):
        return False
import streamlit as st
import requests
import re

load_dotenv()

st.set_page_config(
    page_title="LuthuliScents",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed",
)

if "page" not in st.session_state:
    st.session_state.page = "home"


def set_page(page_name: str) -> None:
    st.session_state.page = page_name


st.markdown(
    """
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
    """,
    unsafe_allow_html=True,
)

nav_cols = st.columns(4, gap="small")
with nav_cols[0]:
    if st.button("🏠 Home", key="nav_home", use_container_width=True, type="primary" if st.session_state.page == "home" else "secondary"):
        set_page("home")
with nav_cols[1]:
    if st.button("ℹ️ About", key="nav_about", use_container_width=True, type="primary" if st.session_state.page == "about" else "secondary"):
        set_page("about")
with nav_cols[2]:
    if st.button("🧴 Products", key="nav_products", use_container_width=True, type="primary" if st.session_state.page == "products" else "secondary"):
        set_page("products")
with nav_cols[3]:
    if st.button("📞 Contact", key="nav_contact", use_container_width=True, type="primary" if st.session_state.page == "contact" else "secondary"):
        set_page("contact")

st.markdown("<br>", unsafe_allow_html=True)


def render_home_page() -> None:
    st.markdown(
        """
        <div style="text-align:center; padding:28px 24px 20px; margin:0 auto 18px; max-width:980px; border:1px solid rgba(212, 175, 55, 0.3); border-radius:24px; background:linear-gradient(135deg, rgba(255,255,255,0.08), rgba(212,175,55,0.12)); box-shadow:0 12px 30px rgba(0,0,0,0.24);">
            <div style="display:inline-block; padding:6px 12px; border-radius:999px; background:rgba(212,175,55,0.16); color:#f2d27b; font-size:0.8rem; letter-spacing:0.2em; text-transform:uppercase; margin-bottom:10px;">Luxury fragrance house</div>
            <h1 style="margin:0 0 8px; color:#f4d98d; font-size:2.3rem; font-weight:700;">✨ GOLDEN LUXURY PERFUMES</h1>
            <p style="margin:0; color:#f6e8c9; font-size:1.05rem; line-height:1.6;">Experience our hand-crafted, artisan scents designed to feel timeless, bold, and unforgettable.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.title("✨ LUTHULISCENTS")
    st.subheader("Discover your signature scent")
    st.image("logo.jpeg", width=220)
    st.write("Browse our collection, learn more about our story, and place your order in a few simple steps.")


def render_about_page() -> None:
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


def render_products_page() -> None:
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
        "rosie": {"name": "Rosie", "price": 180.0, "image": "WhatsApp Image 2026-05-27 at 09.07.42.jpeg", "description": "Longlasting feminine fragrance"},
        "sweetapple": {"name": "Sweetapple", "price": 180.0, "image": "WhatsApp Image 2026-05-27 at 09.05.30.jpeg", "description": "Long lasting unisex fragrance"},
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
            return

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

                    elif response.status_code == 403:
                        st.error("Shipping service rejected the request: the sandbox endpoint does not support POST on /rates. Check the API URL or provider docs.")
                        st.write(response.text)
                    else:
                        st.error(f"Server Error ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {str(e)}")


def render_contact_page() -> None:
    st.title("Contact Us")
    st.write("We make long-lasting scents that feel luxurious without being overly expensive.")
    st.write("Follow us:")
    st.link_button("TikTok", "https://www.tiktok.com/@sthandiwe386?is_from_webapp=1&sender_device=pc")
    st.link_button("Instagram", "https://www.instagram.com/luthuliscents?igsh=NzJvNDNxbDJsY3Jv")
    st.link_button("WhatsApp", "https://wa.me/27692380796")
    st.link_button("X / Twitter", "https://x.com/L68220Luthuli")
    st.link_button("Email Us", "mailto:sthandiweluthuli322@gmail.com")
    st.link_button("Facebook", "https://www.facebook.com/profile.php?id=61583709642144")


if st.session_state.page == "home":
    render_home_page()
elif st.session_state.page == "about":
    render_about_page()
elif st.session_state.page == "products":
    render_products_page()
else:
    render_contact_page()
