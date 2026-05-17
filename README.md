# movie-recommend

A [Hermes Agent](https://hermes-agent.nousresearch.com) skill that recommends movies, TV shows, and documentaries based on your personal watch history exported from [Kinorium.com](https://ru.kinorium.com).

## How it works

The skill reads your personal ratings from a CSV export (`references/watched.csv`) and uses them to:
- Understand your taste profile (genres, directors, themes you love)
- Avoid recommending titles you've already seen
- Find new titles that match your preferences
- Provide a Kinorium link for every recommendation

## Setup

1. Export your data from Kinorium:
   - Go to your Kinorium profile → Settings → **Export data**
   - You will receive an email from `robot@kinorium.com` with CSV attachments

2. Download the attachments to `~/Downloads/`, then convert and install (files arrive as UTF-16 LE with BOM):
   ```python
   import os, glob
   dest = os.path.expanduser('~/.hermes/skills/movie-recommend/references/')
   for pattern, dst in [('backup_*_votes.csv', 'watched.csv'), ('backup_*_movie_list.csv', 'watchlist.csv')]:
       matches = glob.glob(os.path.expanduser(f'~/Downloads/{pattern}'))
       if matches:
           text = open(matches[0], 'rb').read().decode('utf-16')
           open(dest + dst, 'w', encoding='utf-8').write(text)
           print(f'Written: {dst}')
   ```

3. Install the skill:
   ```bash
   hermes skills install https://github.com/sg-shag/skill-movie-recommend
   ```

## Usage

Just ask naturally:
- «Посоветуй фильм»
- «Что посмотреть сегодня вечером?»
- «Recommend me something like Левиафан»

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
