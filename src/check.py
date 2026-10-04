import os, re, json, sys
root = os.path.abspath("../site"); bad = []; n = 0; h1bad = []; titles = {}; hidden = 0; pages = 0
# addresses served by a rule in _redirects rather than by a file
ruled = {l.split()[0] for l in open(os.path.join(root, "_redirects")) if l.strip() and not l.startswith("#")}
ruled_prefix = tuple(r.split(":")[0] for r in ruled if ":" in r)  # rules with a placeholder cover everything under their prefix
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".html"): continue
        p = os.path.join(dp, f); s = open(p).read()
        for h in re.findall(r'(?:href|src)="([^"#?]+)[^"]*"', s):
            if re.match(r"(https?:|mailto:|tel:)", h): continue
            n += 1
            target = os.path.normpath(os.path.join(dp, h))
            if not os.path.exists(target) and "/" + os.path.relpath(target, root) not in ruled and not ("/" + os.path.relpath(target, root)).startswith(ruled_prefix): bad.append((os.path.relpath(p, root), h))
        for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(j)
        if len(re.findall(r"<h1[ >]", s)) != 1: h1bad.append(os.path.relpath(p, root))
        t = re.search(r"<title>(.*?)</title>", s).group(1); titles.setdefault(t, []).append(os.path.relpath(p, root))
        assert "[[" not in s, p
        if "contact/thanks" in p: continue  # always noindex, in both modes
        pages += 1; hidden += '<meta name="robots" content="noindex' in s
blocked = "Disallow: /" in open(os.path.join(root, "robots.txt")).read()
assert hidden in (0, pages) and blocked == (hidden == pages), "mixed preview/live build: rebuild"
print("mode:", "PREVIEW, hidden from search engines" if blocked else "LIVE, open to search engines", f"({hidden}/{pages} pages noindex)")
print("internal links checked:", n, "broken:", bad[:10])
print("pages without exactly one h1:", h1bad)
print("duplicate titles:", {k: v for k, v in titles.items() if len(v) > 1})
