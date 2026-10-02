# Southern Design website concept

A redesign concept for [southerndesign.com](https://www.southerndesign.com/), prepared by Lucid. It is not the live Southern Design website, and every page carries a ribbon saying so.

## What is here

| Path | What it is |
|---|---|
| `site/` | The built site: 70 static HTML pages, ready to host. Open `site/index.html` to browse it locally. |
| `site/seo-page-map.csv` | Every page with its target search, title and description. |
| `site/sitemap.xml`, `site/robots.txt`, `site/_redirects` | Sitemap, crawler rules, and redirects from the five old Wix addresses. |
| `src/` | The generator that builds `site/`. |

## Changing the site

Edit the content, then rebuild. Do not edit files in `site/` by hand; the next build overwrites them.

| To change | Edit |
|---|---|
| Manufacturers and the states each is supplied in | `src/brands.py` |
| Problem guides | `src/guides.py` |
| Service and industry pages | `src/content2.py` |
| Home page layout and base styles | `src/home-template.html` |
| Inner-page styles | `src/extra.css` |
| Page templates, titles, structured data | `src/build.py` |

```
cd src
python3 build.py    # rebuilds ../site
python3 check.py    # checks links, headings and structured data
```

Python 3 only, no packages to install.

## Hosting

Publish the `site/` folder. `_redirects` is in Netlify / Cloudflare Pages format.

If this is deployed as a preview before Southern Design has approved it, hide it from search engines first. It carries their name and logo.

## Still needed before it goes live

- An engineer at Southern Design to review the eight problem guides, and a named reviewer on each.
- Confirmation of their status with each manufacturer. Pages say "supplier", not "authorized distributor".
- A check of the Virginia and Carolinas line list against their own line sheet.
- Real case studies and the people for the About page (placeholders are marked).
- Their own photos. The current ones are free-licence stock from Unsplash, loaded by link.
- A real enquiry form. The current one does not send anything.
