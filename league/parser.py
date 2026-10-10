"""Parse match results from lines of comma-separated text."""

from collections.abc import Iterable

from league.models import Match


class ParseError(ValueError):
    """Raised when a match result line is invalid."""


def parse_matches(lines: Iterable[str]) -> list[Match]:
    """Parse valid match result lines, skipping blank lines."""
    matches: list[Match] = []

    for line_number, line in enumerate(lines, start=1):
        fields = [field.strip() for field in line.split(",")]
        if not line.strip():
            continue

        def fail(reason: str) -> None:
            raise ParseError(f"Line {line_number}: {reason}: {line.rstrip()}" )

        if len(fields) != 4:
            fail("expected 4 fields")

        home_team, home_goals_text, away_team, away_goals_text = fields
        if not home_team or not away_team:
            fail("team name cannot be empty")

        try:
            home_goals = int(home_goals_text)
            away_goals = int(away_goals_text)
        except ValueError:
            fail("goals must be whole numbers")

        if home_goals < 0 or away_goals < 0:
            fail("goals cannot be negative")
        if home_team == away_team:
            fail("a team cannot play itself")

        matches.append(Match(home_team, home_goals, away_team, away_goals))

    return matches
