# Football League Standings

CLI app that reads match results (CSV) and prints a league table
using 1974/75 English First Division rules.
AI assistant used: OpenAI Codex CLI.

## Rules (do not change without asking)
- Win = 2 points, draw = 1, loss = 0
- Rank by: points, then goal average (GF/GA), then goals scored, then team name A-Z
- GA of 0 => goal average is infinite (no division by zero); such teams tie on this step
- Data scope: results of matchweek 10 only (Sat 28 Sep 1974), not a running total

## Conventions
- Python 3.10+, standard library only (pytest for tests)
- Small modules with one job each; type hints everywhere
- Invalid input raises a clear error that includes the line number
- Every behavior change needs a test
- Run tests with: `python -m pytest`

## Input:  home_team,home_goals,away_team,away_goals
## Output: position,team,played,won,drawn,lost,gf,ga,goal_average,points