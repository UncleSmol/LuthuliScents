# LuthuliScents — Yoco checkout function (Vercel serverless)

One serverless function that turns the customer's **actual cart** into a Yoco
hosted payment link. It is the only place your Yoco secret key lives — it must
never go in the static site's HTML/JS.

## Flow

1. The static site on GitHub Pages posts `{ total, items, email, successUrl,
   cancelUrl }` to this function via `js/checkout.js`.
2. This function calls Yoco's Checkout API
   (`POST payments.yoco.com/api/checkouts`) with
   `Authorization: Bearer <YOCO_SECRET_KEY>` and an amount in **cents**.
3. Yoco returns a `redirectUrl`; this function responds with it; the browser
   redirects the customer to pay on Yoco's hosted page.

## Deploy

Create the project in the Vercel dashboard (import your GitHub repo, Framework
Preset = **Other**). This repo has no framework, so Vercel serves the static
files at root and treats `api/create-checkout.js` as a serverless function.

Set the environment variable (never commit it):
- Vercel dashboard → Project → Settings → Environment Variables
- Name `YOCO_SECRET_KEY`, value `sk_live_...` (live) or `sk_test_...` (test).
- Check the deployment scope you use (Production / Preview / Development).

Deploy via `vercel --prod` or push to your `main` branch if you enabled
Git integration.

## Point the static site at your function

After deploying you get a URL like `https://<project>.vercel.app`. The
checkout endpoint is `https://<project>.vercel.app/api/create-checkout`.

Edit the constant in `build.py`:
```python
YOCO_CHECKOUT_API = "https://<project>.vercel.app/api/create-checkout"
```
then regenerate the site data:
```bash
python build.py products
```

## Yoco live keys / domain verification

Yoco requires you to verify the domain that redirects back after payment
(`success.html`/`cart.html`, i.e. your GitHub Pages hostname) before live keys
activate. In the Yoco app: **Sales → Payment Gateway → Verified domains**.
Use `sk_test_...` while building, `sk_live_...` for production.

## Local testing

```bash
# run the function locally with a key present
set YOCO_SECRET_KEY=sk_test_your_key_here   # PowerShell
vercel dev
curl -X POST http://localhost:3000/api/create-checkout \
  -H "Content-Type: application/json" \
  -d '{"total":54000,"items":[{"name":"Rosie","quantity":2}],"successUrl":"https://example.com/success.html","cancelUrl":"https://example.com/cart.html"}'
```

## Security notes

- `YOCO_SECRET_KEY` is a secret — set it as a Vercel env var, never commit it.
- Amounts are validated server-side (min R2.00). Confirm actual receipt via
  Yoco's `payment.succeeded` webhook in production, not the `successUrl`.