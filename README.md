# movie-recommend

An [OpenClaw](https://github.com/openclaw/openclaw) skill that recommends movies, TV shows, and documentaries based on your personal watch history exported from [Kinorium.com](https://ru.kinorium.com).

## How it works

The skill reads your personal ratings from a CSV export (`references/watched.csv`) and uses them to:
- Understand your taste profile (genres, directors, themes you love)
- Avoid recommending titles you've already seen
- Find new titles that match your preferences
- Provide a Kinorium link for every recommendation

## Setup

1. Export your data from Kinorium:
   - Go to your Kinorium profile → Settings → **Export data**
   - Download `backup_USERID_votes.csv`

2. Replace the sample file with your export (rename to `watched.csv`, convert from UTF-16 to UTF-8):
   ```
   movie-recommend/references/watched.csv
   ```

3. Package and install the skill in OpenClaw:
   ```
   openclaw skills install ./movie-recommend.skill
   ```

## Input format

Tab-separated CSV exported from Kinorium. Columns:
`My rating`, `backup_id`, `Date`, `Title`, `Original Title`, `Type`, `Year`, `Genres`, `Countries`, `Runtime`, `Age limit`, `MPAA`, `Budget`, `Box USA`, `Box world`, `Box RU`, `Audience`, `Knrm rating`, `Knrm cnt`, `IMDb rating`, `IMDb cnt`, `World premier date`, `RU premier date`, `Digital premier date`, `Actors`, `Directors`, `Note`

## Usage

Just ask naturally:
- "Посоветуй фильм"
- "Что посмотреть сегодня вечером?"
- "Recommend me something like Левиафан"

---

## 🚧 Roadmap: live data from Kinorium

Currently the skill works only with a manually exported CSV snapshot. There are two paths to make it live:

### Option A — Kinorium Insider API

Kinorium has an internal API documented at `https://en.kinorium.com/insider/api/` — but access appears to be restricted to partners or registered developers. If a public API key becomes available, the skill can be extended to fetch ratings on demand without manual export.

**What's needed:** Kinorium API token + endpoint for user ratings.

### Option B — Public profile scraping

The public profile URL `https://ru.kinorium.com/user/USERID/ratings/` exists but is protected by JS anti-bot challenges (cookie/fingerprint verification). Standard HTTP fetching fails.

**What's needed:** A headless browser solution (Playwright/Puppeteer) or a Kinorium session cookie to bypass the JS challenge and fetch ratings without export.

### Contributions welcome

If you have access to the Kinorium API or a working scraping approach, PRs are welcome.

## License

MIT
