"""LuthuliScents — Vercel Python serverless function.

GET /api/bob-track?ref=<tracking_reference>   (also accepts ?tracking_reference=)

Proxies BobGo v2 tracking so customers can check their parcel on the static
site without exposing BOBGO_API_KEY. Returns a normalised:
  {
    ok, reference, status, status_friendly,
    courier, service_level, order_number, type,
    events: [{ date, status, location, message }]
  }

Env:
  BOBGO_API_KEY   required — bearer token (e.g. sandbox key from the BobGo
                  app -> Settings -> API).
  BOBGO_BASE_URL  optional — default sandbox. Use
                  https://api.sandbox.bobgo.co.za/v2 while testing and
                  https://api.bobgo.co.za/v2 for production.

Vercel Python entrypoint: the `handler` class below is routed to /api/bob-track.
"""

import json
import os
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler

DEFAULT_BASE_URL = "https://api.sandbox.bobgo.co.za/v2"


def _pick_field(event, keys):
    for key in keys:
        value = event.get(key)
        if value is not None and str(value).strip() != "":
            return value
    return ""


def _normalize_events(events):
    if not isinstance(events, list) or not events:
        return []
    normalised = []
    for event in events:
        if not isinstance(event, dict):
            continue
        item = {
            "date": _pick_field(event, ["time", "date", "event_date", "created_at"]),
            "status": _pick_field(event, ["status_friendly", "status", "event_type"]),
            "location": _pick_field(event, ["location", "address", "city"]),
            "message": _pick_field(event, ["message", "description", "text"]),
        }
        if item["date"] or item["status"] or item["message"]:
            normalised.append(item)
    return normalised


def _pick_status(payload):
    status = _pick_field(payload, ["status_friendly", "status"])
    if status:
        return status
    events = payload.get("checkpoints") or payload.get("tracking_events")
    if isinstance(events, list) and events:
        last = events[-1]
        if isinstance(last, dict):
            return _pick_field(last, ["status_friendly", "status"]) or "unknown"
    return "unknown"


def _pick_event_list(payload):
    checkpoints = payload.get("checkpoints")
    if isinstance(checkpoints, list):
        return checkpoints
    tracking_events = payload.get("tracking_events")
    if isinstance(tracking_events, list):
        return tracking_events
    grouped = payload.get("grouped_checkpoints")
    if (
        isinstance(grouped, list)
        and grouped
        and isinstance(grouped[0], dict)
        and isinstance(grouped[0].get("checkpoints"), list)
    ):
        events = []
        for group in grouped:
            events.extend(group.get("checkpoints") or [])
        return events
    return []


class handler(BaseHTTPRequestHandler):
    def _cors(self):
        origin = self.headers.get("Origin", "*")
        self.send_header("Access-Control-Allow-Origin", origin)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
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

    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlsplit(self.path).query)
        track_ref = (query.get("ref") or query.get("tracking_reference") or [""])[0].strip()
        if not track_ref:
            self._json(400, {"error": "Missing tracking reference (?ref=...)."})
            return

        key = os.environ.get("BOBGO_API_KEY", "")
        if not key:
            self._json(
                500,
                {"error": "BOBGO_API_KEY is not configured on Vercel. Add it in Project -> Settings -> Environment Variables."},
            )
            return

        base = (os.environ.get("BOBGO_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
        url = base + "/tracking?tracking_reference=" + urllib.parse.quote(track_ref)

        req = urllib.request.Request(
            url,
            headers={
                "Authorization": "Bearer " + key,
                "Accept": "application/json",
                "User-Agent": "LuthuliScents/2.0 (+https://luthuli-scents.vercel.app)",
            },
        )

        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                status = res.status
                text = res.read().decode("utf-8")
        except urllib.error.HTTPError as err:
            status = err.code
            text = err.read().decode("utf-8", "replace")
        except Exception as exc:
            self._json(502, {"error": "Could not reach BobGo: {0}".format(exc)})
            return

        data = {}
        if text:
            try:
                data = json.loads(text)
            except (ValueError, json.JSONDecodeError):
                data = {}

        if not 200 <= status < 300:
            err_msg = (
                data.get("error")
                or data.get("message")
                or data.get("description")
                or "BobGo tracking failed"
            )
            if isinstance(err_msg, str):
                cleaned = err_msg.rstrip("}")
                try:
                    inner = json.loads(cleaned)
                except (ValueError, json.JSONDecodeError):
                    inner = None
                if inner:
                    err_msg = (
                        (inner.get("data") or {}).get("message")
                        if isinstance(inner.get("data"), dict)
                        else None
                    ) or inner.get("message") or err_msg
            self._json(status, {"error": err_msg, "detail": data})
            return

        # Real v2 tracking returns an array wrapping the payload; also tolerate
        # a bare object or a { data } envelope.
        if isinstance(data, list):
            payload = data[0] if data else {}
        elif (
            isinstance(data.get("data"), dict)
            and not data.get("data").get("status")
            and (data.get("data").get("checkpoints") or not data.get("status"))
        ):
            payload = data["data"]
        else:
            payload = data

        events = _normalize_events(_pick_event_list(payload))

        self._json(
            200,
            {
                "ok": True,
                "reference": (
                    _pick_field(payload, ["shipment_tracking_reference", "tracking_reference", "id"])
                    or track_ref
                ),
                "status": payload.get("status") or "",
                "status_friendly": payload.get("status_friendly") or _pick_status(payload),
                "courier": _pick_field(payload, ["courier_name", "provider_name"]),
                "service": _pick_field(payload, ["service_level", "service_level_name"]),
                "order_number": _pick_field(
                    payload, ["order_number", "channel_order_number", "custom_order_number"]
                ),
                "type": payload.get("type") or "shipment",
                "events": events,
                "raw": data,
            },
        )