# movie-recommend

A [Hermes Agent](https://hermes-agent.nousresearch.com) skill that recommends movies, TV shows, and documentaries based on your personal watch history exported from [Kinorium.com](https://ru.kinorium.com).

## How it works

The skill reads your personal ratings from a CSV export (`references/watched.csv`) and:
1. Analyses your taste profile (genres, directors, themes rated 9–10)
2. Checks every candidate against your watch history to avoid repeats
3. Verifies real IMDb ratings via web search (not LLM memory)
4. Provides a Kinorium link for every recommendation

## Setup

### 1. Export your data from Kinorium

Go to your Kinorium profile → Settings → **Export data**. You'll receive an email from `robot@kinorium.com` with CSV attachments.

### 2. Install the skill

```bash
hermes skills install https://github.com/sg-shag/skill-movie-recommend
```

### 3. Place your CSV exports

Download the attachments from the Kinorium email to `~/Downloads/`, then run the install script:

```bash
cd ~/.hermes/skills/movie-recommend
python3 scripts/install_kinorium_exports.py
```

This converts the exports from UTF-16 to UTF-8 and places them in `references/`.

### 4. Verify

```bash
cat references/kinorium_date.txt
# Should show today's date
```

## Auto-refresh

The skill checks for a newer Kinorium email automatically before each recommendation. If found, it downloads and installs the fresh exports.

## Usage

Just ask naturally:
- «Посоветуй фильм»
- «Что посмотреть сегодня вечером?»
- «Recommend me something like Сталкер»

## Files

- `SKILL.md` — Hermes skill definition
- `scripts/check_watched.py` — verify a film against your watch history
- `scripts/install_kinorium_exports.py` — install CSV exports from ~/Downloads/
- `references/light-tone-criteria.md` — criteria for "light/warm" recommendations
- `references/watched.csv`, `watchlist.csv`, `kinorium_date.txt` — personal runtime data, not tracked in git

## Pitfalls

- **Don't hardcode film titles in LLM prompts** — the model generates encoding garbage for Russian text. Use `check_watched.py` via terminal with English titles.
- **Don't state ratings from memory** — always fetch real IMDb rating via web search. LLMs hallucinate ratings.
- **Always verify candidates programmatically** — 1800+ watched titles make "new" recommendations likely already seen.

---

## 🚧 Roadmap: live data from Kinorium

Currently the skill works only with manually exported CSV snapshots. Two paths to make it live:

### Option A — Kinorium Insider API

Kinorium has an internal API documented at `https://en.kinorium.com/insider/api/` — but access appears restricted to partners. If a public API key becomes available, the skill can fetch ratings on demand.

### Option B — Public profile scraping

The public profile URL `https://ru.kinorium.com/user/USERID/ratings/` is protected by JS anti-bot challenges. A headless browser (Playwright/Puppeteer) with a session cookie could bypass this.

### Contributions welcome

If you have Kinorium API access or a working scraping approach, PRs are welcome.

## License

MIT
