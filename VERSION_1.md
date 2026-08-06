# LuthuliScents — Version 1 (Streamlit)

> Documentation of the website **as currently shipped** (Version 1).
> See `VERSION_2.md` for the planned HTML/CSS + Flask redesign.

## 1. Overview

LuthuliScents is a single-brand perfume e-commerce website. It is built as a
**Streamlit** app that runs one Python script (`app.py`) and renders every page
server-side on rerun. Customers can browse two fragrances, add them to a
session-based cart, request a BobGo shipping quote, and pay through a Yoco
checkout link.

The app is deployed to **Railway** using a `Procfile` and a GitHub Actions
workflow.

## 2. Tech Stack

| Layer        | Technology                                                       |
| ------------ | ---------------------------------------------------------------- |
| Framework    | Streamlit (`>=1.26.0`)                                            |
| HTTP client  | `requests` (BobGo rates API)                                      |
| Config       | `python-dotenv` + Streamlit `secrets`                              |
| Deployment   | Railway (Procfile), GitHub Actions                                 |
| Persistence  | None (cart held in `st.session_state` only)                       |
| Styling      | Injected CSS (`unsafe_allow_html=True`)                           |

Dependencies (`requirements.txt`):

```
python-dotenv>=1.0.0
streamlit>=1.26.0
requests>=2.31.0
```

## 3. Architecture & File Index

```
website/
├── app.py                              # Main entry point + all 4 pages
├── pages/
│   ├── 01_Home.py                      # Home page (HTML nav bar)
│   ├── 02_About.py                     # About page
│   ├── 03_Products.py                  # Products + cart + shipping form
│   ├── 04_Contact.py                   # Contact / social links
│   └── 05_Cart.py                      # Cart summary + quick checkout
├── requirements.txt                    # Python dependencies
├── Procfile                            # Railway start command
├── .github/workflows/deploy-to-railway.yml  # CI/CD
├── RAILWAY_DEPLOY_README.md            # Deployment notes (outdated vs workflow)
├── logo.jpeg                           # Brand logo (used)
├── WhatsApp Image 2026-05-27 at 09.07.42.jpeg   # Rosie product image (used)
├── WhatsApp Image 2026-05-27 at 09.05.30.jpeg   # Sweetapple product image (used)
├── apple blaze.jpeg                    # Unused image
├── sweetapple.jpeg                     # Unused image
├── woody2.png                          # Unused image
└── IMG-20260429-WA0066.jpg             # Unused image
```

## 4. Features

### Navigation
- **Custom button nav** (`app.py:93-105`): four buttons (Home, About, Products,
  Contact) set `st.session_state.page`, and a dispatcher at `app.py:347-354`
  renders the matching page.
- **HTML nav bars** in `pages/*`: each page renders `<a>` links using
  `/?script=/pages/02_About.py`-style URLs.
- **Conflict:** when deployed, Streamlit auto-adds `pages/` to the native
  sidebar, so two navigation systems render at once.

### Pages
| Page    | Location                         | Content                                         |
| ------- | -------------------------------- | ----------------------------------------------- |
| Home    | `app.py` `render_home_page` / `pages/01_Home.py` | Hero banner, brand title, logo              |
| About   | `app.py` `render_about_page` / `pages/02_About.py` | Brand story, bullet list                   |
| Products| `app.py` `render_products_page` / `pages/03_Products.py` | Catalog, cart, shipping form             |
| Contact | `app.py` `render_contact_page` / `pages/04_Contact.py` | Social links (TikTok, IG, WhatsApp, X, email, FB) |
| Cart    | `pages/05_Cart.py`                | Line items, total, quick Yoco checkout          |

### Product catalog
Hardcoded dict (`app.py:159-162`):

| Code        | Name       | Price  | Size | Image                                   | Description                 |
| ----------- | ---------- | ------ | ---- | --------------------------------------- | --------------------------- |
| `rosie`     | Rosie      | R180   | 50ml | `WhatsApp Image 2026-05-27 at 09.07.42.jpeg` | Longlasting feminine fragrance |
| `sweetapple`| Sweetapple | R180   | 50ml | `WhatsApp Image 2026-05-27 at 09.05.30.jpeg` | Long lasting unisex fragrance |

### Cart
- Stored as a list in `st.session_state["cart"]`.
- Item shape: `{"code": str, "name": str, "price": float, "quantity": int}`.
- Adding the same code again increments quantity (`add_to_cart`,
  `app.py:149-154`).
- Items can be removed; cart total is summed and displayed.
- **Session-only:** cart is lost when the browser session ends.

### Shipping & checkout
1. Customer fills a shipping form (name, email, phone, delivery address).
2. `POST https://api.sandbox.bobgo.co.za/rates` returns courier options.
3. A shipping option is selected; order summary is displayed.
4. A Yoco checkout link is generated and displayed for payment.

## 5. Data Model

No database. The only runtime state is:

```python
st.session_state["page"]        # str: "home" | "about" | "products" | "contact"
st.session_state["cart"]        # list[dict] of cart items (see shape above)
st.session_state["shipping_option"]  # selected courier label
```

## 6. External Integrations

### BobGo Shipping Rates (sandbox)
- **Endpoint:** `https://api.sandbox.bobgo.co.za/rates`
- **Auth:** `Authorization: Bearer <BOBGO_API_KEY>`
- **Key source:** `st.secrets.get("BOBGO_API_KEY")` then fallback to
  environment variable `BOBGO_API_KEY` (`app.py:221-232`).
- **Payload:** fixed collection address (123 Main Street, Sandton,
  Johannesburg 2001, ZA), customer delivery address, and a single 0.5kg
  parcel (10 × 8 × 8 cm).
- **Response parsing:** two shapes handled — a flat `rates[]` array, or
  `provider_rate_requests[].responses[]` with per-provider success/pending
  status (`app.py:275-291`).
- **Error handling:** 200 (parse rates), 403 (sandbox POST restriction),
  other codes, and network exceptions (`app.py:269-332`).

### Yoco Checkout (payment)
- Hardcoded payment link:
  `https://pay.yoco.com/r/7KEK5q?amount={total_cents}&description=LuthuliScents+Cart`
- Amount is `round(total_amount * 100)` (ZAR → cents).
- No order is recorded server-side after payment.

## 7. Theming

Dark luxury palette injected as CSS in `app.py:28-91`:

- Background: radial gold/brown gradients over `#140c07 → #4a2b16`.
- Text: warm cream `#f8ead2` / `#f7e7c6`.
- Headings: gold `#f2d27b`.
- Buttons/inputs: brown gradient with gold border; hover inverts to gold.
- Rounded cards, blur backdrop, soft shadows.

## 8. Deployment

> **Status:** this version is being retired from Railway and replaced by a
> static site on GitHub Pages (see `VERSION_2.md`). The notes below describe
> how V1 currently runs.

- **Platform:** Railway.
- **Procfile:** `web: streamlit run app.py --server.port $PORT --server.headless true`
- **CI/CD:** `.github/workflows/deploy-to-railway.yml` — installs Node 20 and
  the Railway CLI, then runs `railway up --detach` on push to `main`
  (also manually dispatchable). **To be removed/replaced with the GitHub Pages
  workflow.**
- **Secrets:** `BOBGO_API_KEY` must be set as a Railway env var (or Streamlit
  secret). Note: `RAILWAY_DEPLOY_README.md` describes an older workflow that
  references `RAILWAY_API_KEY`/`RAILWAY_PROJECT_ID` and is now stale.

## 9. Known Issues & Limitations

| # | Issue | Location |
| - | ----- | -------- |
| 1 | Two conflicting navigation systems (button nav + `pages/` multipage nav) render together | `app.py:93-105`, `pages/*` |
| 2 | ~200 lines duplicated between `app.py` products page and `pages/03_Products.py` | `app.py:142-332`, `pages/03_Products.py` |
| 3 | Cart is session-only — no persistence across reloads, no order records | `app.py:146`, `pages/05_Cart.py` |
| 4 | `st.experimental_rerun()` is deprecated | `pages/05_Cart.py:34` |
| 5 | Four product images shipped but unused | root images |
| 6 | Hardcoded values: Yoco link, collection address, parcel dimensions | `app.py:244-312` |
| 7 | `RAILWAY_DEPLOY_README.md` is stale vs the actual workflow | root |
| 8 | `__pycache__` committed to git | `__pycache__/` |

---

*Next: see `VERSION_2.md` for the redesign — a static HTML/CSS site hosted on
GitHub Pages (with Python used as local tooling).*
