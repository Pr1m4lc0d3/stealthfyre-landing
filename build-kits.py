#!/usr/bin/env python3
"""
Generates the five kit pages in kits/ from the KITS table below.

Why this exists: prices are provisional until the cutting quote lands, and every
kit page repeats the same shell. Editing five near-identical files by hand is how
they drift apart. Change a number here, run `python build-kits.py`, commit the
regenerated HTML. The site stays static — this is a authoring tool, not a runtime
dependency.

To switch a kit from waitlist to live checkout, put its Stripe Payment Link in
`buy` and re-run.
"""

import html
from pathlib import Path

OUT = Path(__file__).parent / "kits"
GA_ID = "G-MMNR8VCMZ4"

# Specs are HARD — lifted from each kit's PARTS LIST.TXT in the production package.
# Assembly counts are FLOORS: the site says "at least", never "up to".
KITS = [
    dict(
        num="01", slug="bush-runner", name="Bush Runner", sku="",
        img="kit-bush-runner.jpg",
        alt="A StealthFyre Bush Runner assembled into an open stove on a forest floor, "
            "brand stamped on the stainless panel",
        tag="The smallest way in.",
        list_price=175, launch_price=131,
        assembles="5", assembles_note="",
        panels="11", panels_note=True,
        deployed="17¾ × 9 × 4⅝ in", packed="9¼ × 5 × ½ in", weight="2 lb 15.25 oz",
        buy="",
        blurb=[
            "The Bush Runner is the entry point to the panel system and the lightest "
            "thing in the range. It packs down to roughly the footprint of a paperback "
            "and disappears into a daypack.",
            "It is a complete stove in its own right, not a sample. And because every "
            "kit in the range is cut from the same panel family, anything you buy later "
            "combines with it rather than replacing it.",
        ],
        accessory="Grill and damper kit available.",
    ),
    dict(
        num="02", slug="deuce", name="Deuce", sku="GTO-SF-02DE",
        img="kit-deuce.jpg",
        alt="A StealthFyre Deuce assembled as a tall tower stove beside a waterfall",
        tag="Two Bush Runners, one kit.",
        list_price=329, launch_price=247,
        assembles="9", assembles_note="",
        panels="22", panels_note=True,
        deployed="17¾ × 17¾ × 4⅝ in", packed="9½ × 5¼ × 1 in", weight="6 lb 2 oz",
        buy="",
        blurb=[
            "The Deuce is exactly twice the Bush Runner — the same panels, doubled. That "
            "extra material is what buys height: this is the smallest kit in the range "
            "that builds a proper tower.",
            "It still packs to under an inch thick. Two people cooking, or one person "
            "who wants a real chimney draw, start here.",
        ],
        accessory="Grill and damper kit available.",
    ),
    dict(
        num="03", slug="origin", name="Origin", sku="",
        img="kit-origin.jpg",
        alt="A StealthFyre Origin assembled as a tunnel stove with a pot heating on top",
        tag="Where the tunnel faces arrive.",
        list_price=279, launch_price=209,
        assembles="9", assembles_note=" plus windbreaks of varying sizes",
        panels="20", panels_note=False,
        deployed="26½ × 9 × 9 in", packed="9½ × 5¼ × 1 in", weight="5 lb 1.95 oz",
        buy="",
        blurb=[
            "The Origin introduces the left and right tunnel faces, and with them a "
            "different class of stove. Tunnel configurations run longer and hotter than "
            "anything the tower-only kits reach, and the leftover panels become "
            "windbreaks at whatever size the weather demands.",
            "This is the kit most people should start with if they intend to keep going.",
        ],
        accessory="Grill and damper kit, potbelly stove and full chimney system available.",
    ),
    dict(
        num="04", slug="origin-deluxe", name="Origin Deluxe", sku="",
        img="kit-origin-deluxe.jpg",
        alt="A StealthFyre Origin Deluxe assembled into a multi-unit cooking layout beside a creek",
        tag="The range opens up.",
        list_price=319, launch_price=239,
        assembles="20", assembles_note=" plus windbreaks of varying sizes",
        panels="24", panels_note=False,
        deployed="26½ × 9 × 9 in", packed="9½ × 5¼ × 1 in", weight="5 lb 6.05 oz",
        buy="",
        blurb=[
            "The Origin Deluxe is the Origin plus four more panels — two tower walls and "
            "two mini tunnel faces. Four panels does not sound like much. It more than "
            "doubles what the kit can build.",
            "That is the nature of a combinatorial system: the configurations do not grow "
            "in a line, they grow by multiplication. This is the best value in the range "
            "by a wide margin.",
        ],
        accessory="Grill and damper kit, potbelly stove and full chimney system available.",
    ),
    dict(
        num="05", slug="guerrilla-master", name="Guerrilla Master", sku="",
        img="kit-guerrilla-master.jpg",
        alt="A large StealthFyre Guerrilla Master build with a potbelly body and chimney, "
            "assembled in a wooded gully",
        tag="Everything the system can do.",
        list_price=589, launch_price=441,
        assembles="three dozen", assembles_note=" plus windbreaks of varying sizes",
        panels="44", panels_note=True,
        deployed="26½ × 26½ × 9 in", packed="10 × 5¾ × 2 in", weight="10 lb 11.6 oz",
        buy="",
        flagship=True,
        blurb=[
            "The Guerrilla Master is two Origin Deluxe kits in one box, and it reaches "
            "well over three dozen distinct configurations before you start counting "
            "windbreaks. With the potbelly accessory it becomes an enclosed stove with a "
            "chimney — a different object entirely from where the range starts.",
            "It still packs into a box ten inches long. That is the whole argument for "
            "the panel system, in one kit.",
        ],
        accessory="Grill and damper kit, potbelly stove door and full chimney system available.",
    ),
]

PAGE = """<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{name} — StealthFyre {tagline_t}</title>
<meta name="description" content="{meta_desc}">
<link rel="icon" href="/img/favicon.png">
<link rel="canonical" href="https://stealthfyre.com/kits/{slug}.html">

<meta property="og:type" content="product">
<meta property="og:site_name" content="StealthFyre">
<meta property="og:title" content="{name} — StealthFyre">
<meta property="og:description" content="{meta_desc}">
<meta property="og:image" content="https://stealthfyre.com/img/{img}">
<meta property="og:url" content="https://stealthfyre.com/kits/{slug}.html">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{name} — StealthFyre">
<meta name="twitter:description" content="{meta_desc}">
<meta name="twitter:image" content="https://stealthfyre.com/img/{img}">

<link rel="stylesheet" href="/style.css">
<script async src="https://www.googletagmanager.com/gtag/js?id={ga}"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('js', new Date());
  gtag('config', '{ga}');
</script>

<a class="skip" href="#main">Skip to content</a>

<header class="nav is-stuck" id="nav">
  <div class="wrap nav__inner">
    <a class="nav__logo" href="/" aria-label="StealthFyre home">
      <img src="/img/logo-nav.png" alt="StealthFyre" width="250" height="44">
    </a>
    <a class="btn btn--ghost nav__cta" href="/#kits">All kits</a>
  </div>
</header>

<main id="main">

<section class="product">
  <div class="wrap">
    <p class="crumb"><a href="/#kits">Kits</a> <span>/</span> {name}</p>

    <div class="product__grid">

      <div class="product__media">
        <img src="/img/{img}" alt="{alt}" width="452" height="450">
      </div>

      <div class="product__body">
        <p class="eyebrow">Kit {num}{sku_t}</p>
        <h1 class="h2">{name}</h1>
        <p class="product__tag">{tag}</p>

        <p class="product__cap">Assembles <strong>at least {assembles}</strong> different stoves{assembles_note}.</p>

        <div class="price">
          <span class="price__now">${launch}</span>
          <span class="price__was">${list}</span>
          <span class="price__tag">Launch price</span>
        </div>
        <p class="price__note">
          Launch pricing while current panel stock lasts. Shipping calculated at checkout.
        </p>

        {cta}

        <p class="leadtime">
          <strong>Made to order.</strong> Built by hand, one at a time, after you order —
          expect <strong>about two weeks</strong> from order to mailbox. If anything is
          going to take longer than that, you will be told and offered a refund.
        </p>

        <table class="spec">
          <caption class="visually-hidden">{name} specifications</caption>
          <tbody>
            <tr><th scope="row">Panels</th><td>{panels}{panels_note}</td></tr>
            <tr><th scope="row">Deployed</th><td>{deployed}</td></tr>
            <tr><th scope="row">Packed</th><td>{packed}</td></tr>
            <tr><th scope="row">Weight</th><td>{weight}</td></tr>
            <tr><th scope="row">Material</th><td>24-gauge stainless steel</td></tr>
            <tr><th scope="row">Made</th><td>By hand, in the USA</td></tr>
          </tbody>
        </table>
      </div>

    </div>
  </div>
</section>

<section class="section section--alt">
  <div class="wrap narrow">
    <h2 class="h2">About this kit</h2>
    {blurb}
    <p class="accessory"><strong>Accessories.</strong> {accessory}</p>
    <p><a class="btn btn--ghost" href="/#kits">Compare all five kits</a></p>
  </div>
</section>

<section class="section">
  <div class="wrap narrow">
    <h2 class="h2">Made to order, by hand.</h2>
    <p>
      StealthFyre is not mass produced. Every kit is built one at a time, by one
      person, after you order it. Each panel has its protective backing stripped, its
      edges deburred by hand until they are clean to the touch, and every fold bent
      individually on a purpose-built tool. The finished kit is wrapped, boxed and
      addressed by the same pair of hands.
    </p>
    <p>
      Panel stock is limited and the kits share the same panels between them — so when
      a run is spoken for, it is genuinely gone until the next one.
    </p>
  </div>
</section>

</main>

<footer class="footer">
  <div class="wrap footer__inner">
    <img class="footer__logo" src="/img/logo-footer-light.png" alt="StealthFyre — Modular, Tactical, Compact" width="480" height="236" loading="lazy">
    <p class="footer__line">Modular &middot; Tactical &middot; Compact</p>
    <p class="footer__meta">&copy; <span id="year">2026</span> StealthFyre. All rights reserved.</p>
    <p class="footer__privacy">This site uses Google Analytics to count visits. No advertising trackers.</p>
  </div>
</footer>

<script>
  document.getElementById('year').textContent = new Date().getFullYear();
</script>
"""

CTA_LIVE = """<a class="btn btn--primary btn--lg btn--block" href="{buy}"
           data-track="buy_{slug}">Order the {name} &mdash; ${launch}</a>"""

# No Payment Link yet: send them to the list rather than to a dead button.
CTA_WAIT = """<a class="btn btn--primary btn--lg btn--block" href="/#waitlist"
           data-track="notify_{slug}">Tell me when ordering opens &rsaquo;</a>
        <p class="cta__note">Checkout opens shortly. The list is told first.</p>"""


def build(k):
    meta = (f"{k['name']} — a flat-pack 24-gauge stainless panel kit that assembles into "
            f"at least {k['assembles']} different stoves. Made to order by hand in the USA.")
    cta = (CTA_LIVE if k["buy"] else CTA_WAIT).format(
        buy=k["buy"], slug=k["slug"], name=k["name"], launch=k["launch_price"])

    return PAGE.format(
        name=html.escape(k["name"]),
        tagline_t="kit",
        meta_desc=html.escape(meta),
        slug=k["slug"], img=k["img"], alt=html.escape(k["alt"]),
        ga=GA_ID, num=k["num"],
        sku_t=f" &middot; {k['sku']}" if k["sku"] else "",
        tag=html.escape(k["tag"]),
        assembles=k["assembles"], assembles_note=k["assembles_note"],
        launch=k["launch_price"], list=k["list_price"],
        cta=cta,
        panels=k["panels"],
        panels_note=" <span class=\"spec__q\">(being re-verified)</span>" if k["panels_note"] else "",
        deployed=k["deployed"], packed=k["packed"], weight=k["weight"],
        blurb="\n    ".join(f"<p>{html.escape(p)}</p>" for p in k["blurb"]),
        accessory=html.escape(k["accessory"]),
    )


def main():
    OUT.mkdir(exist_ok=True)
    for k in KITS:
        p = OUT / f"{k['slug']}.html"
        p.write_text(build(k), encoding="utf-8")
        state = "LIVE checkout" if k["buy"] else "waitlist CTA"
        print(f"  {p.relative_to(OUT.parent)}  ({state})")
    print(f"\n{len(KITS)} kit pages written.")


if __name__ == "__main__":
    main()
