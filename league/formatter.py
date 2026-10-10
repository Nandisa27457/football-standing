"""Format league standings as CSV text."""

import csv
from io import StringIO

from league.models import TeamRecord


def format_table(records: list[TeamRecord]) -> str:
    """Return standings as CSV with a header and one-based positions."""
    output = StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "position",
            "team",
            "played",
            "won",
            "drawn",
            "lost",
            "gf",
            "ga",
            "goal_average",
            "points",
        ]
    )

    for position, record in enumerate(records, start=1):
        goal_average = (
            "inf"
            if record.goal_average == float("inf")
            else f"{record.goal_average:.3f}"
        )
        writer.writerow(
            [
                position,
                record.team,
                record.played,
                record.won,
                record.drawn,
                record.lost,
                record.goals_for,
                record.goals_against,
                goal_average,
                record.points,
            ]
        )

    return output.getvalue()
