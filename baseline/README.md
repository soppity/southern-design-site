# Baseline: where Southern Design stood before the new site

Taken on 4 October 2026, while the Wix site was live at southerndesign.com and the new site was only a preview. Re-run the same checks after launch and compare.

## What it shows

| Measure | Result on 4 October 2026 |
|---|---|
| Searches for the company by name (3) | First result in all 3 |
| Searches for what they sell and fix (66) | On page 1 for 0 of 66 |
| Named anywhere on those 66 result pages | 1 of 66, and only inside another site's listing (the Ebara search) |
| Perplexity, 3 "who does this near me" questions | Not named or cited in any, including "pump distributor in El Dorado Arkansas" |
| Current site speed score, mobile | 67 of 100, main content visible after 8.8 seconds |
| Current site speed score, desktop | 91 of 100 |
| New site speed score, same day | 97 mobile, 100 desktop (home page, after the speed work); inner pages 100 |
| Real-visitor speed data from Chrome | None: Google has too few visits on record to report any |

The 66 searches are 8 pump problems, 13 local supplier and repair searches, 6 services, 7 industries and 32 manufacturer lines. The sites that came up most often in the top three for local and service searches were cummins-wagner.com (6 of 19), tencarva.com (5), cbeuptime.com (3) and carotek.com (3).

## Files

| File | What it holds |
|---|---|
| `queries.csv` | The 69 searches and the page on the new site meant to answer each |
| `2026-10-04/search-positions.csv` | For each search: Southern Design's position on page 1 of Google, the top three sites, and whether Southern Design is named anywhere on the page |
| `2026-10-04/speed.csv` | PageSpeed Insights scores for the Wix home page and the new home page, mobile and desktop |
| `2026-10-04/ai-answers.csv` | Three questions asked of Perplexity and who it named |
| `2026-10-04/ranking-pages.csv` | The top three results for the 19 local and service searches: which page ranks and its title |
| `competitors.md` | Who ranks instead of Southern Design, why, and what the new site still lacks |
| `actions-for-southern-design.md` | What only Southern Design can do: addresses, Google listing, manufacturer and directory listings, material for the site |
| `2026-10-04/distributor-listings.csv` | Each manufacturer's distributor page and whether it lists Southern Design |

## How it was measured, and the limits

- **Search positions.** Google, United States results in English (`gl=us&hl=en&pws=0`), first page only, read from a UK connection. Google would not let the location be set to a town, so searches carry the state or city in the wording. Positions count ordinary results; map listings and adverts are not counted, but the "named anywhere" column covers the whole page including those. Results from an Arkansas or Maryland connection may differ by a place or two.
- **AI Overview column.** Records whether Google's AI Overview marker was in the page (68 of 69). It was confirmed on screen for seven searches and read from the page source for the rest, so treat the count as approximate. The firmer finding is the "named anywhere" column.
- **Speed.** One PageSpeed Insights run per page. Scores move a few points between runs. The new site's SEO score of 69 is because the preview is deliberately hidden from search engines; that goes when it launches.
- **AI assistants.** Only three Perplexity questions were asked, signed out, with no account. ChatGPT was not checked. This is a spot check, not a survey.
- **Not measured.** Visits, enquiries and calls on the current site. Those need the Analytics tag on the Wix site or access to their Search Console.

## Running it again

1. Search positions: run each line of `queries.csv` through Google with `gl=us&hl=en&pws=0` and record the same columns in a new dated folder. Leave several seconds between searches or Google starts returning empty pages.
2. Speed: test both home pages at pagespeed.web.dev.
3. AI answers: ask the same three questions.
