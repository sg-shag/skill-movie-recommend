---
name: movie-recommend
description: Recommend movies, TV shows, or documentaries based on the user's Kinorium watch history. Always verify candidates against watched.csv before presenting — the user has 1800+ watched titles, and unverified recommendations will often overlap. Always include a Kinorium search link for every recommended title.
triggers:
  - recommend movie
  - посоветуй фильм
  - посоветуй что посмотреть
  - порекомендуй фильм
---

# Movie Recommendation Skill

## Updating Data from Kinorium Email

Kinorium has no public API. It sends CSV exports by email on request.

## Pre-Recommendation Gate (Mandatory)

Before any recommendation turn, perform this gate in order. Do not skip it.

1. Read local snapshot date from `references/kinorium_date.txt`.
2. Check mailbox for the latest email from `robot@kinorium.com` with subject "Мои данные в Кинориуме".
3. Compare the email date to `kinorium_date.txt`.
4. If email date is newer, you must download attachments and run `python3 scripts/install_kinorium_exports.py` before generating any recommendation.
5. If email date is not newer, continue with current CSV files.

Never generate recommendations until this gate is resolved.

Hard block while gate is unresolved:
- Do not output any candidate titles.
- Do not output "temporary", "draft", or "while updating" recommendations.
- Do not output taste-profile-based suggestions before refresh and watched checks are complete.

Use these operational commands when the gate requires refresh:

1. Download newer CSV attachments from mailbox to `~/Downloads/`.
   Example with himalaya: `himalaya envelope list && himalaya attachment download <ID>`
2. Install the exports with the helper script:
```bash
python3 scripts/install_kinorium_exports.py
```

On success, the script updates `references/watched.csv`, `references/watchlist.csv`, and writes today's date to `references/kinorium_date.txt`.
If the refresh is incomplete, it exits with non-zero status and does not update `kinorium_date.txt`.

## Data Files

- `references/watched.csv` — full Kinorium votes export (UTF-8, tab-separated, ~1800+ titles)
- `references/watchlist.csv` — "Буду смотреть" list (titles user wants to watch)
- `references/kinorium_date.txt` — date of last export (YYYY-MM-DD)
- `references/light-tone-criteria.md` — tone criteria for "light/warm/positive" recommendations, derived from user's taste profile

## Filtering by Tone

When the user asks for "light", "warm", or positive cinema, load `references/light-tone-criteria.md` and apply its filters. Do NOT assume all well-rated films are light — the user's taste profile shows strong anti-correlation with war, crime, noir, and tragedy genres.

**watched.csv columns:** `My rating`, `backup_id`, `Date`, `Title`, `Original Title`, `Type`, `Year`, `Genres`, `Countries`, `Runtime`, `Age limit`, `MPAA`, `Budget`, `Box USA`, `Box world`, `Box RU`, `Audience`, `Knrm rating`, `Knrm cnt`, `IMDb rating`, `IMDb cnt`, `World premier date`, `RU premier date`, `Digital premier date`, `Actors`, `Directors`, `Note`

**watchlist.csv columns:** same as watched.csv plus `ListTitle`, `Status`

## Pitfalls

- **Email agnosticism:** himalaya is just one example. Never require it. Correct phrasing: "find the email from robot@kinorium.com in your email client".
- **Himalaya query syntax:** filters use spaces, NOT flags. `from <pattern>` (space, not `--from`), `and` / `or` to combine. Example: `himalaya envelope list "from robot@kinorium.com and subject Мои данные в Кинориуме"`. No `-n`/`--limit` flag — pipe through `head -N` to trim. The `--output` flag accepts only `plain` or `json`, NOT a filesystem path.
- **Mailbox check is mandatory:** do not skip mailbox-date comparison before recommendation. If a newer Kinorium email exists, download and refresh first.
- **No provisional recommendations:** while mailbox check/refresh is in progress, never output recommendations, candidate lists, or placeholders.
- **Python check — mandatory:** never give a recommendation without verifying via `scripts/check_watched.py` (or equivalent Python check). 1800+ watched titles make fake-new recommendations inevitable. Check both `Title` and `Original Title` columns — normalize: lowercase + strip quotes.
- **Path agnostic:** use `os.path.expanduser('~/.hermes/...')` everywhere.
- **watchlist.csv may not exist** — check `os.path.exists()` before reading.
- **One version rule:** local and public SKILL.md must always be identical.
- **Never hardcode candidate lists in execute_code:** when writing Python to verify candidates, do NOT embed film titles with Russian text directly in the code block. The model produces encoding garbage (Chinese characters, mixed scripts, Latin transcription errors). Instead:
  - Use the `check_watched.py` script via terminal (bash) with CLI arguments for each candidate
  - Or keep candidate names very short and purely in the original language (English titles only)
- **Verify IMDb/Kinorium rating on every candidate:** do NOT state a rating from memory. Use `web_search` to fetch the real IMDb or Kinorium rating for each candidate before including it in the recommendation. If a candidate has no verifiable rating, mark it as uncertain.
- **Verify film existence:** before recommending, check via web_search that the film actually exists with the stated year and director. Do not invent films or characteristics.

## Checking watched.csv — do it properly

**Always use Python to search, never eyeball or guess.** The CSV has 1800+ entries in Russian + original titles. A film can appear as:
- Russian title only (e.g. `Нелюбовь` with empty `Original Title`)
- Russian + original (e.g. `Охота` / `Jagten`)
- With different spelling or year variants

**Use the helper script instead of rewriting the check each time:**
```bash
python3 scripts/check_watched.py \
  "Охота|Jagten" \
  "Идеальные дни|Perfect Days"
```

The script prints JSON with `title_ru`, `title_orig`, and `watched` for each candidate. Filter out every candidate where `watched` is `true`.

If you need a non-default file, pass `--csv /path/to/watched.csv`.

Run this script for **every candidate** before including it in the recommendation. Filter out all watched titles before presenting results.

## Hindsight Memory

Tag everything with `movie-recommend`. Keep it minimal.

- **Recall (before recommending):** prior taste signals, rejection reasons ("too dark", "already tried"), past reactions. Use for ranking, not eligibility.
- **Retain (after answering):** one entry per recommendation turn — user's request context, what you recommended, why it matched.
- **Retain (reaction):** store user reactions as they come. Highest-value signal CSV doesn't contain.
- **Reflect (rarely):** only for "summarize my taste" or "based on everything I like, what should I watch?".

## Workflow

1. Read `references/kinorium_date.txt`
2. Check mailbox for latest Kinorium email from `robot@kinorium.com`
3. Compare mailbox email date with `kinorium_date.txt`
4. If mailbox date is newer, download attachments and run `python3 scripts/install_kinorium_exports.py`
5. Only after steps 1-4 are resolved, read `references/watched.csv` to understand taste profile (focus on ratings 9–10)
6. Check `references/watchlist.csv` — mention relevant watchlist titles **after** new recommendations, not before
7. Identify patterns: genres, directors, countries, eras, themes the user loves
8. Generate a shortlist of 5–8 candidate films that fit the taste profile
9. **For each candidate, verify via web_search:**
   - IMDb rating (real, not from memory)
   - Year of release
   - Director
   - Brief synopsis (confirm it matches the taste profile)
   - Mark as discard any candidate whose IMDb rating is more than 1.0 below stated (shows the film was hallucinated)
10. Run `scripts/check_watched.py` on every verified candidate
11. Present only candidates where the script returns `watched: false`
12. For each recommendation, include a valid Kinorium URL (see below)
13. After answering, call `hindsight_retain` once to store the recommendation turn
14. After the user reacts, call `hindsight_retain` again to store the reaction

## Required Link for Every Recommendation

Every recommended title **must** include a Kinorium search link:

`https://ru.kinorium.com/search/?q=TITLE+YEAR`

Replace `TITLE` with URL-encoded original title and `YEAR` with release year.

Use direct title URL only when the ID is verified and known to resolve:
`https://ru.kinorium.com/NNNNN/`

URL validity rules:
- Always include scheme: `https://`.
- Prefer the search URL format by default; it is more robust when ID is uncertain.
- Do not invent direct IDs.
- Do not output `/movie/<id>/` links unless you explicitly verified that route works for that title.

## Format

For each recommendation:

**«Русское название» / Original Title (Year, Country)**
One sentence why it fits this user's taste — reference specific films they rated highly.
Kinorium: [ссылка]

## Important

- Never invent films. If uncertain whether a title exists, search the web to verify before recommending.
- **Never state a rating from memory** — always fetch real IMDb/Kinorium rating via web_search for every candidate. The model hallucinates ratings.
- **Never hardcode Russian film titles in execute_code Python blocks** — the model produces encoding garbage. Use check_watched.py via terminal with English titles only, or verify via web_search.
- Before recommending, compare latest Kinorium email date with `references/kinorium_date.txt`; if email is newer, download and refresh first.
- Never output recommendations before mailbox check + refresh (if needed) + watched verification are complete.
- Always use tag `movie-recommend` for recommendation memory so recall and reaction history stay in one simple lane.
- Prefer titles with strong critical consensus (IMDb 7.5+) unless recommending niche/arthouse — but verify this rating, don't state it from memory.
