
from collections.abc import Iterable

from league.models import Match


class ParseError(ValueError):
    """Raised when a match result line is invalid."""


def parse_matches(lines: Iterable[str]) -> list[Match]:
    """Parse valid match result lines, skipping blank lines."""

    # Create a list to store the valid match results.
    matches: list[Match] = []

    # Read each line and keep track of its line number for error messages.
    for line_number, line in enumerate(lines, start=1):

        # Split the line at commas and remove extra spaces from each field.
        fields = [field.strip() for field in line.split(",")]

        # Ignore blank lines in the input.
        if not line.strip():
            continue

        # Raise a clear error containing the line number and invalid input.
        def fail(reason: str) -> None:
            raise ParseError(f"Line {line_number}: {reason}: {line.rstrip()}")

        # Each match must contain exactly four fields.
        if len(fields) != 4:
            fail("expected 4 fields")

        # Assign the four fields to descriptive variable names.
        home_team, home_goals_text, away_team, away_goals_text = fields

        # Make sure both teams have names.
        if not home_team or not away_team:
            fail("team name cannot be empty")

        # Convert the goal values from text to integers.
        # If conversion fails, the goals were not whole numbers.
        try:
            home_goals = int(home_goals_text)
            away_goals = int(away_goals_text)
        except ValueError:
            fail("goals must be whole numbers")

        # Goals cannot be negative.
        if home_goals < 0 or away_goals < 0:
            fail("goals cannot be negative")

        # A team cannot play against itself.
        if home_team == away_team:
            fail("a team cannot play itself")

        # Create a Match object and add it to the list of valid matches.
        matches.append(Match(home_team, home_goals, away_team, away_goals))

    # Return all successfully parsed matches.
    return matches