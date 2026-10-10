"""End-to-end coverage for the matchweek 10 input and CLI output."""

import csv
from pathlib import Path

from league.cli import main


TESTS_DIR = Path(__file__).parent
PROJECT_DIR = TESTS_DIR.parent
INPUT_FILE = PROJECT_DIR / "data" / "input_1974_75_week10.csv"
EXPECTED_FILE = TESTS_DIR / "expected_week10.csv"


def test_matchweek_10_output_matches_expected_file(tmp_path: Path) -> None:
    output_file = tmp_path / "standings.csv"

    assert main([str(INPUT_FILE), "-o", str(output_file)]) == 0
    assert output_file.read_text(encoding="utf-8") == EXPECTED_FILE.read_text(
        encoding="utf-8"
    )


# TODO: Remove this extra test; its totals are covered by the expected-output check.
def test_matchweek_10_totals(tmp_path: Path) -> None:
    output_file = tmp_path / "standings.csv"
    assert main([str(INPUT_FILE), "-o", str(output_file)]) == 0

    with output_file.open(encoding="utf-8", newline="") as standings_file:
        rows = list(csv.DictReader(standings_file))

    # The input contains one appearance for each of the 22 clubs in its 22 matches.
    assert sum(int(row["played"]) for row in rows) == 22
    # Ten of the 22 match results are wins.
    assert sum(int(row["won"]) for row in rows) == 10
    # Two of the 22 match results are draws.
    assert sum(int(row["drawn"]) for row in rows) == 2
    # Ten of the 22 match results are losses.
    assert sum(int(row["lost"]) for row in rows) == 10
    # Every goal scored is a goal for one team in the table.
    assert sum(int(row["gf"]) for row in rows) == 31
    # Every goal conceded is a goal against one team in the table.
    assert sum(int(row["ga"]) for row in rows) == 31
    # A win earns two points and a draw earns one, totaling 10*2 + 2 = 22.
    assert sum(int(row["points"]) for row in rows) == 22
