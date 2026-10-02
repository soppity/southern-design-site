# Southern Design website concept

A redesign concept for [southerndesign.com](https://www.southerndesign.com/), prepared by Lucid. It is not the live Southern Design website, and every page carries a ribbon saying so.

## What is here

| Path | What it is |
|---|---|
| `site/` | The built site: 70 static HTML pages, ready to host. Open `site/index.html` to browse it locally. |
| `site/seo-page-map.csv` | Every page with its target search, title and description. |
| `site/sitemap.xml`, `site/robots.txt`, `site/_redirects`, `site/_headers` | Sitemap, crawler rules, redirects from the five old Wix addresses, and the preview's do-not-index header. |
| `src/` | The generator that builds `site/`. |

## Changing the site

Edit the content, then rebuild. Do not edit files in `site/` by hand; the next build overwrites them.

| To change | Edit |
|---|---|
| Manufacturers and the states each is supplied in | `src/brands.py` |
| Problem guides | `src/guides.py` |
| Service and industry pages | `src/content2.py` |
| Header photos on inner pages | `src/photos.py` |
| Manufacturer logos (one file per manufacturer, named by its page slug) | `src/logos/` |
| Home page layout and base styles | `src/home-template.html` |
| Inner-page styles | `src/extra.css` |
| Page templates, titles, structured data | `src/build.py` |

```
cd src
python3 build.py           # rebuilds ../site as a preview, hidden from search engines
python3 build.py --live    # rebuilds ../site for launch, open to search engines
python3 check.py           # checks links, headings and structured data, and reports the mode
```

Python 3 only, no packages to install.

## Preview and live builds

The site carries Southern Design's name and logo, so it is built as a **preview** by default and the copy in this repo is a preview. A preview build:

- adds a `noindex, nofollow` tag to every page,
- sets `robots.txt` to disallow all crawlers, including AI crawlers,
- writes a `_headers` file that sends the same instruction as an HTTP header on Netlify and Cloudflare Pages.

This keeps a preview out of search results. It does not stop someone with the link from opening it; use the host's password protection for that.

Build with `--live` only once Southern Design has approved the site. That removes all three and restores the launch `robots.txt` with the sitemap.

## Hosting

Publish the `site/` folder. `_redirects` and `_headers` are in Netlify / Cloudflare Pages format.

## Still needed before it goes live

- An engineer at Southern Design to review the eight problem guides, and a named reviewer on each.
- Confirmation of their status with each manufacturer. Pages say "supplier", not "authorized distributor".
- A check of the Virginia and Carolinas line list against their own line sheet.
- Real case studies and the people for the About page (placeholders are marked).
- Their own photos. The current ones are free-licence stock from Unsplash, loaded by link.
- Manufacturer logos checked against each manufacturer's brand guidelines. The current files were taken from Southern Design's own 2024 line sheets. Flex-A-Seal, MRI and Lotus have no logo on those sheets, so their pages have none.
- A real enquiry form. The current one does not send anything.
