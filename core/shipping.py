"""Shipping rates client for the BobGo courier API (sandbox)."""

import re

import requests

API_URL = "https://api.sandbox.bobgo.co.za/rates"
API_KEY = "4b63fa75f2214611a0d97c2e3da57aff"

FREE_SHIPPING_THRESHOLD = 500.0


def _headers() -> dict:
    return {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}


def parse_price(option: str) -> float:
    """Extract the Rand amount from a shipping option label like 'The Courier Guy - R95'."""
    match = re.search(r"R([0-9]+\.?[0-9]*)", option)
    return float(match.group(1)) if match else 0.0


def apply_free_shipping(shipping_cost: float, subtotal: float) -> float:
    return 0.0 if subtotal > FREE_SHIPPING_THRESHOLD else shipping_cost


def get_rates(
    *,
    postal_code: str,
    parcel_weight_kg: float,
    address_line: str,
    suburb: str,
    city: str,
) -> dict:
    """Fetch courier options. Returns a dict with either ``options`` or an error."""
    payload = {
        "collection_address": {
            "address_line_1": "123 Main Street",
            "suburb": "Sandton",
            "city": "Johannesburg",
            "postal_code": "2001",
            "country_code": "ZA",
        },
        "delivery_address": {
            "address_line_1": address_line or "456 Delivery Road",
            "suburb": suburb or "Rosebank",
            "city": city,
            "postal_code": postal_code,
            "country_code": "ZA",
        },
        "parcels": [{"weight": parcel_weight_kg, "length": 10, "width": 8, "height": 8}],
    }

    try:
        response = requests.post(API_URL, json=payload, headers=_headers(), timeout=15)
    except Exception as exc:  # network / timeout
        return {"ok": False, "error": str(exc)}

    if response.status_code != 200:
        return {"ok": False, "status": response.status_code, "text": response.text[:500]}

    data = response.json()
    options = []
    for rate in data.get("rates", []):
        options.append(f"{rate['courier_name']} ({rate['service_level']}) - R{rate['price']}")

    for provider in data.get("provider_rate_requests", []):
        provider_name = provider.get("provider_name", "")
        for resp in provider.get("responses", []):
            if resp.get("status") != "success":
                continue
            service = resp.get("service_level", {}).get("name") or resp.get("service_level_code", "Service")
            amount = resp.get("rate_amount") or resp.get("rate_amount_excl_vat")
            if amount is None:
                continue
            label = f"{service} - R{amount}"
            if provider_name:
                label = f"{provider_name}: {label}"
            options.append(label)

    pending = any(
        provider.get("status") == "pending" or not provider.get("responses")
        for provider in data.get("provider_rate_requests", [])
    )

    return {"ok": True, "options": options, "pending": pending, "data": data}
