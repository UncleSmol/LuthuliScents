# LuthuliScents — Version 2 (Static HTML/CSS on GitHub Pages + Python Tooling)

> Blueprint for the redesign of LuthuliScents from the Streamlit app (V1) to a
> **static website hosted on GitHub Pages**.
> Hosting constraint: GitHub Pages only serves static HTML/CSS/JS — it cannot
> run Python. Python is therefore used for **local build, content generation,
> and order automation tooling** (see §4), not for serving the live site.
> See `VERSION_1.md` for the current implementation.

## 1. Goals

1. Host the website **free on GitHub Pages** (no Railway, no server).
2. Real, single navigation system (no duplicated navs as in V1).
3. Plain HTML5 + CSS3 pages styled with a shared theme — fast and static.
4. Client-side cart persisted in `localStorage` (survives page loads).
5. Keep Yoco checkout via a link; collect orders through a third-party form
   (e.g. Formspree/Google Form) or a mailto/WhatsApp handoff.
6. Use **Python as local tooling**: generate product data, build pages, and
   process exported orders.
7. Fix every known issue documented in `VERSION_1.md` where possible in a
   static context.

## 2. Tech Stack

| Layer          | Technology                                             |
| -------------- | ------------------------------------------------------ |
| Frontend       | Plain HTML5 + CSS3 + vanilla JS (no framework)          |
| Hosting        | GitHub Pages (free static hosting)                      |
| Cart           | Browser `localStorage` (client-side)                    |
| Payments       | Yoco checkout link (opened client-side)                 |
| Order intake   | Third-party form (Formspree / Google Form / WhatsApp)   |
| Python (local) | `python` + stdlib (`json`, `csv`) and `requests`        |
| Deployment     | GitHub Actions → GitHub Pages (`.github/workflows/pages.yml`) |

Local Python `requirements-dev.txt` (optional tooling):

```
requests>=2.31.0
python-dotenv>=1.0.0
```

## 3. Project Structure

```
luthuliscents-v2/
├── index.html               # Home page
├── about.html               # About page
├── products.html            # Product grid + cart summary
├── contact.html             # Contact / social links
├── cart.html                # Cart page + checkout
├── confirmation.html        # Order confirmation (after form submit)
├── css/
│   └── style.css            # Luxury gold/dark theme
├── js/
│   ├── products.js          # Product data + rendering
│   ├── cart.js              # localStorage cart logic
│   └── checkout.js          # Order form handling
├── img/                     # logo.jpeg + all product images
├── data/
│   └── products.json        # Generated catalog (single source of truth)
├── tools/                   # Local Python tooling (not hosted)
│   ├── build_products.py    # products.py → products.json
│   ├── render_pages.py      # (optional) generates HTML from templates
│   └── process_orders.py    # Downloads form exports → orders.csv
├── .gitignore               # excludes __pycache__/, .venv/
└── .github/workflows/
    └── pages.yml            # Deploys static site to GitHub Pages
```

## 4. Python "Backend Logic" (Local Tooling)

Because GitHub Pages cannot run Python, the V2 "backend logic" is implemented
as **local scripts** in `tools/`. They run on the developer's machine (or in
CI) and their outputs are committed to the repo.

### 4.1 Catalog generation (`tools/build_products.py`)

Single source of truth `products.py` → `data/products.json`, which the
browser loads.

```python
# tools/build_products.py
import json

PRODUCTS = {
    "rosie": {
        "name": "Rosie", "price": 180.0, "size_ml": 50,
        "image": "img/rosie.jpg",
        "description": "Longlasting feminine fragrance",
    },
    "sweetapple": {
        "name": "Sweetapple", "price": 180.0, "size_ml": 50,
        "image": "img/sweetapple.jpg",
        "description": "Long lasting unisex fragrance",
    },
    # new products are added here, never in two places
}

with open("data/products.json", "w", encoding="utf-8") as fh:
    json.dump(PRODUCTS, fh, indent=2, ensure_ascii=False)
```

### 4.2 Page generation (`tools/render_pages.py`, optional)

If hand-editing six HTML files is too repetitive, a small template renderer can
generate the nav/footer into every page so navigation stays DRY.

```python
# tools/render_pages.py — merges NAV/FOOTER snippets into each page
NAV = """<nav>...Home · About · Products · Contact · Cart (0)...</nav>"""
for page in ("index", "about", "products", "contact", "cart", "confirmation"):
    # replace a <!--NAV--> marker in each .html and write it back
```

> Recommended: keep the HTML hand-authored for the baseline. Add
> `render_pages.py` only if page count grows.

### 4.3 Order processing (`tools/process_orders.py`)

Orders are captured by a third-party form (Formspree email / Google Sheet /
WhatsApp). The script pulls that export and normalises it to `orders.csv` for
fulfilment.

```python
# tools/process_orders.py — example: convert exported rows to orders.csv
import csv, sys

def main(source_csv: str, out_csv: str = "orders.csv") -> None:
    with open(source_csv, newline="", encoding="utf-8") as fin, \
         open(out_csv, "w", newline="", encoding="utf-8") as fout:
        rows = csv.DictReader(fin)
        fieldnames = ["order_no", "customer", "email", "phone",
                      "address", "suburb", "city", "postal",
                      "items", "total", "date"]
        writer = csv.DictWriter(fout, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            # normalise + write fulfilment-ready row
            writer.writerow(row)

if __name__ == "__main__":
    main(sys.argv[1])
```

## 5. Frontend Design

### 5.1 Shared layout
- One header with a **single nav** (same markup on every page):
  Home · About · Products · Contact · Cart (n).
- Footer with contact info and social links.
- Cart count is updated from `localStorage` on every page.

### 5.2 Theme (`css/style.css`)
The V1 luxury palette is consolidated into CSS variables:

```css
:root {
  --bg: #140c07;
  --bg-alt: #23150c;
  --gold: #f2d27b;
  --gold-deep: #c9a24b;
  --text: #f8ead2;
  --text-dim: #f6e8c9;
  --brown: #4a2b16;
}
```

- Gradient background, cream text, gold headings, gold-bordered cards.
- Buttons: brown gradient → gold hover inversion (matches V1 hover state).
- Responsive product grid via CSS `grid` / `flexwrap`.

### 5.3 Pages
- **index.html** — hero banner + brand title + logo.
- **about.html** — brand story bullets.
- **products.html** — product cards rendered from `data/products.json` via
  `js/products.js`; each card has "Add to cart".
- **cart.html** — line items from `localStorage`, quantity, remove, total,
  order form, and pay link.
- **confirmation.html** — shown after the order form submits.
- **contact.html** — social link buttons.

### 5.4 Client-side cart (`js/cart.js`)

```js
// cart stored in localStorage so it survives page loads
let cart = JSON.parse(localStorage.getItem("cart") || "{}");

function addToCart(code) { cart[code] = (cart[code] || 0) + 1; save(); }
function setQty(code, qty) { cart[code] = Math.max(0, qty); save(); }
function save() {
  localStorage.setItem("cart", JSON.stringify(cart));
  updateBadge();
}
```

Prices always come from `data/products.json`, never from the cart, so a
tampered value cannot change the total.

### 5.5 Checkout (`js/checkout.js`)
1. Read cart + products, compute totals, show order summary.
2. Submit order details (name, email, phone, delivery address) to the
   third-party form (Formspree/Google Form) — this is what records the order.
3. Show the Yoco payment link:
   `https://pay.yoco.com/r/7KEK5q?amount={total_cents}&description=LuthuliScents+Cart`
4. Redirect to `confirmation.html` and clear the cart.

## 6. Feature Migration Map

| V1 Feature                        | V2 Equivalent                               | Notes / Improvements                     |
| --------------------------------- | ------------------------------------------- | ---------------------------------------- |
| Custom button nav (`set_page`)    | Single static nav on every page             | One nav, no `st.session_state`           |
| `pages/` multipage + HTML `?script=` links | Removed entirely                   | Eliminates duplicate-nav conflict        |
| `render_products_page` + `pages/03_Products.py` (duplicated) | One `products.html` + `js/products.js` | Code written once, DRY               |
| Hardcoded `products` dict         | `data/products.json` (generated by `tools/`) | Single source of truth                 |
| Cart in `st.session_state`        | Cart in browser `localStorage`              | Survives page reloads                    |
| BobGo shipping form in page       | Not feasible statically (CORS + secret key) | Use flat-rate / contact-for-quote; see §7 |
| Yoco redirect link                | Yoco link built client-side                 | Preserved as checkout                    |
| No order records                  | Third-party form + `tools/process_orders.py`→`orders.csv` | Orders captured off-site          |
| `st.experimental_rerun()`         | Vanilla JS `location`/state updates         | Deprecated API removed                   |
| Injected CSS in Python string     | Static `css/style.css` + CSS variables      | Maintainable, cacheable, reusable        |
| Unused product images             | All images wired into `data/products.json`  | All 6 images used in the catalog         |

## 7. Known V1 Issues → Fixes

| V1 Issue | V2 Resolution |
| -------- | ------------- |
| Dual/conflicting navigation | One static nav; no `pages/` directory |
| ~200 lines of duplication | One `products.html` + shared `js/` + generated catalog |
| Session-only cart, no persistence | Cart in `localStorage` |
| `st.experimental_rerun()` deprecated | Vanilla JS state updates |
| Unused product images | All images referenced in `data/products.json` |
| Hardcoded Yoco/address/parcel values | Yoco link constant in `js/checkout.js`; no server constants needed |
| Stale deploy docs | Docs kept in sync with the actual Pages workflow |
| `__pycache__` committed | `.gitignore` excludes `__pycache__/`, `.venv/`, `tools/output/` |

**Not supported on GitHub Pages (replacement chosen):**
- BobGo live rate lookup → flat shipping rates set in `js/checkout.js`, or a
  "request a quote" WhatsApp/email handoff.
- SQLite order storage → third-party form + exported `orders.csv` processed by
  `tools/process_orders.py`.
- Server-side secret handling → no secrets exist on the site; the BobGo API key
  would only ever be used from the developer's machine in `tools/`.

## 8. Deployment (GitHub Pages)

### 8.1 Enable GitHub Pages (one-time, in repo Settings)
1. `Settings → Pages → Build and deployment → Source: GitHub Actions`.

### 8.2 `.github/workflows/pages.yml`

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
      - name: Configure Pages
        uses: actions/configure-pages@v5
      - name: Upload site
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'          # static site lives at repo root
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### 8.3 How it works
- Push to `main` → Actions builds the static site → GitHub Pages serves it at
  `https://<user>.github.io/<repo>/`.
- No Procfile, no server, no secrets — the site is just committed files.

### 8.4 What is removed from V1
- `Procfile`, Railway CLI workflow, and Railway env vars (`BOBGO_API_KEY`).
- Streamlit-specific runtime (`streamlit run ...`, `st.secrets`).

## 9. Optional Next Steps (Out of Scope for V2 Baseline)

- **Custom domain** — point a domain at GitHub Pages and add a `CNAME`.
- **`render_pages.py`** — template-driven page generation once pages grow.
- **Form backend** — Formspree (free tier) or a Google Form for order capture.
- **WhatsApp order handoff** — a prefilled `wa.me` link with cart contents.
- **Static site generator** (e.g. plain Jinja2 build) if editing HTML by hand
  becomes tedious.
