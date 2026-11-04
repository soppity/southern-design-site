"""The index behind the site's search box.

One entry per page a buyer might be looking for. Each entry has the title and one line that are shown in the results,
plus words that are matched but never shown: what the page covers, and the words buyers actually type
(symptoms, abbreviations, other spellings of a brand name).

build.py writes the result to site/assets/search.json. site.js fetches it the first time a search box is used."""
import re
from pumptypes import PUMP_PAGES

# Words buyers type that the page itself may not use. Only add a word where the page really answers it.
SAID_AS = {
 # problem guides: the symptom as an operator would describe it
 "mechanical-seal-keeps-failing": "seal leak leaking leaks leakage dripping seal failure failed seal faces o-ring flush short seal life",
 "pump-cavitation": "noise noisy loud gravel marbles rattling crackling npsh suction vibration pitting impeller damage",
 "pump-running-off-curve": "bep best efficiency point oversized throttled low flow high flow vibration recirculation overload amps motor tripping",
 "pump-bearing-failure": "bearing hot overheating temperature noisy bearing oil grease lubrication contamination vibration",
 "npsh-calculation": "npsh npsha npshr net positive suction head available required suction pressure vapor pressure margin cavitation boiling hot liquid",
 "calculate-pump-mtbf": "mtbf mean time between failures bad actors kpi metrics failure rate",
 "water-hammer-pulsation": "banging bang knocking hammering surge pulsation pipe shaking vibration slam pressure spike",
 "mag-drive-pump-failure": "magnetic drive magdrive sealless decoupling decoupled dry run dry running no flow overheating melted",
 "repair-or-replace-pump": "rebuild overhaul new pump old pump obsolete cost worth repairing",
 "pump-reliability-program": "reliability programme rcm preventive predictive maintenance plan fewer failures",
 # services
 "pump-repair": "rebuild overhaul fix broken failed repair shop rotating equipment rcfa root cause failure analysis",
 "mechanical-seal-repair": "seal rebuild seal exchange reconditioned",
 "field-service": "installation install technician on site onsite turnkey per diem maintenance outage troubleshooting",
 "hydraulic-system-analysis": "system curve simulation model sizing design engineering piping",
 "reliability-management": "rms reliability management system mtbf failure tracking root cause contract",
 "lubrication-training-audits": "icml mlt mla oil analysis lubrication course certification audit",
 # manufacturers: other spellings, parent brands, common abbreviations
 "american-marsh": "americanmarsh american-marsh",
 "aplex": "pentair plunger triplex",
 "aurora": "pentair",
 "fairbanks": "pentair fairbanks nijhuis fairbanks morse",
 "myers": "pentair",
 "finish-thompson": "fti finishthompson",
 "graco": "aodd quantm",
 "nomad": "aodd",
 "john-crane": "johncrane crane",
 "us-seal": "us seal usseal u s seal",
 "cla-val": "claval cla val",
 "flex-a-seal": "flexaseal flex a seal",
 "lube-it": "lubeit lube it",
 "load-controls": "loadcontrols",
 "basetek": "base tek",
 "toshiba": "vfd vsd variable speed drive",
 "blacoh": "dampener dampeners damper pulsation surge",
 "pmv": "positioner",
 # industries
 "chemical": "chemical plant corrosive acid caustic hazardous",
 "pulp-paper": "paper mill pulp mill stock",
 "water-wastewater": "municipal utility treatment plant lift station sewage wwtp",
 "power-generation": "power plant power station utility",
 "pharmaceutical": "pharma",
 "steel": "steel mill",
 "bio-energy": "bioenergy biofuel",
}
PUMP_TYPE_WORDS = {
 "ANSI centrifugal process pumps": "ansi end suction centrifugal chemical process pump",
 "Split case and vertical turbine pumps": "double suction horizontal split case vertical turbine vtp water municipal",
 "Magnetic drive (sealless) pumps": "mag drive mag-drive magdrive sealless seal-less lined etfe pfa",
 "Air-operated and electric diaphragm pumps": "aodd air operated double diaphragm eodd electric diaphragm pneumatic",
 "Gear pumps": "gear positive displacement metering",
 "High-pressure reciprocating pumps": "plunger piston triplex high pressure positive displacement",
 "Submersible and self-priming pumps": "submersible sump dewatering self priming trash pump",
 "Peristaltic pumps": "hose pump tube",
 "Mixers and agitators": "mixer agitator tank mixing top entry side entry",
}
# Territories: the names buyers type. Manufacturers match on state names only, so a city or an abbreviation finds the location pages first.
STATE_NAMES = {"ar": "arkansas", "md": "maryland dc delaware", "va": "virginia north south carolina carolinas"}
PLACES = {"ar": "arkansas ar el dorado", "md": "maryland md dc washington delaware de millersville baltimore annapolis",
          "va": "virginia va north carolina nc south carolina sc carolinas"}

def _plain(x):
    """Text out of the content structures: strings, lists and tuples, with [[path|text]] links reduced to their text."""
    if isinstance(x, str): return re.sub(r"\[\[[^|\]]*\|([^\]]+)\]\]", r"\1", re.sub(r"<[^>]+>", " ", x))
    return " ".join(_plain(i) for i in x)

def _words(*parts):
    """Lower-case, de-duplicated words, in first-seen order."""
    seen = []
    for w in re.sub(r"[^a-z0-9]+", " ", " ".join(parts).lower().replace("&", " and ")).split():
        if w not in seen and len(w) > 1: seen.append(w)
    return seen

def _cap(s): return s[0].upper() + s[1:]

def build_index(B, GUIDES, SERVICES, INDUSTRIES, CATS, CAT_COPY, TERR, LOC, PUMP_TYPES, terr_tag, st_members, phone):
    """Each entry: t title, k kind, u address, s the line shown under the title,
    h words that say what the page is for (matched strongly), w words from the body of the page (matched weakly)."""
    E = []
    def add(title, kind, path, sub, strong, weak="", browse=True):
        seen = set(_words(title))
        h = [w for w in _words(strong) if w not in seen]; seen |= set(h) | set(_words(sub))
        E.append(dict(t=title, k=kind, u=path, s=sub, h=" ".join(h), w=" ".join(w for w in _words(weak) if w not in seen), browse=browse))

    for g in GUIDES:
        sub = g["h1"].split(": ", 1)[1] if g["h1"].startswith(g["nav"] + ": ") else g["h1"]
        add(g["nav"], "Problem guide", f"problems/{g['slug']}/", _cap(sub), g["query"] + " " + SAID_AS.get(g["slug"], ""),
            " ".join([g["short"], _plain(g["table"][2]), " ".join(h for h, _ in g["sections"]), " ".join(q for q, _ in g["faq"])]))

    for b in sorted(B.values(), key=lambda x: x["name"].lower()):
        add(b["name"], "Manufacturer", f"manufacturers/{b['slug']}/", f"{_cap(b['noun'])} · {terr_tag(b['terr'])}",
            " ".join([b["noun"], " ".join(b["items"]), SAID_AS.get(b["slug"], "")]), " ".join([b["line"], CATS[b["cat"]][1], " ".join(STATE_NAMES[t] for t in b["terr"])]))

    for c, (cslug, cname, cnav) in CATS.items():
        add(cnav, "Product", f"products/{cslug}/", CAT_COPY[c][1], cname + " supplier distributor", " ".join(b["name"] for b in B.values() if b["cat"] == c))
    PT = {p["pt"]: p for p in PUMP_PAGES}
    for pt, slugs in PUMP_TYPES:
        p = PT.get(pt)
        if p:
            add(p["nav"], "Pump type", f"products/pumps/{p['slug']}/", "From " + ", ".join(B[s]["name"] for s in slugs),
                " ".join([pt, p["query"].replace("/", " "), PUMP_TYPE_WORDS.get(pt, "")]), _plain([p["how"], p["good"], [q for q, _ in p["faq"]]]))
        else:
            add(pt, "Pump type", "products/pumps/", "From " + ", ".join(B[s]["name"] for s in slugs), PUMP_TYPE_WORDS.get(pt, ""), browse=False)

    for s in SERVICES:
        add(s["nav"], "Service", f"services/{s['slug']}/", s["lede"], " ".join([s["h1"], SAID_AS.get(s["slug"], "")]),
            " ".join([s["query"], " ".join(h for h, _ in s["sections"]), " ".join(_plain(bl) for _, bl in s["sections"]), " ".join(q for q, _ in s["faq"])]))

    for i in INDUSTRIES:
        add(i["name"], "Industry", f"industries/{i['slug']}/", i["h1"], "industry plants " + SAID_AS.get(i["slug"], ""), _plain(i["supply"]))

    for t, (slug, tname, tlong) in TERR.items():
        L = LOC[t]; here = PLACES[t] + " " + tlong
        add(tname, "Location", f"locations/{slug}/", f"{L['office']}{', ' + L['addr'][1].split(',')[0] if L['pa'] else ''} · {L['phone']}",
            here + " office address location", "near me distributor supplier pumps seals valves repair")
        add(f"Pump repair in {tname}", "Location", f"locations/{slug}/pump-repair/", f"Repair with the cause of failure written down. Call {L['phone']}.",
            here + " repair shop rebuild overhaul", "mechanical seal repair field service near me")
        for c in CATS:
            ms = st_members(t, c)
            if ms: add(f"{CATS[c][2]} in {tname}", "Location", f"locations/{slug}/{CATS[c][0]}/", ", ".join(x["name"] for x in ms), here + " distributor supplier " + CATS[c][1])

    add(f"Equipment down? Call {phone}", "Call", "tel:+1" + re.sub(r"\D", "", phone), "Or send the details and mark the request \u201cEquipment is down\u201d.", "pump emergency urgent breakdown broken stopped failed asap rush", browse=False)
    add("Request a quote", "Page", "contact/", f"Six fields, or call {phone} if equipment is down.", "quote price pricing cost rfq lead time order buy purchase contact phone number email address offices")
    add("All manufacturers", "Page", "manufacturers/", "The full line card, A to Z, with the states where each is supplied.", "brands line card lines represented", browse=False)
    add("About Southern Design", "Page", "about/", "A product supplier and a reliability partner in one company.", "company history who we are sdm southern design and mechanical", browse=False)
    add("Customer portal login", "Page", "http://rms.mysoutherndesign.com/client", "Sign in to the Reliability Management System.", "log in sign in rms account client", browse=False)
    return E
