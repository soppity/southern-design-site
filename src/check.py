import os, re, json, sys
root = os.path.abspath("../site"); bad = []; n = 0; h1bad = []; titles = {}
for dp, dn, fn in os.walk(root):
    for f in fn:
        if not f.endswith(".html"): continue
        p = os.path.join(dp, f); s = open(p).read()
        for h in re.findall(r'(?:href|src)="([^"#?]+)[^"]*"', s):
            if re.match(r"(https?:|mailto:|tel:)", h): continue
            n += 1
            if not os.path.exists(os.path.normpath(os.path.join(dp, h))): bad.append((os.path.relpath(p, root), h))
        for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S): json.loads(j)
        if len(re.findall(r"<h1[ >]", s)) != 1: h1bad.append(os.path.relpath(p, root))
        t = re.search(r"<title>(.*?)</title>", s).group(1); titles.setdefault(t, []).append(os.path.relpath(p, root))
        assert "[[" not in s, p
print("internal links checked:", n, "broken:", bad[:10])
print("pages without exactly one h1:", h1bad)
print("duplicate titles:", {k: v for k, v in titles.items() if len(v) > 1})
