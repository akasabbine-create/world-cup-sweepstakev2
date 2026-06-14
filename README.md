# World Cup Sweepstake

A GitHub Pages dashboard with a scheduled GitHub Actions updater.

## Setup

1. Upload these files to the root of a GitHub repository.
2. Edit `data/players.json` with your real players and teams.
3. Add a repository secret called `RAPIDAPI_KEY` in Settings > Secrets and variables > Actions.
4. Optional: add repository variables `API_FOOTBALL_LEAGUE_ID` and `API_FOOTBALL_SEASON` if your API provider uses different World Cup IDs.
5. Run the workflow manually from Actions.
6. Enable GitHub Pages from Settings > Pages, using the `main` branch and `/root` folder.

## Important

The default API endpoint assumes API-Football on RapidAPI using `league=1&season=2026`. If your API returns no matches, the league ID needs changing.
