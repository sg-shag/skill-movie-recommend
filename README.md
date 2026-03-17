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

## License

MIT
