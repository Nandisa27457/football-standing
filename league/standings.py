"""Calculate league standings from match results."""

from collections.abc import Iterable

from league.models import Match, TeamRecord


def calculate_standings(matches: Iterable[Match]) -> list[TeamRecord]:
    records: dict[str, TeamRecord] = {}

    for match in matches:
        home = records.setdefault(
            match.home_team, TeamRecord(match.home_team, 0, 0, 0, 0, 0, 0)
        )
        away = records.setdefault(
            match.away_team, TeamRecord(match.away_team, 0, 0, 0, 0, 0, 0)
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
