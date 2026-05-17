---
name: movie-recommend
description: Recommend movies, TV shows, or documentaries to the user based on their personal watch history and ratings from Kinorium. Use when the user asks for film or series recommendations, or says "what to watch", "посоветуй фильм", "что посмотреть", etc. Always include a link to Kinorium (ru.kinorium.com) for every recommended title.
---

# Movie Recommendation Skill

## Updating Data from Kinorium Email

Kinorium has no public API. It sends CSV exports by email on request.

**When user asks to refresh watched/watchlist data:**
1. Check date: `cat ~/.hermes/skills/movie-recommend/references/kinorium_date.txt`
2. Find the email via your configured email tool — look for subject containing "Кинориум" or "backup", sender `robot@kinorium.com`
3. Download attachments → saves to `~/Downloads/`
4. Convert (files are UTF-16 LE with BOM) and install:
```python
import codecs, os, glob
dest = os.path.expanduser('~/.hermes/skills/movie-recommend/references/')
mapping = [('backup_*_votes.csv', 'watched.csv'), ('backup_*_movie_list.csv', 'watchlist.csv')]
for pattern, dst in mapping:
    matches = glob.glob(os.path.expanduser(f'~/Downloads/{pattern}'))
    if not matches:
        print(f'Not found: {pattern}')
        continue
    text = open(matches[0], 'rb').read().decode('utf-16')
    open(dest + dst, 'w', encoding='utf-8').write(text)
    print(f'Written: {dst}')
```
5. Update date: `echo "$(date +%Y-%m-%d)" > ~/.hermes/skills/movie-recommend/references/kinorium_date.txt`

## Data Files

- `references/watched.csv` — full Kinorium votes export (UTF-8, tab-separated, ~1800+ titles)
- `references/watchlist.csv` — "Буду смотреть" list (titles user wants to watch)
- `references/kinorium_date.txt` — date of last export (YYYY-MM-DD)

**watched.csv columns:** `My rating`, `backup_id`, `Date`, `Title`, `Original Title`, `Type`, `Year`, `Genres`, `Countries`, `Runtime`, `Age limit`, `MPAA`, `Budget`, `Box USA`, `Box world`, `Box RU`, `Audience`, `Knrm rating`, `Knrm cnt`, `IMDb rating`, `IMDb cnt`, `World premier date`, `RU premier date`, `Digital premier date`, `Actors`, `Directors`, `Note`

**watchlist.csv columns:** same as watched.csv plus `ListTitle`, `Status`

## Pitfalls

- **Always run a Python check before recommending** — do not rely on memory or skimming the CSV. Load watched.csv, build a normalized set (lowercase, strip quotes), and check every candidate programmatically. Without this check, "new" recommendations are often already watched.
- **Search both `Title` and `Original Title` columns** — Russian and English names both appear. Normalize: lowercase + strip surrounding quotes.
- **Do not hardcode user paths** — use `os.path.expanduser('~/.hermes/...')` everywhere.
- **watchlist.csv may not exist** if the user hasn't set it up — handle gracefully with `os.path.exists()`.

## Checking watched.csv — do it properly

**Always use Python to search, never eyeball or guess.** The CSV has 1800+ entries in Russian + original titles. A film can appear as:
- Russian title only (e.g. `Нелюбовь` with empty `Original Title`)
- Russian + original (e.g. `Охота` / `Jagten`)
- With different spelling or year variants

**Correct check before recommending:**
```python
import csv, os

watched_path = os.path.expanduser('~/.hermes/skills/movie-recommend/references/watched.csv')
with open(watched_path, encoding='utf-8') as f:
    rows = list(csv.reader(f, delimiter='\t'))

watched_titles = set()
for r in rows[1:]:
    if len(r) > 3:
        watched_titles.add(r[3].strip('"').lower())  # Russian title
    if len(r) > 4:
        watched_titles.add(r[4].strip('"').lower())  # Original title
watched_titles.discard('')  # remove empty strings

def is_watched(title_ru=None, title_orig=None):
    if title_ru and title_ru.lower() in watched_titles:
        return True
    if title_orig and title_orig.lower() in watched_titles:
        return True
    return False
```

Run this check for **every candidate** before including it in the recommendation. Filter out all watched titles before presenting results.

## Workflow

1. Read `references/watched.csv` to understand taste profile (focus on ratings 9–10)
2. Check `references/watchlist.csv` — mention relevant watchlist titles **after** new recommendations, not before
3. Identify patterns: genres, directors, countries, eras, themes the user loves
4. Generate recommendations **not present** in watched.csv (verified with Python check above)
5. For each recommendation, include a Kinorium link (see below)

## Required Link for Every Recommendation

Every recommended title **must** include a Kinorium search link:

`https://ru.kinorium.com/search/?q=TITLE+YEAR`

Replace `TITLE` with URL-encoded original title and `YEAR` with release year.

Or use a direct URL if you know the Kinorium ID:
`https://ru.kinorium.com/NNNNN/`

## Format

For each recommendation:

**«Русское название» / Original Title (Year, Country)**
One sentence why it fits this user's taste — reference specific films they rated highly.
Kinorium: [ссылка]

## Important

- Never invent films. If uncertain whether a title exists, search the web to verify before recommending.
- Always verify: is the title already in watched.csv? If yes — skip it. Use Python, not memory.
- Prefer titles with strong critical consensus (IMDb 7.5+) unless recommending niche/arthouse.
