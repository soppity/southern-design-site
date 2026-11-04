# Southern Design website concept

A redesign concept for [southerndesign.com](https://www.southerndesign.com/), prepared by Lucid. It is not the live Southern Design website, and every page carries a ribbon saying so.

## What is here

| Path | What it is |
|---|---|
| `site/` | The built site: 100 static HTML pages plus a thank-you page, ready to host. Open `site/index.html` to browse it locally. |
| `site/seo-page-map.csv` | Every page with its target search, title and description. |
| `site/sitemap.xml`, `site/robots.txt`, `site/_redirects`, `site/_headers` | Sitemap, crawler rules, redirects from the five old Wix addresses, and the preview's do-not-index header. |
| `src/` | The generator that builds `site/`. |
| `baseline/` | Where Southern Design stood in search, AI answers and site speed before the new site, for a before-and-after comparison. See `baseline/README.md`. |

## Changing the site

Edit the content, then rebuild. Do not edit files in `site/` by hand; the next build overwrites them.

| To change | Edit |
|---|---|
| Manufacturers and the states each is supplied in | `src/brands.py` |
| Problem guides | `src/guides.py` |
| Service and industry pages | `src/content2.py` |
| Header photos on inner pages | `src/photos.py` |
| Words the search box matches (symptoms, other spellings of a brand) | `src/search.py` |
| Pump-type pages (one per pump type, chosen from keyword research) | `src/pumptypes.py` |
| Keyword research behind the page titles and new pages | `baseline/2026-11-04/openseo-keywords.md` |
| Manufacturer logos (one file per manufacturer, named by its page slug) | `src/logos/` |
| Home page layout, base styles and the colour palette (the `:root` block) | `src/home-template.html` |
| Inner-page styles | `src/extra.css` |
| Page templates, titles, structured data | `src/build.py` |

```
cd src
python3 build.py           # rebuilds ../site as a preview, hidden from search engines
python3 build.py --live    # rebuilds ../site for launch, open to search engines
python3 check.py           # checks links, headings, structured data and the search index, and reports the mode
```

Python 3 only, no packages to install.

## Preview and live builds

The site carries Southern Design's name and logo, so it is built as a **preview** by default and the copy in this repo is a preview. A preview build:

- adds a `noindex, nofollow` tag to every page,
- sets `robots.txt` to disallow all crawlers, including AI crawlers,
- writes a `_headers` file that sends the same instruction as an HTTP header on Netlify and Cloudflare Pages.

This keeps a preview out of search results. It does not stop someone with the link from opening it; use the host's password protection for that.

Build with `--live` only once Southern Design has approved the site. That removes all three and restores the launch `robots.txt` with the sitemap.

## State pages

Buyers search by state, and Southern Design's lines differ by state, so each of the three territories has its own set of pages under `locations/`:

- an overview (`locations/arkansas/`),
- one page per product type that territory carries (`locations/arkansas/pumps/`, `.../mechanical-seals/` and so on), listing only the manufacturers on that territory's line card,
- a pump repair page (`locations/arkansas/pump-repair/`).

They are generated from `src/brands.py`, so changing which territories a manufacturer is supplied in updates them. The repair pages each carry a marked gap for detail only Southern Design can give.

## Search

Every page has a search box: a magnifier in the header, and a box in the home page header area. A visitor types a symptom ("seal leaking"), a manufacturer ("Ebara") or a product ("gear pump") and gets the matching pages as they type. It tolerates a typo, plurals, and words typed in any order.

- **What it searches.** A small index built with the site (`site/assets/search.json`, under 100 entries): the ten guides, 32 manufacturers, nine pump-type pages, services, industries and every location page. It is written by `src/search.py` from the same content as the pages, so it never goes out of date.
- **Words buyers use.** `SAID_AS` in `src/search.py` lists words people type that a page may not use: symptoms ("noisy", "banging"), abbreviations ("AODD", "VFD"), and other spellings of a brand ("claval", "FTI"). Add a word only where the page really answers it.
- **Nothing found.** The box offers to send the search to Southern Design: the link opens the enquiry form with the search already in the make, model or part number field. Every result list ends with the same offer. Part numbers and models the site has no page for become enquiries this way.
- **Breakdowns.** Searches such as "pump down" or "emergency" show the phone number first.
- **The search page** (`search/`) lists everything by type. It is also where the search box sends a visitor whose browser has JavaScript switched off.
- **Where it runs.** In the visitor's browser. There is no search server or outside service, so it works on any host and costs nothing.

## Colour palette

The logo is Southern Design's own and is unchanged: red and white. The site uses the "Graphite and red" palette: neutral graphite for dark areas, white pages with cool grey panels, and the logo's red as the one accent (buttons, links, the call strip at the top).

The colours are set once, as named values in the `:root` block of `src/home-template.html`, and every page follows them. The earlier options (a blue-black and bronze palette, a warm ivory one, and the grey and gold taken from the Wix site) are in the Git history.

## Speed

On 4 October 2026 the home page scored 97 (mobile) and 100 (desktop) for performance on PageSpeed Insights, with 100 for accessibility and best practices. A guide page, a manufacturer page and a state page each scored 100 on both. What keeps it there:

- The font is a cut-down copy of Open Sans served from the site (`src/fonts/`), not from Google Fonts. It covers English text and common punctuation; other characters fall back to the system font.
- The stylesheet is written into every page, so there is no separate file to wait for.
- Google's Analytics script loads three seconds after the page has finished, or at the visitor's first tap, key press or scroll. Events are queued from the start, so the only visits missed are ones that end within a few seconds of arriving without a tap or scroll. The thank-you page loads the script at once, so a lead is never missed.
- Header photos are requested straight from the HTML. On phones, header photos come through the site's own address using a pass-through rule in `_redirects`, which only works on Netlify. On another host, replace the `img/` addresses with real files.
- Fonts, the script and logos are cached for a long time (`_headers`).
- The search index is only fetched when someone first uses a search box, so it adds nothing to the first load.

The SEO score reads 69 on the preview because the preview is deliberately hidden from search engines. That is the only failing check, and it goes with a `--live` build.

Netlify adds a "Powered by Netlify" badge to free-plan sites. It is a small extra script on every page. It can be switched off under Project configuration > General in Netlify.

## Tracking

The site sends data to the Google Analytics property "Southern Design website" (account "Southern Design", under patrick@wearelucid.uk). The measurement ID is in `src/tracking.py`; clear it to build with no analytics. Advertising signals are switched off, and nothing a visitor types into the enquiry form (name, email, phone) is sent. Search terms are sent, except any that look like an email address or a phone number.

| Event | Fires when | Counts as a lead |
|---|---|---|
| `generate_lead` | The thank-you page `contact/thanks/` loads after a real form submission | Yes |
| `phone_call_click` | Someone clicks or taps any phone number | Yes |
| `email_click` | Someone clicks the email address | No |
| `quote_cta_click` | Someone clicks a "Request a quote" style button | No |
| `form_start` | Someone starts filling in the enquiry form | No |
| `portal_click` | An existing customer clicks through to the portal | No |
| `form_error` | The enquiry form could not be sent | No |
| `search` | Someone searches the site and pauses, picks a result or presses Enter. Carries the search term | No |
| `search_no_results` | A search finds nothing. Carries the search term | No |
| `search_result_click` | Someone picks a search result. Carries the term and the result chosen | No |

Each event records where on the page it happened, and every page reports its type (guide, manufacturer, service and so on) as the content group.

The search events show what buyers are looking for in their own words. `search_no_results` is the list of things they wanted that the site has no page for: models, part numbers, brands not carried. In Analytics, the term is in the built-in "Search term" dimension. A phone number or "Ask us" link clicked inside the search results counts as `phone_call_click` or `quote_cta_click` with the location `search`.

The first place a visitor came from (source, medium, campaign, landing page) is stored in their browser and added to the enquiry form as hidden fields, so each lead can carry its source into the CRM.

Already set up in the Analytics property:

- `generate_lead` and `phone_call_click` are marked as key events, counted once per event, with no default money value.
- Five custom dimensions, so leads and clicks can be broken down in reports: Link location, Enquiry need, Enquiry state, First source, First landing page.
- Event data is kept for 14 months (the default is 2).
- Optional data sharing with Google is off.
- Visits from ChatGPT, Perplexity and similar need no setup: the property's default channel group already has an "AI Assistant" channel.

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

- An engineer at Southern Design to review the nine problem guides, and a named reviewer on each.
- Confirmation of their status with each manufacturer. Pages say "supplier", not "authorized distributor".
- A check of the Virginia and Carolinas line list against their own line sheet.
- Real case studies and the people for the About page (placeholders are marked).
- Their own photos. The current ones are free-licence stock from Unsplash, loaded by link.
- Manufacturer logos checked against each manufacturer's brand guidelines. The current files were taken from Southern Design's own 2024 line sheets. Flex-A-Seal, MRI and Lotus have no logo on those sheets, so their pages have none. PMV has none either: its line sheet logo was Flowserve's, and Flowserve sold PMV in August 2026.
- A real enquiry form. The current one does not send anything.
