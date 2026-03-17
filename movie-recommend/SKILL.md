---
name: movie-recommend
description: Recommend movies, TV shows, or documentaries to the user based on their personal watch history and ratings from Kinorium. Use when the user asks for film or series recommendations, or says "what to watch", "посоветуй фильм", "что посмотреть", etc. Always include a link to Kinorium (ru.kinorium.com) for every recommended title.
---

# Movie Recommendation Skill

## User's Watch History

The file `references/watched.csv` contains the user's full Kinorium export (UTF-8, tab-separated, ~1800 titles).

Columns: `My rating`, `backup_id`, `Date`, `Title`, `Original Title`, `Type`, `Year`, `Genres`, `Countries`, `Runtime`, `Age limit`, `MPAA`, `Budget`, `Box USA`, `Box world`, `Box RU`, `Audience`, `Knrm rating`, `Knrm cnt`, `IMDb rating`, `IMDb cnt`, `World premier date`, `RU premier date`, `Digital premier date`, `Actors`, `Directors`, `Note`

To find what the user has already seen, search this file before recommending. Never recommend titles already in the file.

## Workflow

1. Read `references/watched.csv` to understand taste profile (focus on ratings 9–10)
2. Identify patterns: genres, directors, countries, eras, themes the user loves
3. Generate recommendations **not present** in the CSV
4. For each recommendation, include all three links (see below)

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
- Always verify: is the title already in watched.csv? If yes — skip it.
- Prefer titles with strong critical consensus (IMDb 7.5+) unless recommending niche/arthouse.
