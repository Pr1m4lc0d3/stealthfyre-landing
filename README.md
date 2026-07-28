# StealthFyre — landing page

A single static page for **stealthfyre.com**. No build step, no dependencies.
Open `index.html` in a browser and what you see is what ships.

```
index.html      the page (markup + inline JS at the bottom)
style.css       all styling; brand tokens are at the top in :root
img/            images, already resized and compressed
CNAME           tells GitHub Pages the custom domain
DNS-SETUP.txt   exact registrar records — follow this to go live
```

---

## Two placeholders must be replaced before launch

Both are clearly marked in the source. The page works without them; it just
can't capture anything yet.

### 1. Kit (ConvertKit) form ID

In `index.html`, near the bottom:

```js
var KIT_FORM_ID = 'REPLACE_ME';
```

In your Kit account:

1. Create a form for StealthFyre — keep it separate from the Madame Whisper
   form so the lists stay clean.
2. Add a **custom field** named exactly `kit_interest`.
3. Copy the form's numeric ID out of its URL and paste it above.

Until this is set, submitting shows *"The list isn't open just yet"* rather
than failing silently.

### 2. GA4 measurement ID

In `index.html`, in `<head>`, replace **both** occurrences of `G-XXXXXXXXXX`
with the real ID from your new StealthFyre GA4 property.

Until it's set, the tracking code is inert and sends nothing.

---

## Events sent to GA4

| Event | When | Parameter |
|---|---|---|
| `cta_click` | any call-to-action is clicked | `cta` — which one |
| `waitlist_submit` | a signup succeeds | `kit` — the kit chosen |
| `scroll_depth` | 25 / 50 / 75 / 100% reached | `percent` |

`page_view` comes free with the GA4 config call.

---

## Going live

Follow `DNS-SETUP.txt`. Short version: push to GitHub, turn on Pages, swap the
A records at Squarespace Domains away from the dead host `50.6.226.52`, then
enforce HTTPS.

## Updating

Edit the files and push. GitHub Pages redeploys on push — there is nothing to
rebuild.

---

## When you're ready to sell

Product is already on hand, so the only missing piece is a checkout. Each kit
card in `index.html` has a marked **CTA SLOT**:

```html
<!-- CTA SLOT: swap this anchor for a Stripe Payment Link when selling opens -->
<a class="kit__cta" href="#waitlist" ...>Notify me ›</a>
```

Create one Stripe Payment Link per kit and change the `href`. Stripe handles
checkout, shipping address and receipts with no backend, which is what makes
this work on a static host. Put prices back on the cards at the same time.

The waitlist is worth keeping for whatever you're out of stock on.

---

## Where the images came from

Pulled from the 2024 cPanel backup (`stealthfyre.tar.gz`), specifically
`wp-content/uploads/2020/04/`, then resized and recompressed. **Only image
files were taken out of that archive** — no database, no credentials, no
customer data. Originals are in `F:\StealthFyre\_source-assets\`, which is a
local working folder and is not part of this site.

The stock photography from the old theme (`hero-min.jpg`, `our-stoves1-min.jpg`,
`meet-steath-min.jpg`, the `AdobeStock_*` files) is deliberately unused. Every
photograph on the page is a real StealthFyre kit.
