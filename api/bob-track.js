/* LuthuliScents — Vercel serverless function.
   GET /api/bob-track?ref=<tracking_reference>   (also accepts ?tracking_reference=)
     Proxies BobGo v2 tracking so customers can check their parcel on the
     static site without exposing BOBGO_API_KEY. Returns a normalized:
       {
         ok, reference, status, status_friendly,
         courier, service_level, order_number, type,
         events: [{ date, status, location, message }]
       }
     BobGo keys live in Vercel env vars — never in client-side code.

   Env:
     BOBGO_API_KEY   required — bearer token (e.g. sandbox key from the BobGo
                     app → Settings → API).
     BOBGO_BASE_URL  optional — default sandbox. Use
                     https://api.sandbox.bobgo.co.za/v2 while testing and
                     https://api.bobgo.co.za/v2 for production. */

var DEFAULT_BASE_URL = 'https://api.sandbox.bobgo.co.za/v2';

function pickField(ev, keys) {
  for (var i = 0; i < keys.length; i++) {
    var v = ev[keys[i]];
    if (v != null && String(v).trim() !== '') return v;
  }
  return '';
}

function normalizeEvents(events) {
  if (!Array.isArray(events) || events.length === 0) return [];
  return events.map(function (ev) {
    return {
      // BobGo v2 live: { time, status, status_friendly, location, message }
      // Postman sample: { date, status, location, message, parcel_id }
      date: pickField(ev, ['time', 'date', 'event_date', 'created_at']),
      status: pickField(ev, ['status_friendly', 'status', 'event_type']),
      location: pickField(ev, ['location', 'address', 'city']),
      message: pickField(ev, ['message', 'description', 'text'])
    };
  }).filter(function (ev) { return ev.date || ev.status || ev.message; });
}

function pickStatus(payload) {
  var status = payload.status_friendly || payload.status;
  if (status) return status;
  var events = payload.checkpoints || payload.tracking_events;
  if (Array.isArray(events) && events.length) {
    var last = events[events.length - 1];
    return last.status_friendly || last.status || 'unknown';
  }
  return 'unknown';
}

function pickEventList(payload) {
  if (Array.isArray(payload.checkpoints)) return payload.checkpoints;
  if (Array.isArray(payload.tracking_events)) return payload.tracking_events;
  var grouped = payload.grouped_checkpoints;
  if (Array.isArray(grouped) && grouped.length && Array.isArray(grouped[0].checkpoints)) {
    return grouped.reduce(function (acc, g) { return acc.concat(g.checkpoints); }, []);
  }
  return [];
}

module.exports = async function handler(req, res) {
  var origin = req.headers.origin || '*';
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  if (req.method !== 'GET') {
    res.status(404).json({ error: 'Not found' });
    return;
  }

  var trackRef = (req.query.ref || req.query.tracking_reference || '').trim();
  if (!trackRef) {
    res.status(400).json({ error: 'Missing tracking reference (?ref=...).' });
    return;
  }

  var key = process.env.BOBGO_API_KEY || '';
  if (!key) {
    res.status(500).json({ error: 'BOBGO_API_KEY is not configured on Vercel. Add it in Project → Settings → Environment Variables.' });
    return;
  }

  var base = String(process.env.BOBGO_BASE_URL || DEFAULT_BASE_URL).replace(/\/+$/, '');
  var url = base + '/tracking?tracking_reference=' + encodeURIComponent(trackRef);

  try {
    var upstream = await fetch(url, {
      method: 'GET',
      headers: { 'Authorization': 'Bearer ' + key, 'Accept': 'application/json' }
    });
    var text = await upstream.text();
    var data = {};
    if (text) {
      try { data = JSON.parse(text); } catch (e) { /* non-JSON, surfaced via error */ }
    }

    if (!upstream.ok) {
      var errMsg = data.error || data.message || data.description || 'BobGo tracking failed';
      if (typeof errMsg === 'string') {
        var cleaned = errMsg.replace(/\}\}?\.?$/, '}}').trim();
        var inner = null;
        try { inner = JSON.parse(cleaned); } catch (e) {
          var m = /"message"\s*:\s*"([^"]+)"/.exec(errMsg);
          if (m) errMsg = m[1];
        }
        if (inner) {
          errMsg = (inner.data && inner.data.message) || inner.message || errMsg;
        }
      }
      res.status(upstream.status).json({ error: errMsg, detail: data });
      return;
    }

    // Real v2 tracking returns an array wrapping the payload; also tolerate a
    // bare object or a { data } envelope.
    var payload = Array.isArray(data) ? (data[0] || {})
      : (data.data && !data.data.status && (data.data.checkpoints || !data.status)) ? data.data
      : data;
    var events = pickEventList(payload);

    res.json({
      ok: true,
      reference: payload.shipment_tracking_reference || payload.tracking_reference || payload.id || trackRef,
      status: payload.status || '',
      status_friendly: payload.status_friendly || pickStatus(payload),
      courier: payload.courier_name || payload.provider_name || '',
      service: payload.service_level || payload.service_level_name || '',
      order_number: payload.order_number || payload.channel_order_number || payload.custom_order_number || '',
      type: payload.type || 'shipment',
      events: normalizeEvents(events),
      raw: data
    });
  } catch (err) {
    res.status(502).json({ error: 'Could not reach BobGo: ' + err.message });
  }
};