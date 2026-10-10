"""Calculate league standings from match results."""

from collections.abc import Iterable

from league.models import Match, TeamRecord


def create_team_record(team_name: str) -> TeamRecord:
    return TeamRecord(
        team=team_name,
        played=0,
        won=0,
        drawn=0,
        lost=0,
        goals_for=0,
        goals_against=0,
    )

def calculate_standings(matches: Iterable[Match]) -> list[TeamRecord]:
    records: dict[str, TeamRecord] = {}


    for match in matches:
 # Get the home team's record, creating one if it doesn't exist.
        home = records.setdefault(
            match.home_team, create_team_record(match.home_team)
        )
 # Get the away team's record, creating one if it doesn't exist.
        away = records.setdefault(
            match.away_team, 
            create_team_record(match.away_team)
        )

        home.played += 1
        away.played += 1
        home.goals_for += match.home_goals
        home.goals_against += match.away_goals
        away.goals_for += match.away_goals
        away.goals_against += match.home_goals

        if match.home_goals > match.away_goals:
            home.won += 1
            away.lost += 1
        elif match.home_goals < match.away_goals:
            away.won += 1
            home.lost += 1
        else:
            home.drawn += 1
            away.drawn += 1

    return sorted(
        records.values(),
        key=lambda record: (
            -record.points,
            -record.goal_average,
            -record.goals_for,
            record.team,
        ),
    )
