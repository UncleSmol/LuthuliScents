"""LuthuliScents — Vercel Python serverless function.

POST /api/create-checkout
  body: {
    total: 54000,             // amount in CENTS (R540.00)
    items: [{ name, quantity }],
    email: 'buyer@example.com' (optional),
    successUrl: 'https://<site>/success.html',
    cancelUrl:  'https://<site>/cart.html'
  }
  response: { redirectUrl, checkoutId }

Creates a Yoco hosted checkout from the customer's cart and returns the
redirectUrl for the browser. YOCO_SECRET_KEY must be set as a Vercel
environment variable — never in client-side code.

Vercel Python entrypoint: every api/*.py file that defines a `handler` class
inheriting from http.server.BaseHTTPRequestHandler becomes a Vercel Function
routed to /api/<filename>. See https://vercel.com/docs/functions/runtimes/python
"""

import json
import math
import os
import time
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler

YOCO_API = "https://payments.yoco.com/api/checkouts"


def _abs_url(value):
    if isinstance(value, str) and (value.startswith("http://") or value.startswith("https://")):
        return value
    return "https://example.com/cart.html"


class handler(BaseHTTPRequestHandler):
    def _cors(self):
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _json(self, code, payload):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self._cors()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        if self.command != "OPTIONS":
            self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors()
        self.end_headers()

    def do_POST(self):
        key = os.environ.get("YOCO_SECRET_KEY", "").strip()
        if not key:
            self._json(
                500,
                {"error": "YOCO_SECRET_KEY is not configured on Vercel. Add it in Project -> Settings -> Environment Variables."},
            )
            return

        try:
            length = int(self.headers.get("Content-Length", 0) or 0)
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except (ValueError, json.JSONDecodeError):
            self._json(400, {"error": "Invalid JSON body."})
            return

        try:
            total = int(round(float(body.get("total", 0))))
        except (TypeError, ValueError):
            total = 0
        if not math.isfinite(total) or total < 200:
            self._json(400, {"error": "Amount must be at least R2.00 (200 cents)."})
            return

        items = body.get("items") if isinstance(body.get("items"), list) else []
        item_summary = ", ".join(
            "{0} x{1}".format(item.get("name"), item.get("quantity") or 1)
            for item in items
            if isinstance(item, dict) and item.get("name")
        ) or "n/a"

        order_id = "LS-{0}".format(int(time.time() * 1000))

        checkout_request = {
            "amount": total,
            "currency": "ZAR",
            "successUrl": _abs_url(body.get("successUrl")),
            "cancelUrl": _abs_url(body.get("cancelUrl")),
            "metadata": {
                "source": "luthuliscents-static",
                "items": item_summary,
                "email": body.get("email") or "",
                "orderId": order_id,
            },
            "externalId": order_id,
        }

        req = urllib.request.Request(
            YOCO_API,
            data=json.dumps(checkout_request).encode("utf-8"),
            method="POST",
            headers={
                "Content-Type": "application/json",
                "Authorization": "Bearer " + key,
                "Idempotency-Key": str(uuid.uuid4()),
                "User-Agent": "LuthuliScents/2.0 (+https://luthuli-scents.vercel.app)",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                status = res.status
                data = json.loads(res.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            status = err.code
            raw = err.read().decode("utf-8", "replace")
            try:
                data = json.loads(raw)
            except (ValueError, json.JSONDecodeError):
                data = {"raw": raw}
        except Exception as exc:
            self._json(502, {"error": "Could not reach Yoco: {0}".format(exc)})
            return

        if not 200 <= status < 300:
            description = (
                data.get("description")
                or data.get("errorType")
                or data.get("errorCode")
                or (data.get("raw") if data.get("raw") else "Yoco checkout failed")
            )
            self._json(status, {"error": description, "detail": data})
            return

        if not data.get("redirectUrl"):
            self._json(502, {"error": "Yoco returned no redirectUrl"})
            return

        self._json(200, {"redirectUrl": data["redirectUrl"], "checkoutId": data.get("id")})