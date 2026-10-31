# Shree Dogada Farm — Flask Shop

A Flask website for the farm, with product listings, cart, checkout, customer inquiries, owner order management, and livestock/vaccination records.

## Run locally (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
python run.py
```

Open `http://127.0.0.1:5000`.

## Before public deployment

Set these environment variables in the hosting provider:

- `SECRET_KEY`: a long random secret (generate one with `python -c "import secrets; print(secrets.token_hex(32))"`).
- `INITIAL_OWNER_PASSWORD`: a strong password of at least 10 characters if the database does not already contain the owner account. This is only used to create the first owner.
- `DATABASE_URL`: recommended PostgreSQL connection URL for persistent production data. Without it, the app uses SQLite at `instance/farm.db`; that may be lost on hosts with ephemeral filesystems.
- `SITE_URL`: the final public website origin, e.g. `https://your-site.example`.
- `SESSION_COOKIE_SECURE=true` when served over HTTPS.

The owner username is `owner`. Existing owner accounts retain their existing password. To reset an existing owner password, set `RESET_OWNER_PASSWORD` to a strong password for one deployment/start, then remove that variable after confirming the reset. Do not leave reset variables configured permanently.

## Hosting notes

This is a server-rendered Flask application, not a static-only site. Netlify Drop, GitHub Pages, and Cloudflare Pages cannot run this conventional Flask server directly. Use a Python-capable host (the included `Procfile` starts it with Gunicorn). A separate static frontend on Netlify would require a larger frontend/backend split.

Free hosting plans, databases, and file storage have limits and may sleep or delete temporary files. Back up your database and use persistent PostgreSQL plus durable object storage before relying on this for real customer orders.

## Security and payment notes

- POST forms use CSRF tokens.
- Owner login has a basic per-process failed-login throttle. For multi-worker or high-risk production use, configure a shared rate limiter.
- Security response headers and safer session-cookie defaults are enabled.
- eSewa and Khalti are hidden from checkout until a verified integration is added. Bank QR transfers are manual and are not automatically verified; the farm must confirm receipt.
- Never commit `.env`, database files, uploaded customer data, or credentials to a public repository.
- The free public OSRM routing endpoint is not guaranteed for production traffic.

## Test

```powershell
python -m compileall app config.py run.py index.py
```

Please test a sample checkout, owner login, product update, and livestock upload before using the site for real orders.


## Cart and privacy/legal updates (29 October 2026)

- Cart totals now reflect only items actually saved by pressing **Add to cart**; quantity selection is a draft and no longer changes the subtotal prematurely. Cart rendering uses DOM text nodes for product labels.
- Added draft Privacy Policy, Terms of Service, Subprocessor List, Business DPA template and order-data export/deletion form. These are implementation drafts, not legal advice or a guarantee of legal compliance; have a Nepal-qualified lawyer review them.
- Checkout requires an explicit Terms/Privacy acceptance checkbox, checked server-side.
- Added Accept and Reject optional choices. The current application has no analytics/advertising trackers; cart storage is essential browser storage. Checkout still contacts OpenStreetMap and a public OSRM routing service, which are disclosed on checkout and in the privacy notice.
- Removed remote Google Fonts loading. System-font fallbacks are used.
- Added focus-visible styling and reduced-motion support, but a complete WCAG audit with keyboard, screen-reader, contrast and automated testing is still required.
- `ASSET_LICENSE_AUDIT.md` records unresolved image provenance and dependency-license caveats. Confirm image/logo permissions and audit the full resolved dependency tree before public deployment.
- The application has no subscriptions/recurring billing, no configured AI-training feature and no marketing email sender in the reviewed source. If these are added later, re-review terms, consent, unsubscribe and data-use controls.

## Data rights endpoint

Customers can open `/data-rights`, then enter an order code and phone number to download that order's data as JSON or erase direct identifiers from the active order record. This is not a full account-level data management system; the site currently has no customer accounts. Verify requests carefully and follow applicable retention obligations.
