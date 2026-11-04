import re, json, os, shutil, html, csv, sys, hashlib
from brands import BRANDS, CATS, TERR, PUMP_TYPES
from guides import GUIDES
from content2 import SERVICES, INDUSTRIES
from photos import PHOTO, photo_url
from tracking import ga_snippet
from search import build_index
from pumptypes import PUMP_PAGES

# Preview is the default: every page tells search engines and AI crawlers to stay out.
# Build with --live only when Southern Design has approved the site for launch.
LIVE = "--live" in sys.argv
ROBOTS_META = "" if LIVE else '\n<meta name="robots" content="noindex, nofollow">'

SITE = "https://www.southerndesign.com/"
OUT = "../site"
DATE = "2026-10-01"
PHONE, TEL = "877-917-8677", "+18779178677"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT + "/assets")

concept = open("home-template.html").read()
css = concept[concept.index("<style>") + 7:concept.index("</style>")]
css += open("extra.css").read()
# Speed: the stylesheet is inlined in every page and the font is served from this site, so nothing blocks the first paint.
css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
css = re.sub(r"\s+", " ", css)
css = re.sub(r" ?([{};,>]) ?", r"\1", css).replace(";}", "}").strip()
FONT_CSS = ('@font-face{font-family:"Open Sans";font-style:normal;font-weight:300 800;font-stretch:75% 100%;font-display:swap;src:url(ASSETSfonts/open-sans.woff2) format("woff2")}'
            '@font-face{font-family:"Open Sans";font-style:italic;font-weight:300 800;font-stretch:75% 100%;font-display:swap;src:url(ASSETSfonts/open-sans-italic.woff2) format("woff2")}')
def page_css(depth): return FONT_CSS.replace("ASSETS", pre(depth) + "assets/") + css.replace("ROOTimg/", pre(depth) + "img/")
# The largest thing painted first is the header photo, so it is requested straight from the HTML rather than waiting for the styles.
# On phones the home page photo comes through this site's own address (a pass-through rule in _redirects), which saves a second connection.
HERO = "photo-1509390288171-ce2088f7d08e"
HERO_DESKTOP = f"https://images.unsplash.com/{HERO}?auto=format&fit=crop&w=1800&q=60"
HERO_MOBILE_SRC = f"https://images.unsplash.com/{HERO}?fit=crop&w=600&q=40&fm=webp"
def preloads(path, depth):
    if path == "":
        return (f'\n<link rel="preload" as="image" href="img/hero-m.webp" media="(max-width: 720px)" fetchpriority="high">'
                f'\n<link rel="preload" as="image" href="{esc(HERO_DESKTOP)}" media="(min-width: 721px)" fetchpriority="high">')
    if path in PHOTO:
        return f'\n<link rel="preload" as="image" href="{esc(photo_url(PHOTO[path][0], 1800))}" media="(min-width: 721px)" fetchpriority="high">'
    return ""
def ver(name): return hashlib.md5(open(name, "rb").read()).hexdigest()[:8]
V_JS, V_LOGO = ver("site.js"), ver("logo.svg")
home_main = concept[concept.index('<main id="main">'):concept.index("</main>") + 7]
form_html = concept[concept.index('<form id="quote-form"'):concept.index("</form>") + 7]

B = {b[0]: dict(slug=b[0], name=b[1], cat=b[2], noun=b[3], line=b[4], items=b[5], terr=b[6], guides=b[7]) for b in BRANDS}
G = {g["slug"]: g for g in GUIDES}
S = {s["slug"]: s for s in SERVICES}
PAGES = []

def pre(depth): return "../" * depth
def href(depth, path): return pre(depth) + path + "index.html"
def links(text, depth):
    return re.sub(r"\[\[([^|\]]*)\|([^\]]+)\]\]", lambda m: f'<a href="{href(depth, m.group(1))}">{m.group(2)}</a>', text)
def strip_links(text): return re.sub(r"\[\[[^|\]]*\|([^\]]+)\]\]", r"\1", text)
def esc(t): return html.escape(t, quote=True)

def blocks(bl, depth):
    out = []
    for b in bl:
        if isinstance(b, str): out.append(f"<p>{links(b, depth)}</p>")
        elif isinstance(b, tuple): out.append("<ol>" + "".join(f"<li>{links(i, depth)}</li>" for i in b[1]) + "</ol>")
        else: out.append("<ul>" + "".join(f"<li>{links(i, depth)}</li>" for i in b) + "</ul>")
    return "\n".join(out)

def table(t, depth):
    cap, head, rows = t
    return (f'<h2>{cap}</h2>\n<div class="tbl-wrap" tabindex="0" role="region" aria-label="{esc(cap)}"><table class="tbl"><thead><tr>' + "".join(f'<th scope="col">{h}</th>' for h in head) + "</tr></thead><tbody>"
            + "".join("<tr>" + "".join(f"<td>{links(c, depth)}</td>" for c in r) + "</tr>" for r in rows) + "</tbody></table></div>")

def faq_html(faq, depth):
    return '<h2>Frequently asked questions</h2>\n' + "\n".join(f"<h3>{q}</h3>\n<p>{links(a, depth)}</p>" for q, a in faq)

def terr_h1(t):
    if len(t) == 3: return "Arkansas and the Mid-Atlantic"
    names = {"ar": "Arkansas", "md": "Maryland, DC and Delaware", "va": "Virginia and the Carolinas"}
    if t == ["ar", "va"]: return "Arkansas, Virginia and the Carolinas"
    return " and ".join(names[x] for x in t)
def terr_tag(t): return "All territories" if len(t) == 3 else terr_abbr(t)
def terr_abbr(t): return ", ".join({"ar": "AR", "md": "MD, DC, DE", "va": "VA, NC, SC"}[x] for x in t)
def terr_long(t):
    n = {"ar": "Arkansas", "md": "Maryland, DC and Delaware", "va": "Virginia, North Carolina and South Carolina"}
    return "; ".join(n[x] for x in t) if len(t) > 1 else n[t[0]]
def terr_chips(t, depth, sub=""):
    """Links to each territory's page, or to a page under it such as "pumps/" or "pump-repair/"."""
    return '<ul class="chips">' + "".join(f'<li><a href="{href(depth, "locations/" + TERR[x][0] + "/" + sub)}">{TERR[x][1]}</a></li>' for x in t) + "</ul>"

ORG = {"@type": "Organization", "@id": SITE + "#org", "name": "Southern Design and Mechanical, Inc.", "alternateName": ["Southern Design", "SD&M"],
       "url": SITE, "logo": SITE + "assets/logo.svg", "telephone": "+1-877-917-8677", "email": "info@southerndesign.com",
       "sameAs": ["https://www.linkedin.com/company/southern.design"],
       "areaServed": ["Arkansas", "Maryland", "District of Columbia", "Delaware", "Virginia", "North Carolina", "South Carolina"],
       "address": [{"@type": "PostalAddress", "streetAddress": "2710 North West Avenue", "addressLocality": "El Dorado", "addressRegion": "AR", "postalCode": "71730", "addressCountry": "US"},
                   {"@type": "PostalAddress", "streetAddress": "8229 Cloverleaf Drive, Suite 430", "addressLocality": "Millersville", "addressRegion": "MD", "postalCode": "21108", "addressCountry": "US"}]}
ORG_REF = {"@id": SITE + "#org"}

def crumbs_schema(crumbs):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p} for i, (n, p) in enumerate(crumbs)]}
def faq_schema(faq):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": strip_links(a)}} for q, a in faq]}

NAV = [("Products", "products/"), ("Services", "services/"), ("Pump problems", "problems/"), ("Industries", "industries/"), ("Locations", "locations/")]

ICON_SEARCH = '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg>'

def search_form(place, depth):
    """A search box. place: "hero" (home page), "head" (the panel under the header) or "page" (the search page).
    Without JavaScript it is a plain form that opens the search page, which lists everything."""
    return f'''<form class="search" role="search" action="{href(depth, "search/")}" method="get" data-search="{place}" data-index="{pre(depth)}assets/search.json" data-root="{pre(depth)}">
  <label for="q-{place}">Search by problem, manufacturer or product</label>
  <div class="search-box">
    <input id="q-{place}" name="q" type="search" placeholder="e.g. seal leaking, Ebara" autocomplete="off" autocapitalize="off" spellcheck="false" enterkeyhint="search">
    <button class="search-go" type="submit" aria-label="Search">{ICON_SEARCH}</button>
  </div>
  <div class="search-pop" hidden></div>
  <p class="vh" role="status"></p>
</form>'''

def header(depth, here=""):
    nav = "".join(f'<a href="{href(depth, p)}"{" aria-current=\"page\"" if here.startswith(p) else ""}>{n}</a>' for n, p in NAV)
    return f'''<a class="skip" href="#main">Skip to content</a>
<div class="ribbon">Concept redesign prepared by Lucid. This is not the live Southern Design website.</div>
<div class="utility"><div class="wrap">
  <span>Pump down? Call <a href="tel:{TEL}"><strong>{PHONE}</strong></a></span>
  <a class="portal" href="http://rms.mysoutherndesign.com/client">Customer portal sign in</a>
</div></div>
<header class="site-head"><div class="wrap">
  <a class="brand" href="{href(depth, "")}" aria-label="Southern Design home">
    <img class="brand-mark" src="{pre(depth)}assets/logo.svg?v={V_LOGO}" alt="" width="50" height="62">
    <span class="brand-name"><b>SOUTHERN</b> DESIGN<span class="brand-sub">Redefining Reliability</span></span>
  </a>
  <a class="search-btn in-bar" href="{href(depth, "search/")}" aria-label="Search">{ICON_SEARCH}</a>
  <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav">Menu</button>
  <nav class="nav" id="nav" aria-label="Main">{nav}<a class="search-btn" href="{href(depth, "search/")}" aria-label="Search">{ICON_SEARCH}</a><a class="btn btn-signal" href="{href(depth, "contact/")}">Request a quote</a></nav>
</div>
<div class="search-panel" id="search-panel" hidden><div class="wrap"><div class="search-dock">{search_form("head", depth)}<button class="search-close" type="button" aria-label="Close search"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="m6 6 12 12M18 6 6 18"/></svg></button></div></div></div>
</header>'''

def footer(depth):
    h = lambda p: href(depth, p)
    col = lambda title, items: f"<div><b>{title}</b><ul>" + "".join(f'<li><a href="{h(p)}">{n}</a></li>' for n, p in items) + "</ul></div>"
    return f'''<footer class="foot"><div class="wrap">
  <div class="foot-grid">
    <div>
      <img class="foot-mark" src="{pre(depth)}assets/logo.svg?v={V_LOGO}" alt="" width="44" height="54" loading="lazy">
      <b>Southern Design and Mechanical, Inc.</b>
      <p>Pumps, mechanical seals, valves and reliability services for industrial plants and water utilities.</p>
      <ul><li><a href="tel:{TEL}">{PHONE}</a></li><li><a href="mailto:info@southerndesign.com">info@southerndesign.com</a></li></ul>
    </div>
    {col("Products", [(CATS[c][2], "products/" + CATS[c][0] + "/") for c in ["pumps", "seals", "valves", "motors", "reliability"]] + [("All manufacturers", "manufacturers/")])}
    {col("Services", [(s["nav"], "services/" + s["slug"] + "/") for s in SERVICES])}
    {col("Pump problems", [(g["nav"], "problems/" + g["slug"] + "/") for g in GUIDES[:6]] + [("All guides", "problems/")])}
    {col("Company", [("About", "about/"), ("Industries", "industries/")] + [(TERR[t][1], "locations/" + TERR[t][0] + "/") for t in TERR] + [("Contact", "contact/")])}
  </div>
  <div class="foot-base">Concept redesign prepared by Lucid for discussion. Company details taken from the public Southern Design website. Photos are free-licence stock from Unsplash, standing in until Southern Design supplies its own.</div>
</div></footer>
<div class="actionbar"><a class="btn btn-ghost" href="tel:{TEL}">Call</a><a class="btn btn-signal" href="{h("contact/")}">Request a quote</a></div>
<script src="{pre(depth)}assets/site.js?v={V_JS}" defer></script>'''

def full_title(t): return t if "Southern Design" in t or len(t) > 46 else t + " | Southern Design"

def write(path, title, desc, body, schema, kind, query, depth=None, noindex=False):
    depth = path.count("/") if depth is None else depth
    canon = SITE + path
    t = full_title(title)
    robots = '\n<meta name="robots" content="noindex, nofollow">' if noindex else ROBOTS_META
    graph = {"@context": "https://schema.org", "@graph": schema}
    og_image = ""
    if path in PHOTO:
        og_image = f'\n<meta property="og:image" content="{photo_url(PHOTO[path][0], 1200)}">\n<meta property="og:image:alt" content="{esc(PHOTO[path][1])}">'
    doc = f'''<!doctype html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">{robots}{ga_snippet(kind)}
<title>{esc(t)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canon}">
<meta property="og:type" content="{"article" if kind == "Problem guide" else "website"}">
<meta property="og:site_name" content="Southern Design">
<meta property="og:title" content="{esc(t)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canon}">{og_image}
<meta name="twitter:card" content="{"summary_large_image" if og_image else "summary"}">
<link rel="icon" href="{pre(depth)}assets/logo.svg" type="image/svg+xml">
<link rel="preload" href="{pre(depth)}assets/fonts/open-sans.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://images.unsplash.com">{preloads(path, depth)}
<style>{page_css(depth)}</style>
<script type="application/ld+json">{json.dumps(graph, ensure_ascii=False)}</script>
</head>
<body>
{header(depth, path)}
{body}
{footer(depth)}
</body>
</html>
'''
    os.makedirs(os.path.join(OUT, path), exist_ok=True)
    open(os.path.join(OUT, path, "index.html"), "w").write(doc)
    if not noindex:  # utility pages stay out of the sitemap and the page map
        PAGES.append(dict(url="/" + path, kind=kind, query=query, title=t, description=desc))

LOGO_ALT = {s: "Pentair logo, covering Aurora, Myers, Fairbanks Nijhuis and Aplex" for s in ("aplex", "aurora", "fairbanks", "myers")}

def logo_size(f):
    """width and height attributes for a logo file, so the page does not shift when it loads."""
    try:
        from PIL import Image
        w, h = Image.open(f).size
        return f' width="{w}" height="{h}"'
    except Exception:
        return ""

def brand_logo(slug, name, depth):
    """Logo plate for a manufacturer page, if a logo file exists in src/logos/."""
    for ext in ("svg", "png", "webp", "jpg"):
        if os.path.exists(f"logos/{slug}.{ext}"):
            return f'<div class="brand-plate"><img src="{pre(depth)}assets/brands/{slug}.{ext}" alt="{esc(LOGO_ALT.get(slug, name + " logo"))}"{logo_size(f"logos/{slug}.{ext}")}></div>'
    return ""

def inner(path, crumbs, h1, lede, main_html, aside_html, extra_head="", plate=""):
    depth = path.count("/")
    trail = " / ".join(f'<a href="{href(depth, p)}">{n}</a>' for n, p in crumbs[:-1]) + (" / " if len(crumbs) > 1 else "") + f"<span>{crumbs[-1][0]}</span>"
    lay = f'<div class="wrap layout"><article class="prose">{main_html}</article><aside>{aside_html}</aside></div>' if aside_html else f'<div class="wrap page-body">{main_html}</div>'
    cls, style = "page-head", ""
    if path in PHOTO:
        pid = PHOTO[path][0]
        cls += " has-photo"
        style = f' style="--photo: url(\'{photo_url(pid, 1800)}\'); --photo-sm: url(\'{pre(depth)}img/m/photo-{pid}\')"'
    return f'''<main id="main">
<div class="{cls}"{style}><div class="wrap{" with-plate" if plate else ""}">
  <div>
  <nav class="crumbs" aria-label="Breadcrumb">{trail}</nav>
  <h1>{h1}</h1>
  <p class="lede">{lede}</p>{extra_head}
  </div>{plate}
</div></div>
{lay}
</main>'''

def cta(depth, head, text, btn, need="quote", about=""):
    q = f"?need={need}" + (f"&about={about.replace(' ', '%20')}" if about else "")
    return f'''<div class="aside-card"><h2>{head}</h2><p>{text}</p>
<a class="phone" href="tel:{TEL}">{PHONE}</a>
<a class="btn btn-signal" href="{href(depth, "contact/")}{q}">{btn}</a></div>'''

def side_list(title, items, depth):
    return f'<div class="aside-list"><h2>{title}</h2><ul>' + "".join(f'<li><a href="{href(depth, p)}">{n}</a></li>' for n, p in items) + "</ul></div>"

def rows(items, depth):
    return '<ul class="rows">' + "".join(f'<li><b><a href="{href(depth, p)}">{n}</a></b><span>{links(d, depth)}</span></li>' for n, p, d in items) + "</ul>"

HOME_C = [("Home", "")]
PT_SLUG = {p["pt"]: p["slug"] for p in PUMP_PAGES}
def lower1(t): return t if t[:2].isupper() else t[0].lower() + t[1:]
def pt_link(pt): return f"[[products/pumps/{PT_SLUG[pt]}/|{pt}]]" if pt in PT_SLUG else pt
# Title nouns follow what buyers search (OpenSEO, Nov 2026): "Cla-Val valves" 4,400/mo, "Graco pumps" 1,300, "Ebara pumps" 1,000,
# "Sulzer pumps" 1,000, "Toshiba motors" 480 and "Toshiba VFD" 260, "Finish Thompson pumps" 320, "Hisco pumps" 210, "Trico oiler" 170.
TNOUN = {"blacoh": "pulsation dampeners", "finish-thompson": "pumps", "graco": "pumps", "lube-it": "lubrication software", "amrri": "lubrication training",
         "richter": "PFA-lined pumps", "load-controls": "power monitors", "cla-val": "valves", "ebara": "pumps", "sulzer": "pumps and mixers",
         "toshiba": "motors and VFDs", "trico": "oilers", "hisco": "pumps and ANSI parts", "us-seal": "mechanical seals"}

# ---------- problem guides
for g in GUIDES:
    path = f"problems/{g['slug']}/"; d = 2
    crumbs = HOME_C + [("Pump problems", "problems/"), (g["nav"], path)]
    body = f'<div class="answer"><b>Short answer</b><p>{g["short"]}</p></div>\n' + table(g["table"], d)
    for h, bl in g["sections"]: body += f"\n<h2>{h}</h2>\n" + blocks(bl, d)
    body += "\n" + faq_html(g["faq"], d)
    body += '\n<h2>Products and services that help</h2>\n<ul class="chips">' + "".join(f'<li><a href="{href(d, "services/" + s + "/")}">{S[s]["nav"]}</a></li>' for s in g["services"]) + "".join(f'<li><a href="{href(d, "manufacturers/" + b + "/")}">{B[b]["name"]} {B[b]["noun"]}</a></li>' for b in g["brands"]) + "</ul>"
    body += '\n<p class="meta-line">Written by the Southern Design reliability team. Last reviewed October 2026.</p>'
    aside = cta(d, "Pump giving you trouble?", "Tell a reliability specialist what it is doing. We troubleshoot on site and find the cause.", "Book a troubleshooting visit", "troubleshoot") \
        + side_list("More pump problems", [(x["nav"], f"problems/{x['slug']}/") for x in GUIDES if x is not g], d)
    schema = [ORG, {"@type": "TechArticle", "headline": g["h1"], "description": g["meta"], "datePublished": DATE, "dateModified": DATE, "author": ORG_REF, "publisher": ORG_REF, "mainEntityOfPage": SITE + path}, faq_schema(g["faq"]), crumbs_schema(crumbs)]
    write(path, g["title"], g["meta"], inner(path, crumbs, g["h1"], "", body, aside), schema, "Problem guide", g["query"])

path = "problems/"; crumbs = HOME_C + [("Pump problems", path)]
body = rows([(g["h1"], f"problems/{g['slug']}/", g["meta"]) for g in GUIDES], 1)
write(path, "Pump Problems Solved: Troubleshooting Guides", "Plain answers to the pump problems that cost plants the most: seal failures, cavitation, bearing failures, water hammer, mag-drive failures and more.",
      inner(path, crumbs, "Pump problems, and what fixes them", "Plain answers to the failures that cost plants the most, written by the people who repair the equipment.", body, ""),
      [ORG, crumbs_schema(crumbs)], "Hub", "pump troubleshooting guide")

# ---------- services
for s in SERVICES:
    path = f"services/{s['slug']}/"; d = 2
    crumbs = HOME_C + [("Services", "services/"), (s["nav"], path)]
    body = ""
    for h, bl in s["sections"]: body += f"\n<h2>{h}</h2>\n" + blocks(bl, d)
    body += "\n<h2>Where we provide it</h2>\n<p>Across Southern Design's territories, from offices in El Dorado, Arkansas and Millersville, Maryland.</p>" + terr_chips(["ar", "md", "va"], d, "pump-repair/" if s["slug"] == "pump-repair" else "")
    body += "\n" + faq_html(s["faq"], d)
    aside = cta(d, "Talk to a specialist", "Tell us the equipment and what you need. It goes to the specialist for your state.", "Request service", {"pump-repair": "repair", "mechanical-seal-repair": "repair", "reliability-management": "rms", "lubrication-training-audits": "training"}.get(s["slug"], "troubleshoot")) \
        + side_list("Related guides", [(G[x]["nav"], f"problems/{x}/") for x in s["guides"]], d)
    schema = [ORG, {"@type": "Service", "name": s["nav"], "serviceType": s["stype"], "description": s["meta"], "provider": ORG_REF, "areaServed": ORG["areaServed"], "url": SITE + path}, faq_schema(s["faq"]), crumbs_schema(crumbs)]
    write(path, s["title"], s["meta"], inner(path, crumbs, s["h1"], s["lede"], body, aside), schema, "Service", s["query"])

path = "services/"; crumbs = HOME_C + [("Services", path)]
write(path, "Pump Repair, Field Service and Reliability Services", "Pump and seal repair, field service, hydraulic system analysis, reliability management and ICML lubrication training from Southern Design.",
      inner(path, crumbs, "Repair, field service and reliability engineering", "The same people who quote the part can fix it, install it and work out why the last one failed.", rows([(s["nav"], f"services/{s['slug']}/", s["lede"]) for s in SERVICES], 1), ""),
      [ORG, crumbs_schema(crumbs)], "Hub", "pump services")

# ---------- manufacturers
for b in B.values():
    path = f"manufacturers/{b['slug']}/"; d = 2
    cat = CATS[b["cat"]]
    crumbs = HOME_C + [("Products", "products/"), (cat[2], f"products/{cat[0]}/"), (b["name"], path)]
    h1 = f"{b['name']} {b['noun']} in {terr_h1(b['terr'])}"
    lede = b["line"]
    body = f"<h2>What we supply</h2>\n<ul>" + "".join(f"<li>{i}</li>" for i in b["items"]) + "</ul>"
    body += f"\n<h2>Where we supply {b['name']}</h2>\n<p>{b['name']} is on Southern Design's line card in the territories below. Lines differ by state, so if yours is not listed, ask and we will point you to the right product.</p>" + terr_chips(b["terr"], d, cat[0] + "/")
    sup = ["Selection and sizing for your liquid, flow and pressure, backed by [[services/hydraulic-system-analysis/|hydraulic system analysis]] where the system is the question"]
    if b["cat"] in ("pumps", "seals"): sup.append("[[services/pump-repair/|Repair]] with root cause failure analysis when something fails")
    if b["cat"] == "seals": sup.append("[[services/mechanical-seal-repair/|Seal repair and exchange programs]]")
    sup.append("[[services/field-service/|Field service]] for installation and troubleshooting")
    sup.append("[[services/reliability-management/|Reliability management]] for plants that want the failures tracked and reduced")
    body += "\n<h2>Support that comes with it</h2>\n" + blocks([sup], d)
    if b["guides"]:
        body += "\n<h2>Related pump problems</h2>\n" + blocks([[f"[[problems/{x}/|{G[x]['h1']}]]" for x in b["guides"]]], d)
    aside = cta(d, f"Get a {b['name']} quote", "Send the application or the part number. We size it, quote it and tell you the lead time.", "Request a quote", "quote", b["name"]) \
        + side_list(f"More {cat[2].lower()}", [(x["name"], f"manufacturers/{x['slug']}/") for x in B.values() if x["cat"] == b["cat"] and x is not b][:10], d)
    short = "AR, MD, VA, NC, SC" if len(b["terr"]) == 3 else terr_abbr(b["terr"])
    tn = TNOUN.get(b["slug"], b["noun"])
    title = f"{b['name']} {tn} distributor in {short}"
    if len(title) > 62: title = f"{b['name']} {tn} | {short}"
    meta = f"{b['name']} {b['noun']} supplied and supported by Southern Design in {terr_h1(b['terr'])}. Request a quote or speak to a specialist."
    if len(meta) > 160: meta = meta.replace(" Request a quote or speak to a specialist.", " Request a quote.")
    schema = [ORG, {"@type": "WebPage", "name": h1, "url": SITE + path, "about": {"@type": "Brand", "name": b["name"]}, "provider": ORG_REF}, crumbs_schema(crumbs)]
    write(path, title, meta, inner(path, crumbs, h1, lede, body, aside, plate=brand_logo(b["slug"], b["name"], d)), schema, "Manufacturer", f"{b['name']} {b['noun']} distributor {terr_abbr(b['terr'])}")

path = "manufacturers/"; crumbs = HOME_C + [("Products", "products/"), ("Manufacturers", path)]
allb = sorted(B.values(), key=lambda x: x["name"].lower())
write(path, "Manufacturers We Represent: Pumps, Seals, Valves", "Every manufacturer on Southern Design's line card, from American Marsh to U.S. Seal, with what each makes and the states where we supply it.",
      inner(path, crumbs, "Every manufacturer we represent", "32 manufacturers across three territories. Find the name on your nameplate.", rows([(b["name"], f"manufacturers/{b['slug']}/", f"{b['line']} <em>{terr_tag(b['terr'])}</em>") for b in allb], 1), ""),
      [ORG, crumbs_schema(crumbs)], "Hub", "pump manufacturers represented")

# ---------- product categories
CAT_COPY = {
 "pumps": ("Industrial pumps for process, water and chemical duty", "Centrifugal, magnetic drive, diaphragm, gear, reciprocating and submersible pumps, sized for the duty and supported after the sale.", "Industrial pump supplier in AR, MD, VA, NC, SC", "industrial pump supplier Arkansas / Maryland / Virginia"),
 "seals": ("Mechanical seals and seal support", "Cartridge, component, metal bellows and split seals, with the repair, exchange and failure analysis that stop repeat failures.", "Mechanical seal supplier in AR, MD, VA, NC, SC", "mechanical seal distributor Arkansas / Maryland"),
 "valves": ("Valves and valve automation", "Automatic control valves, isolation and check valves, lined valves for corrosive service, and positioners.", "Industrial valves and automation | AR, MD, VA, NC, SC", "industrial valve supplier Arkansas / Maryland"),
 "motors": ("Motors and drives", "Electric motors, variable frequency drives and control panels, plus power monitors that protect the pump.", "Industrial motors and drives | AR, MD, VA, NC, SC", "Toshiba motor distributor Arkansas / Maryland"),
 "reliability": ("Reliability accessories for pumps and rotating equipment", "The equipment that keeps a pump running between repairs: bearing protection, lubrication, baseplates, monitoring and surge control.", "Pump reliability accessories | AR, MD, VA, NC, SC", "bearing isolators, pulsation dampeners, pump power monitors"),
}
for c, (cslug, cname, cnav) in CATS.items():
    path = f"products/{cslug}/"; d = 2
    crumbs = HOME_C + [("Products", "products/"), (cnav, path)]
    h1, lede, title, query = CAT_COPY[c]
    body = ""
    members = [b for b in B.values() if b["cat"] == c]
    if c == "pumps":
        body += table(("Pump types and who makes them", ["Pump type", "Manufacturers"], [[pt_link(t), ", ".join(f"[[manufacturers/{s}/|{B[s]['name']}]]" for s in sl)] for t, sl in PUMP_TYPES]), d)
    if c == "valves": members = members + [B["richter"]]
    if c == "motors": members = members + [B["load-controls"]]
    if c == "seals": members = members + [B["safematic"]]
    body += f"\n<h2>Manufacturers</h2>\n" + rows([(b["name"], f"manufacturers/{b['slug']}/", f"{b['line']} <em>{terr_tag(b['terr'])}</em>") for b in members], d)
    rel = {"pumps": ["pump-cavitation", "pump-running-off-curve", "repair-or-replace-pump", "mag-drive-pump-failure"], "seals": ["mechanical-seal-keeps-failing"], "valves": ["water-hammer-pulsation"], "motors": ["pump-running-off-curve"], "reliability": ["pump-bearing-failure", "water-hammer-pulsation", "calculate-pump-mtbf"]}[c]
    body += "\n<h2>Related pump problems</h2>\n" + blocks([[f"[[problems/{x}/|{G[x]['h1']}]]" for x in rel]], d)
    body += f"\n<h2>{cnav} by territory</h2>\n<p>Lines differ by state. See what is on the line card where you are.</p>" + terr_chips(["ar", "md", "va"], d, cslug + "/")
    write(path, title, (lede if len(lede) > 115 else lede + " Supplied across Arkansas and the Mid-Atlantic."),
          inner(path, crumbs, h1, lede, f'<div class="prose wide">{body}</div>', ""), [ORG, crumbs_schema(crumbs)], "Product category", query)

# ---------- pump types: one page each (keyword research showed buyers search by pump type)
PT_MAKERS = dict(PUMP_TYPES)
for p in PUMP_PAGES:
    path = f"products/pumps/{p['slug']}/"; d = 3
    crumbs = HOME_C + [("Products", "products/"), ("Pumps", "products/pumps/"), (p["nav"], path)]
    makers = [B[x] for x in PT_MAKERS[p["pt"]]]
    terr = sorted({t for m in makers for t in m["terr"]}, key=["ar", "md", "va"].index)
    body = f"<h2>How it works</h2>\n<p>{links(p['how'], d)}</p>"
    body += "\n<h2>Where it fits</h2>\n" + blocks([p["good"]], d)
    body += "\n<h2>Where it does not</h2>\n" + blocks([p["limits"]], d)
    body += f"\n<h2>Who makes the {lower1(p['nav'])} we supply</h2>\n" + rows([(m["name"], f"manufacturers/{m['slug']}/", f"{m['line']} <em>{terr_tag(m['terr'])}</em>") for m in makers], d)
    body += "\n<h2>What to send for a quote</h2>\n" + blocks([["The liquid, its temperature, and any solids or chemicals in it", "The flow and pressure (or head) you need", "What it is replacing, with the nameplate if there is one", "How it runs: continuous, batch or standby, and anything that has failed before"]], d)
    body += "\n" + faq_html(p["faq"], d)
    body += "\n<h2>Related pump problems</h2>\n" + blocks([[f"[[problems/{x}/|{G[x]['h1']}]]" for x in p["guides"]]], d)
    aside = cta(d, f"Need {lower1(p['nav'])}?", "Send the duty or the nameplate. We size it, quote it and tell you the lead time.", "Request a quote", "quote", p["nav"]) \
        + side_list("Other pump types", [(x["nav"], f"products/pumps/{x['slug']}/") for x in PUMP_PAGES if x is not p], d)
    short = "AR, MD, VA, NC, SC" if len(terr) == 3 else terr_abbr(terr)
    title = p["title"] if len(p["title"]) + len(short) + 3 > 62 else f"{p['title']} | {short}"
    schema = [ORG, {"@type": "WebPage", "name": p["h1"], "description": p["meta"], "url": SITE + path, "provider": ORG_REF}, faq_schema(p["faq"]), crumbs_schema(crumbs)]
    write(path, title, p["meta"], inner(path, crumbs, p["h1"], links(p["lede"], d), body, aside), schema, "Pump type", p["query"])

path = "products/"; crumbs = HOME_C + [("Products", path)]
body = rows([(CATS[c][1], f"products/{CATS[c][0]}/", CAT_COPY[c][1]) for c in CATS] + [("All manufacturers", "manufacturers/", "The full line card, A to Z, with the states where we supply each.")], 1)
write(path, "Pumps, Mechanical Seals, Valves, Motors and Accessories", "Pumps, mechanical seals, valves, motors and reliability accessories from 32 manufacturers, supplied and supported across Arkansas and the Mid-Atlantic.",
      inner(path, crumbs, "Products from 32 manufacturers, supported after the sale", "Pick a category, or go straight to the manufacturer on your nameplate.", body, ""), [ORG, crumbs_schema(crumbs)], "Hub", "pumps seals valves supplier")

# ---------- industries
for i in INDUSTRIES:
    path = f"industries/{i['slug']}/"; d = 2
    crumbs = HOME_C + [("Industries", "industries/"), (i["name"], path)]
    body = f"<h2>What the duty demands</h2>\n<p>{i['duty']}</p>\n<h2>What we supply</h2>\n" + blocks([i["supply"]], d)
    body += "\n<h2>Problems we are called about</h2>\n" + blocks([[f"[[problems/{x}/|{G[x]['h1']}]]" for x in i["guides"]]], d)
    body += '\n<div class="slot"><span class="slot-kind">Case study needed from Southern Design</span><p>A short ' + i["name"].lower() + ' example with the plant type, the problem and the measured result belongs here.</p></div>'
    aside = cta(d, "Talk to a specialist", "Tell us about the plant and the equipment. It goes to the specialist for your state.", "Request a quote") + side_list("Other industries", [(x["name"], f"industries/{x['slug']}/") for x in INDUSTRIES if x is not i], d)
    write(path, f"{i['h1']}", i["meta"], inner(path, crumbs, i["h1"], "", body, aside), [ORG, crumbs_schema(crumbs)], "Industry", f"pumps for {i['name'].lower()} plants")
path = "industries/"; crumbs = HOME_C + [("Industries", path)]
write(path, "Industries We Serve: Chemical, Paper, Water, Power", "Southern Design supplies and supports pumps, seals and valves for chemical, pulp and paper, water, power, pharmaceutical, steel and bio-energy plants.",
      inner(path, crumbs, "Built around the plant you run", "What each industry asks of its pumps, and what we supply for it.", rows([(i["name"], f"industries/{i['slug']}/", i["duty"].split(". ")[0] + ".") for i in INDUSTRIES], 1), ""), [ORG, crumbs_schema(crumbs)], "Hub", "industrial pump supplier by industry")

# ---------- locations
LOC = {
 "ar": dict(h1="Pumps, seals, valves and pump repair in Arkansas", office="Corporate office", addr=["2710 North West Avenue", "El Dorado, AR 71730"], phone="(870) 725-2588", tel="+18707252588",
            lede="Southern Design's corporate office is in El Dorado. From here we supply pumps, mechanical seals and valves across Arkansas, repair what fails, and run reliability programs for plants that want fewer failures.",
            title="Pumps, Seals and Pump Repair in Arkansas | El Dorado", meta="Pump, mechanical seal and valve supply, pump repair and reliability services across Arkansas from Southern Design's corporate office in El Dorado.",
            query="pump repair El Dorado AR / pump distributor Arkansas", area=["Arkansas"],
            pa={"@type": "PostalAddress", "streetAddress": "2710 North West Avenue", "addressLocality": "El Dorado", "addressRegion": "AR", "postalCode": "71730", "addressCountry": "US"}),
 "md": dict(h1="Pumps, seals, valves and pump repair in Maryland, DC and Delaware", office="East Coast office", addr=["8229 Cloverleaf Drive, Suite 430", "Millersville, MD 21108"], phone=PHONE, tel=TEL,
            lede="Southern Design's East Coast office is in Millersville, Maryland, between Baltimore and Annapolis. We supply and support pumps, mechanical seals and valves for plants and utilities across Maryland, Washington DC and Delaware.",
            title="Pumps, Seals and Pump Repair in Maryland, DC, Delaware", meta="Pump, John Crane mechanical seal and valve supply, pump repair and reliability services in Maryland, DC and Delaware from Southern Design in Millersville, MD.",
            query="pump distributor Maryland / pump repair Baltimore", area=["Maryland", "District of Columbia", "Delaware"],
            pa={"@type": "PostalAddress", "streetAddress": "8229 Cloverleaf Drive, Suite 430", "addressLocality": "Millersville", "addressRegion": "MD", "postalCode": "21108", "addressCountry": "US"}),
 "va": dict(h1="Pumps, seals, valves and pump repair in Virginia and the Carolinas", office="Regional specialists", addr=["Covering Virginia, North Carolina and South Carolina"], phone=PHONE, tel=TEL,
            lede="Southern Design's regional specialists supply and support pumps, mechanical seals and valves for plants and utilities across Virginia, North Carolina and South Carolina.",
            title="Pumps, Seals and Pump Repair in Virginia, NC and SC", meta="Pump, mechanical seal and valve supply, pump repair and reliability services across Virginia, North Carolina and South Carolina from Southern Design.",
            query="pump distributor Virginia / North Carolina / South Carolina", area=["Virginia", "North Carolina", "South Carolina"], pa=None),
}
for t, L in LOC.items():
    slug, tname, _ = TERR[t]; path = f"locations/{slug}/"; d = 2
    crumbs = HOME_C + [("Locations", "locations/"), (tname, path)]
    body = f"<h2>Manufacturers we represent in {tname}</h2>"
    for c in ["pumps", "seals", "motors", "valves", "reliability"]:
        ms = [b for b in B.values() if b["cat"] == c and t in b["terr"]]
        if c == "valves" and t in B["richter"]["terr"]: ms.append(B["richter"])
        if not ms: continue
        body += f'\n<h3><a href="{href(d, path + CATS[c][0] + "/")}">{CATS[c][2]} in {tname}</a></h3>\n<ul>' + "".join(f'<li><a href="{href(d, "manufacturers/" + b["slug"] + "/")}">{b["name"]}</a>: {b["noun"]}</li>' for b in ms) + "</ul>"
    body += f"\n<h2>Services in {tname}</h2>\n" + blocks([[f"[[{path}pump-repair/|Pump repair in {tname}]]"] + [f"[[services/{s['slug']}/|{s['nav']}]]" for s in SERVICES if s["slug"] != "pump-repair"]], d)
    body += "\n<h2>Problems we are called about</h2>\n" + blocks([[f"[[problems/{g['slug']}/|{g['h1']}]]" for g in GUIDES[:5]]], d)
    aside = f'''<div class="aside-card"><h2>{L["office"]}</h2><address>{"<br>".join(L["addr"])}</address>
<a class="phone" href="tel:{L["tel"]}">{L["phone"]}</a>
<a class="btn btn-signal" href="{href(d, "contact/")}?need=quote">Request a quote</a></div>''' + side_list("Other territories", [(TERR[x][1], f"locations/{TERR[x][0]}/") for x in TERR if x != t], d)
    lb = {"@type": "LocalBusiness", "name": f"Southern Design, {tname}", "url": SITE + path, "telephone": L["tel"], "parentOrganization": ORG_REF, "areaServed": L["area"], "image": SITE + "assets/logo.svg"}
    if L["pa"]: lb["address"] = L["pa"]
    schema = [ORG, lb if L["pa"] else {"@type": "Service", "name": f"Pump supply and repair in {tname}", "provider": ORG_REF, "areaServed": L["area"], "url": SITE + path}, crumbs_schema(crumbs)]
    write(path, L["title"], L["meta"], inner(path, crumbs, L["h1"], L["lede"], body, aside), schema, "Location", L["query"])
# ---------- state pages: one per product category, plus pump repair, for each territory
# Buyers search by state ("pump distributor Arkansas"), and the lines differ by state, so each territory gets its own pages.
ST_TITLE = {"ar": "Arkansas", "md": "Maryland, DC, Delaware", "va": "Virginia, NC and SC"}
ST_WHERE = {"ar": "across Arkansas, from its corporate office in El Dorado",
            "md": "across Maryland, Washington DC and Delaware, from its East Coast office in Millersville, between Baltimore and Annapolis",
            "va": "across Virginia, North Carolina and South Carolina, through its regional specialists"}
ST_OFFICE_FAQ = {"ar": "The corporate office is at 2710 North West Avenue, El Dorado, AR 71730. Call (870) 725-2588.",
                 "md": "The East Coast office is at 8229 Cloverleaf Drive, Suite 430, Millersville, MD 21108, between Baltimore and Annapolis. Call 877-917-8677.",
                 "va": "There is no walk-in office in the territory. Regional specialists cover Virginia, North Carolina and South Carolina. Call 877-917-8677."}
ST_CAT = {  # title, h1, plural noun for the FAQ, search it answers
 "pumps": ("Industrial Pump Distributor in {t}", "Industrial pump supplier and distributor in {n}", "pump", "pump distributor {s}"),
 "seals": ("Mechanical Seal Distributor in {t}", "Mechanical seal supplier and distributor in {n}", "mechanical seal", "mechanical seal distributor {s}"),
 "valves": ("Industrial Valve Supplier in {t}", "Industrial valve and valve automation supplier in {n}", "valve", "industrial valve supplier {s}"),
 "motors": ("Motors and Drives Supplier in {t}", "Motors, drives and pump protection in {n}", "motor and drive", "Toshiba motor distributor {s}"),
 "reliability": ("Pump Reliability Accessories in {t}", "Reliability accessories for pumps in {n}", "reliability accessory", "bearing isolators, pulsation dampeners {s}"),
}
ST_REL = {"pumps": ["pump-cavitation", "pump-running-off-curve", "repair-or-replace-pump", "mag-drive-pump-failure"], "seals": ["mechanical-seal-keeps-failing"], "valves": ["water-hammer-pulsation"],
          "motors": ["pump-running-off-curve"], "reliability": ["pump-bearing-failure", "water-hammer-pulsation", "pump-reliability-program"]}
ST_QUERY_STATE = {"ar": "Arkansas", "md": "Maryland", "va": "Virginia / North Carolina"}

def st_members(t, c):
    ms = [x for x in B.values() if x["cat"] == c and t in x["terr"]]
    extra = {"valves": "richter", "motors": "load-controls", "seals": "safematic"}.get(c)
    if extra and t in B[extra]["terr"]: ms.append(B[extra])
    return ms

def st_office(t, d):
    L = LOC[t]
    return f'''<div class="aside-card"><h2>{L["office"]}</h2><address>{"<br>".join(L["addr"])}</address>
<a class="phone" href="tel:{L["tel"]}">{L["phone"]}</a>
<a class="btn btn-signal" href="{href(d, "contact/")}?need=quote">Request a quote</a></div>'''

def st_more(t, d, skip):
    slug, tname, _ = TERR[t]
    items = [(f"{CATS[c][2]}", f"locations/{slug}/{CATS[c][0]}/") for c in CATS if st_members(t, c) and c != skip]
    if skip != "repair": items.append(("Pump repair", f"locations/{slug}/pump-repair/"))
    items.append((f"All of {tname}", f"locations/{slug}/"))
    return side_list(f"More in {tname}", items, d)

for t in TERR:
    slug, tname, tlong = TERR[t]; L = LOC[t]; d = 3
    for c in CATS:
        ms = st_members(t, c)
        if not ms: continue
        cslug, cname, cnav = CATS[c]
        path = f"locations/{slug}/{cslug}/"
        PHOTO[path] = PHOTO[f"locations/{slug}/"]
        crumbs = HOME_C + [("Locations", "locations/"), (tname, f"locations/{slug}/"), (cnav, path)]
        title, h1, noun, query = [x.format(t=ST_TITLE[t], n=tname, s=ST_QUERY_STATE[t]) for x in ST_CAT[c]]
        names = [x["name"] for x in ms]
        listed = ", ".join(names[:-1]) + (" and " if len(names) > 1 else "") + names[-1]
        lede = f"Southern Design supplies {cname.lower()} to plants and utilities {ST_WHERE[t]}. {len(ms)} manufacturer{'s' if len(ms) != 1 else ''} on the {tname} line card, with selection, repair and field service behind them."
        body = f"<h2>{cnav} we supply in {tname}</h2>\n" + rows([(x["name"], f"manufacturers/{x['slug']}/", x["line"]) for x in ms], d)
        if c == "pumps":
            have = {x["slug"] for x in ms}
            body += "\n" + table((f"Pump types available in {tname}", ["Pump type", "Manufacturers"],
                                  [[pt_link(pt), ", ".join(f"[[manufacturers/{s}/|{B[s]['name']}]]" for s in sl if s in have)] for pt, sl in PUMP_TYPES if any(s in have for s in sl)]), d)
        others = [x["name"] for x in B.values() if x["cat"] == c and t not in x["terr"]]
        if others:
            body += f"\n<h2>Not on the {tname} line card</h2>\n<p>{', '.join(others)}: supplied by Southern Design in other territories, not this one. If one of these is on your nameplate, ask and we will point you to the right product.</p>"
        sup = ["Selection and sizing for your liquid, flow and pressure, backed by [[services/hydraulic-system-analysis/|hydraulic system analysis]] where the system is the question"]
        if c in ("pumps", "seals"): sup.append(f"[[locations/{slug}/pump-repair/|Repair in {tname}]], with root cause failure analysis when something fails")
        if c == "seals": sup.append("[[services/mechanical-seal-repair/|Seal repair and exchange programs]]")
        sup += ["[[services/field-service/|Field service]] for installation and troubleshooting", "[[services/reliability-management/|Reliability management]] for plants that want the failures tracked and reduced"]
        body += "\n<h2>What comes with the product</h2>\n" + blocks([sup], d)
        body += "\n<h2>Related pump problems</h2>\n" + blocks([[f"[[problems/{x}/|{G[x]['h1']}]]" for x in ST_REL[c]]], d)
        faq = [(f"Which {noun} brands does Southern Design supply in {tname}?", f"{listed}. Lines differ by state, so this list is specific to {tlong}."),
               (f"Where is Southern Design's office for {tname}?", ST_OFFICE_FAQ[t])]
        if c in ("pumps", "seals"):
            faq.append((f"Do you repair {noun}s in {tname} as well as supply them?", f"Yes. See [[locations/{slug}/pump-repair/|pump repair in {tname}]]. Every repair comes with the cause of failure."))
        body += "\n" + faq_html(faq, d)
        aside = st_office(t, d) + st_more(t, d, c) + side_list(f"{cnav} in other territories", [(TERR[x][1], f"locations/{TERR[x][0]}/{cslug}/") for x in TERR if x != t and st_members(x, c)], d)
        tail = " Selection and field service." if c == "reliability" else " Selection, repair and field service."
        meta = f"{cname} for plants and utilities in {tname}: {listed}."
        if len(meta) < 125: meta += tail
        if len(meta) > 158: meta = f"{cname} in {tname} from {len(ms)} manufacturers, including {', '.join(names[:3])}.{tail}"
        schema = [ORG, {"@type": "Service", "name": h1, "serviceType": f"{cname} supply", "provider": ORG_REF, "areaServed": L["area"], "url": SITE + path}, faq_schema(faq), crumbs_schema(crumbs)]
        write(path, title, meta, inner(path, crumbs, h1, lede, body, aside), schema, "State product page", query)

    # pump repair in this territory
    path = f"locations/{slug}/pump-repair/"
    PHOTO[path] = PHOTO[f"locations/{slug}/"]
    crumbs = HOME_C + [("Locations", "locations/"), (tname, f"locations/{slug}/"), ("Pump repair", path)]
    h1 = f"Industrial pump repair in {tname}"
    lede = f"Southern Design repairs pumps, mechanical seals and other rotating equipment for plants and utilities {ST_WHERE[t]}. Every repair comes with the cause of failure, so you know what to change, not just what was replaced."
    pumps = st_members(t, "pumps"); seals = [x for x in st_members(t, "seals") if x["slug"] != "safematic"]
    body = "<h2>What we repair</h2>\n" + blocks([[
        "A wide variety of pumps and other rotating equipment",
        "Magnetic drive and mechanically sealed pumps",
        "Mechanical seals, with [[services/mechanical-seal-repair/|exchange programs]] so a rebuilt seal is ready when the next one is needed",
        f"Equipment from the lines we supply in {tname}: " + ", ".join(f"[[manufacturers/{x['slug']}/|{x['name']}]]" for x in pumps),
        f"Seals from " + ", ".join(f"[[manufacturers/{x['slug']}/|{x['name']}]]" for x in seals)]], d)
    body += f"\n<h2>How a repair runs</h2>\n" + blocks([("ol", [
        f'Call <a href="tel:{L["tel"]}">{L["phone"]}</a> or [[contact/|send the make, model and what happened]].',
        "We inspect the pump and report what failed and why.",
        "You approve the scope, including any upgrades worth making while it is apart.",
        "We repair it.",
        "The repair and its cause go into the pump's history. Contract customers see this in the [[services/reliability-management/|Reliability Management System]]."])], d)
    body += f"\n<h2>At your plant</h2>\n<p>Not every problem needs the pump pulled. On-site performance troubleshooting is part of the service, and [[services/field-service/|field service technicians]] work at plants in {tlong} by the day or as a turnkey job.</p>".replace("[[services/field-service/|field service technicians]]", f'<a href="{href(d, "services/field-service/")}">field service technicians</a>')
    body += "\n<h2>If the same pump keeps coming back</h2>\n" + blocks([[
        "[[problems/repair-or-replace-pump/|Repair or replace: how to decide]]",
        "[[problems/mechanical-seal-keeps-failing/|Why mechanical seals keep failing]]",
        "[[problems/pump-bearing-failure/|Why pump bearings fail early]]",
        "[[problems/pump-reliability-program/|How to set up a pump reliability program]]"]], d)
    body += f'\n<div class="slot"><span class="slot-kind">Needed from Southern Design</span><p>Where repairs for {tname} customers are carried out, what the shop can handle (lifting capacity, balancing, test stand), typical turnaround, and photos of the shop and the people. The pages that rank first for pump repair searches in this territory are built from exactly this.</p></div>'
    faq = [(f"What types of pump do you repair in {tname}?", "A wide variety of pumps and rotating equipment, including magnetic drive and mechanically sealed pumps. Send the make and model and we will confirm."),
           (f"Can someone come to our plant?", f"Yes. Field service technicians work on site in {tlong} by the day or as a turnkey job, and on-site performance troubleshooting is part of the repair service."),
           ("Where do I send a pump for repair?", f"Call {L['phone']} first. The specialist for {tname} will confirm where it should go."),
           ("Will you tell us why the pump failed?", "Yes. Root cause failure analysis and reporting is part of the service for pumps and mechanical seals.")]
    if t == "md": faq.insert(2, ("Do you cover Baltimore?", "Yes. The Millersville office is between Baltimore and Annapolis and covers Maryland, Washington DC and Delaware."))
    body += "\n" + faq_html(faq, d)
    aside = st_office(t, d).replace("Request a quote</a>", "Arrange a repair</a>").replace("?need=quote", "?need=repair") + st_more(t, d, "repair") \
        + side_list("Pump repair in other territories", [(TERR[x][1], f"locations/{TERR[x][0]}/pump-repair/") for x in TERR if x != t], d)
    title = f"Industrial Pump Repair in {ST_TITLE[t]}"
    meta = f"Pump and mechanical seal repair for plants and utilities in {tname}, with root cause failure analysis and field service. Call {L['phone']}."
    schema = [ORG, {"@type": "Service", "name": h1, "serviceType": "Industrial pump repair", "provider": ORG_REF, "areaServed": L["area"], "url": SITE + path}, faq_schema(faq), crumbs_schema(crumbs)]
    write(path, title, meta, inner(path, crumbs, h1, lede, body, aside), schema, "State service page", f"industrial pump repair {ST_QUERY_STATE[t]}")

path = "locations/"; crumbs = HOME_C + [("Locations", path)]
write(path, "Locations: Arkansas, Maryland, Virginia, the Carolinas", "Southern Design serves Arkansas from El Dorado, and Maryland, DC, Delaware, Virginia and the Carolinas from Millersville, Maryland.",
      inner(path, crumbs, "Find the specialist for your state", "Two offices, three territories. Lines differ by state, so start with yours.", rows([(TERR[t][1], f"locations/{TERR[t][0]}/", LOC[t]["lede"]) for t in TERR], 1), ""), [ORG, crumbs_schema(crumbs)], "Hub", "Southern Design locations")

# ---------- about + contact
path = "about/"; crumbs = HOME_C + [("About", path)]
body = '''<h2>What we do</h2>
<p>Southern Design supplies pumps, mechanical seals, valves and the accessories that keep them running, and provides the repair, field service and reliability engineering that find out why equipment fails. For over 20 years our people have provided sensible solutions to the industrial community.</p>
<h2>Our philosophy</h2>
<p>Southern Design is dedicated to being the premier industrial product provider. Our formula for success is providing superior products and services with superior people. Our commitment to solving the most difficult problems is what sets us apart.</p>
<h2>Where we work</h2>
<p>From a corporate office in El Dorado, Arkansas and an East Coast office in Millersville, Maryland, we serve Arkansas, Maryland, DC, Delaware, Virginia and the Carolinas.</p>
<div class="slot"><span class="slot-kind">Needed from Southern Design</span><p>The year the company was founded, the people customers will deal with (names, roles, years in the industry, certifications such as ICML), and any manufacturer awards or industry memberships. Named, qualified people are what buyers and search engines both look for on this page.</p></div>'''
write(path, "About Southern Design: Redefining Reliability", "Southern Design has supplied pumps, seals and valves and solved rotating equipment problems for over 20 years, from offices in El Dorado, AR and Millersville, MD.",
      inner(path, crumbs, "Ending unpredicted machine failures", "A product supplier and a reliability partner in one company.", body, cta(1, "Talk to a specialist", "Tell us what you need. It goes to the specialist for your state.", "Request a quote")), [ORG, {"@type": "AboutPage", "url": SITE + path, "about": ORG_REF}, crumbs_schema(crumbs)], "About", "Southern Design and Mechanical")

path = "contact/"; crumbs = HOME_C + [("Contact", path)]
body = f'''<div class="contact-grid">{form_html}
<div class="offices">
<h2>Arkansas</h2><address>Corporate office<br>2710 North West Avenue<br>El Dorado, AR 71730<br><a href="tel:+18707252588">(870) 725-2588</a></address>
<h2>Maryland, DC and Delaware</h2><address>East Coast office<br>8229 Cloverleaf Drive, Suite 430<br>Millersville, MD 21108<br><a href="tel:{TEL}">{PHONE}</a></address>
<h2>Virginia and the Carolinas</h2><address>Regional specialists<br><a href="tel:{TEL}">{PHONE}</a></address>
<h2>Email</h2><address><a href="mailto:info@southerndesign.com">info@southerndesign.com</a></address>
</div></div>'''
write(path, "Request a Quote or Service | Southern Design", "Request a quote for a pump, seal or valve, arrange a repair, or ask a reliability specialist for help. Call 877-917-8677 if equipment is down.",
      inner(path, crumbs, "Tell us what you need", f'Six fields. It goes to the specialist for your state, not a general inbox. If equipment is down, call <a href="tel:{TEL}">{PHONE}</a>.', body, ""), [ORG, {"@type": "ContactPage", "url": SITE + path}, crumbs_schema(crumbs)], "Contact", "Southern Design contact")

# Thank-you page: the live enquiry form redirects here after a successful submission.
# site.js counts a lead (generate_lead) when this page loads, so it must only be reached that way.
path = "contact/thanks/"; crumbs = HOME_C + [("Contact", "contact/"), ("Request received", path)]
body = f'''<div class="prose">
<h2>What happens next</h2>
<ol><li>Your request goes to the specialist for your state.</li><li>They call or email you back, usually within one working day.</li><li>You get a quote with a lead time, or a visit to find the cause.</li></ol>
<p>If equipment is down, do not wait for us. Call <a href="tel:{TEL}">{PHONE}</a>.</p>
<h2>While you wait</h2>
''' + blocks([[f"[[problems/{g['slug']}/|{g['h1']}]]" for g in GUIDES[:4]]], 2) + "</div>"
write(path, "Request received | Southern Design", "Your request has been sent to Southern Design.",
      inner(path, crumbs, "Request received", "Thank you. A specialist will be in touch.", body, ""), [ORG, crumbs_schema(crumbs)], "Thank you", "", noindex=True)

# ---------- search: the index the search boxes use, and a page that lists everything
INDEX = build_index(B, GUIDES, SERVICES, INDUSTRIES, CATS, CAT_COPY, TERR, LOC, PUMP_TYPES, terr_tag, st_members, PHONE)
path = "search/"; crumbs = HOME_C + [("Search", path)]
body = search_form("page", 1) + '\n<div class="browse">'
for head, kind in [("Pump problems", "Problem guide"), ("Manufacturers", "Manufacturer"), ("Products", "Product"), ("Pump types", "Pump type"), ("Services", "Service"), ("Industries", "Industry"), ("Locations", "Location")]:
    body += f'\n<h2>{head}</h2>\n<ul class="chips">' + "".join(f'<li><a href="{href(1, e["u"])}">{esc(e["t"])}</a></li>' for e in INDEX if e["k"] == kind and e["browse"]) + "</ul>"
body += "\n</div>"
write(path, "Search Southern Design: Problems, Manufacturers, Products", "Search Southern Design by pump problem, manufacturer or product, or browse every guide, manufacturer, product, service, industry and location.",
      inner(path, crumbs, "Find it fast", "Type what the pump is doing, the name on the nameplate, or what you need. Or browse everything below.", body, ""), [ORG, crumbs_schema(crumbs)], "Search", "")

# ---------- home
m = home_main
def rep(old, new, count=1):
    global m
    assert m.count(old) == count, (m.count(old), old[:60]); m = m.replace(old, new)
rep("28 manufacturers on the line card", "32 manufacturers represented")
rep('<div class="hero-cta">', search_form("hero", 0) + '\n      <div class="hero-cta">')
a = m.index('<div class="tabs" role="tablist"'); b = m.index("</p>", m.index('<p class="linecard-note">')) + 4
def lc(ms): return "".join(f'<li><b><a href="manufacturers/{x["slug"]}/index.html">{x["name"]}</a></b><small>{x["line"]} <em>{terr_tag(x["terr"])}</em></small></li>' for x in ms)
t1 = [x for x in B.values() if x["cat"] in ("pumps", "seals", "motors")]; t2 = [x for x in B.values() if x["cat"] == "reliability"]; t3 = [x for x in B.values() if x["cat"] == "valves"] + [B["richter"]]
m = m[:a] + f'''<div class="tabs" role="tablist" aria-label="Product categories">
        <button class="tab" role="tab" id="t-rot" aria-controls="p-rot" aria-selected="true">Pumps, seals and motors<span>{len(t1)}</span></button>
        <button class="tab" role="tab" id="t-rel" aria-controls="p-rel" aria-selected="false" tabindex="-1">Reliability accessories<span>{len(t2)}</span></button>
        <button class="tab" role="tab" id="t-val" aria-controls="p-val" aria-selected="false" tabindex="-1">Valves and automation<span>{len(t3)}</span></button>
      </div>
      <div id="p-rot" role="tabpanel" aria-labelledby="t-rot"><ul class="linecard">{lc(t1)}</ul></div>
      <div id="p-rel" role="tabpanel" aria-labelledby="t-rel" hidden><ul class="linecard">{lc(t2)}</ul></div>
      <div id="p-val" role="tabpanel" aria-labelledby="t-val" hidden><ul class="linecard">{lc(t3)}</ul></div>
      <p class="linecard-note">Lines differ by territory; the states are shown beside each name. Do not see the brand you run? <a href="contact/index.html">Ask us anyway</a>, or browse <a href="products/index.html">products by type</a>.</p>''' + m[b:]
prob = '''<section class="band band-panel" aria-labelledby="prob-h">
    <div class="wrap">
      <h2 id="prob-h">Common pump problems, and what fixes them</h2>
      <p class="lede">Plain answers to the failures that cost plants the most.</p>
      ''' + rows([(g["nav"], f"problems/{g['slug']}/", g["meta"]) for g in GUIDES], 0).replace('<ul class="rows">', '<ul class="rows" style="margin-top:40px">') + '''
    </div>
  </section>

  '''
rep('<section class="band band-panel" id="products"', prob + '<section class="band" id="products"')
for h, slug in [("Precision repair", "pump-repair"), ("Field service", "field-service"), ("Engineering and design", "hydraulic-system-analysis"), ("Lubrication training and audits", "lubrication-training-audits")]:
    rep(f"<h3>{h}</h3>", f'<h3><a href="services/{slug}/index.html">{h}</a></h3>')
for i in INDUSTRIES: rep(f"<li><b>{i['name']}</b>", f'<li><b><a href="industries/{i["slug"]}/index.html">{i["name"]}</a></b>')
for pdf, slug, txt in [("d78e79_1667c1e953b34f3a8f5403be2dc380fb", "arkansas", "Pumps, seals and repair in Arkansas"), ("d78e79_2519b643f9c7481893b1d2a020658922", "maryland-dc-delaware", "Pumps, seals and repair in MD, DC and DE"), ("d78e79_ff1181feb0bf49d4922d980c4e7fa8e3", "virginia-carolinas", "Pumps, seals and repair in VA, NC and SC")]:
    a = m.index(f'<a href="https://www.southerndesign.com/_files/ugd/{pdf}.pdf">'); b = m.index("</a>", a) + 4
    m = m[:a] + f'<a href="locations/{slug}/index.html">{txt}</a>' + m[b:]
rep('data-need="rms">Ask for a reliability assessment</a></div>', 'data-need="rms">Ask for a reliability assessment</a> <a class="text-link" href="services/reliability-management/index.html">How reliability management works</a></div>')
rep('href="#reliability">See how we cut repeat failures', 'href="problems/index.html">See what fixes repeat failures')
home_schema = [ORG, {"@type": "WebSite", "@id": SITE + "#site", "url": SITE, "name": "Southern Design", "publisher": ORG_REF}]
write("", "Pumps, Mechanical Seals, Valves and Pump Repair | Southern Design", "Southern Design supplies pumps, mechanical seals and valves, with pump repair, failure analysis and reliability management across AR, MD, DC, DE, VA, NC and SC.", m, home_schema, "Home", "pump and seal supplier with repair and reliability services", depth=0)

# ---------- assets
os.makedirs(OUT + "/assets/fonts")
for f in ("open-sans.woff2", "open-sans-italic.woff2", "OFL.txt"): shutil.copy("fonts/" + f, OUT + "/assets/fonts/" + f)
shutil.copy("logo.svg", OUT + "/assets/logo.svg")
shutil.copy("site.js", OUT + "/assets/site.js")
json.dump([{k: e[k] for k in "tkushw"} for e in INDEX], open(OUT + "/assets/search.json", "w"), ensure_ascii=False, separators=(",", ":"))
if os.path.isdir("logos") and os.listdir("logos"):
    shutil.copytree("logos", OUT + "/assets/brands")

PAGES.sort(key=lambda p: (p["url"].count("/"), p["url"]))
open(OUT + "/sitemap.xml", "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{SITE}{p['url'][1:]}</loc><lastmod>{DATE}</lastmod></url>\n" for p in PAGES) + "</urlset>\n")
CACHE = "/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n/assets/site.js\n  Cache-Control: public, max-age=31536000, immutable\n/assets/logo.svg\n  Cache-Control: public, max-age=31536000, immutable\n/assets/brands/*\n  Cache-Control: public, max-age=2592000\n"
if not LIVE:
    open(OUT + "/robots.txt", "w").write("# Preview build: not for indexing. Rebuild with --live for launch.\nUser-agent: *\nDisallow: /\n")
    open(OUT + "/_headers", "w").write("# Preview build. Format: Netlify / Cloudflare Pages.\n/*\n  X-Robots-Tag: noindex, nofollow\n" + CACHE)
else:
  open(OUT + "/_headers", "w").write("# Format: Netlify / Cloudflare Pages.\n" + CACHE)
  open(OUT + "/robots.txt", "w").write(f"""# Southern Design: open to search engines and AI search crawlers
User-agent: *
Allow: /

# AI search and assistant crawlers (named so the intent is explicit)
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: bingbot
User-agent: Applebot
Allow: /

Sitemap: {SITE}sitemap.xml
""")
open(OUT + "/_redirects", "w").write(f"""# The phone-sized home page photo, passed through from Unsplash so it loads from this site's own address (Netlify).
/img/hero-m.webp        {HERO_MOBILE_SRC}  200
# Phone-sized header photos for inner pages, passed through the same way.
/img/m/:photo           https://images.unsplash.com/:photo?fit=crop&w=640&h=420&q=50&fm=webp  200

# Old Wix URLs to new pages (301). Format: Netlify / Cloudflare Pages.
/about-sdm              /about/                            301
/product-solutions      /products/                         301
/reliability-solutions  /services/reliability-management/  301
/manufacturers          /manufacturers/                    301
/contact                /contact/                          301
""")
with open(OUT + "/seo-page-map.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["url", "kind", "query", "title", "description"]); w.writeheader(); w.writerows(PAGES)
from collections import Counter
print("LIVE build: open to search engines" if LIVE else "PREVIEW build: hidden from search engines (use --live for launch)")
print(len(PAGES), "pages", dict(Counter(p["kind"] for p in PAGES)))
print("search index:", len(INDEX), "entries,", os.path.getsize(OUT + "/assets/search.json"), "bytes")
print("long titles:", [(len(p["title"]), p["url"]) for p in PAGES if len(p["title"]) > 65])
print("long metas:", [(len(p["description"]), p["url"]) for p in PAGES if len(p["description"]) > 165])
