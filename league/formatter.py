"""Format league standings as CSV text."""

import csv
from io import StringIO

from league.models import TeamRecord


def format_table(records: list[TeamRecord]) -> str:
    """Return standings as CSV with a header and one-based positions."""

    # Create an in-memory text buffer to store the CSV output.
    output = StringIO(newline="")

   # Create a CSV writer and use a newline character after each row.
    writer = csv.writer(output, lineterminator="\n")

     # Write the column headings as the first row of the CSV output.
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

 # Loop through the team records and assign positions starting at 1.
    for position, record in enumerate(records, start=1):

        # Display an infinite goal average as "inf".
        # Otherwise, format the goal average to three decimal places.
        goal_average = (
            "inf"
            if record.goal_average == float("inf")
            else f"{record.goal_average:.3f}"
        )

        # Write each team's statistics as a row in the CSV output.
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


# Return the complete CSV output as a string.
    return output.getvalue()
