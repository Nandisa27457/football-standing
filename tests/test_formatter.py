"""Tests for formatting standings as CSV."""

import csv
from io import StringIO

from league.formatter import format_table
from league.models import TeamRecord


def test_formats_header_positions_and_three_decimal_goal_average() -> None:
    records = [
        TeamRecord("First", 2, 1, 1, 0, 5, 2),
        TeamRecord("Second", 1, 0, 0, 1, 1, 3),
    ]

    rows = list(csv.reader(StringIO(format_table(records))))

    assert rows[0] == [
        "position", "team", "played", "won", "drawn", "lost", "gf", "ga",
        "goal_average", "points",
    ]
    assert rows[1] == ["1", "First", "2", "1", "1", "0", "5", "2", "2.500", "3"]
    assert rows[2] == ["2", "Second", "1", "0", "0", "1", "1", "3", "0.333", "0"]


def test_formats_infinite_goal_average_as_inf() -> None:
    record = TeamRecord("Clean sheet", 1, 1, 0, 0, 2, 0)

    assert list(csv.reader(StringIO(format_table([record]))))[1][8] == "inf"


def test_quotes_team_name_containing_comma() -> None:
    record = TeamRecord("A, B", 1, 0, 1, 0, 1, 1)

    assert '"A, B"' in format_table([record])


def test_empty_list_gives_only_header() -> None:
    assert format_table([]) == (
        "position,team,played,won,drawn,lost,gf,ga,goal_average,points\n"
    )
