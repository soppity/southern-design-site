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

## Tracking

The site sends data to the Google Analytics property "Southern Design website" (account "Southern Design", under patrick@wearelucid.uk). The measurement ID is in `src/tracking.py`; clear it to build with no analytics. Advertising signals are switched off, and nothing a visitor types (name, email, phone) is sent.

| Event | Fires when | Counts as a lead |
|---|---|---|
| `generate_lead` | The thank-you page `contact/thanks/` loads after a real form submission | Yes |
| `phone_call_click` | Someone clicks or taps any phone number | Yes |
| `email_click` | Someone clicks the email address | No |
| `quote_cta_click` | Someone clicks a "Request a quote" style button | No |
| `form_start` | Someone starts filling in the enquiry form | No |
| `portal_click` | An existing customer clicks through to the portal | No |
| `form_demo_submit` | The concept form is submitted (it sends nothing) | No |

Each event records where on the page it happened, and every page reports its type (guide, manufacturer, service and so on) as the content group.

The first place a visitor came from (source, medium, campaign, landing page) is stored in their browser and added to the enquiry form as hidden fields, so each lead can carry its source into the CRM.

Already set up in the Analytics property:

- `generate_lead` and `phone_call_click` are marked as key events, counted once per event, with no default money value.
- Five custom dimensions, so leads and clicks can be broken down in reports: Link location, Enquiry need, Enquiry state, First source, First landing page.
- Event data is kept for 14 months (the default is 2).
- Optional data sharing with Google is off.

The tag works on any address the site is served from, so it is already recording visits to the Netlify preview. Nothing needs changing when the real domain is pointed at the site. In reports, filter on the built-in Hostname dimension (or by date from launch day) to separate preview visits from real ones. One test lead with the source `lucid_test` was sent on 4 October 2026 to check the setup.

To finish before launch:

- Point the real enquiry form (a GoHighLevel embed is the plan) at `contact/thanks/` as its redirect after submission. Until then no form leads are counted.
- Phone clicks show intent, not completed calls. To count and record actual calls, put a call-tracking number that forwards to 877-917-8677 on the site: change `PHONE` and `TEL` at the top of `src/build.py`.
- Add a privacy policy page that mentions Google Analytics.
- For a before-and-after comparison, the same measurement ID needs adding to the current Wix site (Wix has a Google Analytics field under Marketing Integrations). That needs Southern Design's Wix login.
- Google Search Console can only be set up once there is access to the domain (a DNS record) or to the Wix site. After that, submit `sitemap.xml` and link Search Console to the Analytics property.

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
