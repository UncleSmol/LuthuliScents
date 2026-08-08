/* LuthuliScents — Vercel serverless function.
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
   environment variable — never in client-side code. */

var YOCO_API = 'https://payments.yoco.com/api/checkouts';

module.exports = async function handler(req, res) {
  var origin = req.headers.origin || '*';
  res.setHeader('Access-Control-Allow-Origin', origin);
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.status(204).end();
    return;
  }
  if (req.method !== 'POST') {
    res.status(404).json({ error: 'Not found' });
    return;
  }

  var key = process.env.YOCO_SECRET_KEY || '';
  if (!key) {
    res.status(500).json({ error: 'YOCO_SECRET_KEY is not configured on Vercel. Add it in Project → Settings → Environment Variables.' });
    return;
  }

  var body = req.body || {};
  var total = Math.round(Number(body.total));
  if (!isFinite(total) || total < 200) {
    res.status(400).json({ error: 'Amount must be at least R2.00 (200 cents).' });
    return;
  }

  var items = Array.isArray(body.items) ? body.items : [];
  var itemSummary = items
    .filter(function (it) { return it && it.name; })
    .map(function (it) { return it.name + ' x' + (it.quantity || 1); })
    .join(', ');

  var absUrl = function (u) { return /^https?:\/\//.test(u) ? u : 'https://example.com/cart.html'; };

  var checkoutRequest = {
    amount: total,
    currency: 'ZAR',
    successUrl: absUrl(body.successUrl),
    cancelUrl: absUrl(body.cancelUrl),
    metadata: {
      source: 'luthuliscents-static',
      items: itemSummary || 'n/a',
      email: body.email || '',
      orderId: 'LS-' + Date.now()
    },
    externalId: 'LS-' + Date.now()
  };

  try {
    var upstream = await fetch(YOCO_API, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + key,
        'Idempotency-Key': crypto.randomUUID()
      },
      body: JSON.stringify(checkoutRequest)
    });
    var data = await upstream.json();

    if (!upstream.ok) {
      res.status(upstream.status).json({ error: data.description || data.errorType || 'Yoco checkout failed', detail: data });
      return;
    }
    if (!data.redirectUrl) {
      res.status(502).json({ error: 'Yoco returned no redirectUrl' });
      return;
    }
    res.json({ redirectUrl: data.redirectUrl, checkoutId: data.id });
  } catch (err) {
    res.status(502).json({ error: 'Could not reach Yoco: ' + err.message });
  }
};