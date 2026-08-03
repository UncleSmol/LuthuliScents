"""Cart & checkout page: line items, shipping rates and Yoco payment link."""

import urllib.parse

import streamlit as st

from core.session import clear, decrement, increment, items, subtotal
from core.shipping import apply_free_shipping, get_rates, parse_price
from core.ui import render_footer, section_heading


def _render_line_item(p: dict, qty: int) -> None:
    row_l, row_m, row_r = st.columns([1.4, 1, 1])
    with row_l:
        st.markdown(f"**{p['name']}**  \n{p['family']} · {p['size']}")
    with row_m:
        mc1, mc2, mc3, mc4 = st.columns([1, 1, 1, 1])
        with mc1:
            st.button("−", key=f"dec_{p['key']}", on_click=decrement, args=(p["key"],))
        with mc3:
            st.write(f"**×{qty}**")
        with mc4:
            st.button("+", key=f"inc_{p['key']}", on_click=increment, args=(p["key"],))
    with row_r:
        st.write(f"**R{p['price'] * qty:.2f}**")
    st.markdown("<hr>", unsafe_allow_html=True)


def render() -> None:
    st.title("Your Cart")

    if not st.session_state.cart:
        st.write("Your cart is empty. Visit the Shop page to add your signature scent.")
        st.stop()

    cart_items = items()
    total_product = subtotal(cart_items)

    for p, qty in cart_items:
        _render_line_item(p, qty)

    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        st.metric("Subtotal", f"R{total_product:.2f}")
    with col3:
        if st.button("Clear cart"):
            clear()

    st.markdown("<hr>", unsafe_allow_html=True)
    section_heading("Delivery", "Checkout")
    st.caption("Enter your details to calculate shipping to your door.")

    with st.form("checkout_form"):
        c1, c2 = st.columns(2)
        with c1:
            customer_name = st.text_input("Full name")
            customer_email = st.text_input("Email address")
        with c2:
            customer_phone = st.text_input("Phone number")
            selected_city = st.text_input("City", value="Johannesburg")

        d1, d2 = st.columns(2)
        with d1:
            delivery_address_line = st.text_input("Street address")
            delivery_suburb = st.text_input("Suburb")
        with d2:
            delivery_postal_code = st.text_input("Postal code")
            delivery_city = st.text_input("Delivery city", value="Johannesburg")

        submit_checkout = st.form_submit_button("Calculate shipping", type="primary")

    if submit_checkout:
        _handle_checkout(
            postal_code=delivery_postal_code,
            cart_items=cart_items,
            total_product=total_product,
            customer_name=customer_name,
            customer_email=customer_email,
            customer_phone=customer_phone,
            delivery_address_line=delivery_address_line,
            delivery_suburb=delivery_suburb,
            delivery_city=delivery_city,
            selected_city=selected_city,
        )

    render_footer()


def _handle_checkout(**kwargs) -> None:
    postal_code = (kwargs["postal_code"] or "").strip()
    if not postal_code:
        st.warning("Please enter a postal code to calculate shipping.")
        return

    cart_items = kwargs["cart_items"]
    total_product = kwargs["total_product"]
    parcel_weight = 0.5 * len(cart_items) if cart_items else 0.5

    with st.spinner("Fetching the best delivery rates..."):
        result = get_rates(
            postal_code=postal_code,
            parcel_weight_kg=parcel_weight,
            address_line=kwargs["delivery_address_line"],
            suburb=kwargs["delivery_suburb"],
            city=kwargs["delivery_city"] or kwargs["selected_city"],
        )

    if not result["ok"]:
        st.error(f"Could not reach the shipping service: {result.get('error') or f'{result.get('status')} — {result.get('text')}'}")
        return

    options = result["options"]
    if options:
        selected_shipping = st.selectbox("Select delivery option:", options, key="shipping_option")
        shipping_cost = parse_price(selected_shipping)
        shipping_cost = apply_free_shipping(shipping_cost, total_product)
        total_amount = total_product + shipping_cost

        st.success(f"Selected shipping: {selected_shipping}")

        st.markdown("#### Order summary")
        for p, qty in cart_items:
            st.write(f"- {p['name']} × {qty} — R{p['price'] * qty:.2f}")
        st.write(f"**Subtotal:** R{total_product:.2f}")
        free_note = " *(free — over R500)*" if total_product > 500 else ""
        st.write(f"**Shipping:** R{shipping_cost:.2f}{free_note}")
        st.write(f"**Total to pay:** R{total_amount:.2f}")

        description = "+".join(p["name"] for p, _ in cart_items) or "Perfume"
        checkout_url = (
            f"{cart_items[0][0]['pay_link']}"
            f"?amount={int(round(total_amount * 100))}"
            f"&description={urllib.parse.quote(description)}"
        )
        st.markdown("#### Complete payment")
        st.markdown(f"[Pay R{total_amount:.2f} securely via Yoco]({checkout_url})")
        st.info("After payment, your order will be prepared and shipped within 2 business days.")
    elif result.get("pending"):
        st.warning("Rate requests are still pending from providers — try again in a moment.")
    else:
        st.warning("No shipping options available for this postal code in sandbox mode.")
