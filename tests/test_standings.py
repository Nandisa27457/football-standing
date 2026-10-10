"""Tests for league standings calculations."""

from league.models import Match, TeamRecord
from league.standings import calculate_standings


def test_win_draw_loss_points_and_records_for_both_teams() -> None:
    records = calculate_standings(
        [
            Match("Alpha", 2, "Beta", 0),
            Match("Alpha", 1, "Gamma", 1),
            Match("Alpha", 0, "Delta", 1),
        ]
    )
    by_team = {record.team: record for record in records}

    assert set(by_team) == {"Alpha", "Beta", "Gamma", "Delta"}
    assert (by_team["Alpha"].played, by_team["Alpha"].won,
            by_team["Alpha"].drawn, by_team["Alpha"].lost,
            by_team["Alpha"].points) == (3, 1, 1, 1, 3)
    assert (by_team["Beta"].played, by_team["Beta"].lost,
            by_team["Beta"].points) == (1, 1, 0)
    assert by_team["Gamma"].drawn == 1
    assert by_team["Delta"].won == 1


def test_goals_accumulate_over_several_matches() -> None:
    records = calculate_standings(
        [Match("A", 3, "B", 1), Match("C", 2, "A", 4)]
    )
    alpha = next(record for record in records if record.team == "A")

    assert (alpha.played, alpha.goals_for, alpha.goals_against) == (2, 7, 3)


def test_empty_input_returns_empty_list() -> None:
    assert calculate_standings([]) == []


def test_goal_average_zero_against_is_infinite_and_ranks_above_finite() -> None:
    records = calculate_standings(
        [Match("Untouched", 2, "Victim", 0), Match("Finite", 4, "Other", 1)]
    )
    by_team = {record.team: record for record in records}

    assert by_team["Untouched"].goal_average == float("inf")
    assert records.index(by_team["Untouched"]) < records.index(by_team["Finite"])


def test_zero_zero_goal_average_is_zero() -> None:
    record = TeamRecord("Nil", 1, 0, 1, 0, 0, 0)

    assert record.goal_average == 0.0


def test_goal_average_ranks_above_goal_difference() -> None:
    records = calculate_standings(
        [
            Match("Team A", 4, "A Opponent", 1),
            Match("Team B", 10, "B Opponent", 6),
        ]
    )

    assert [record.team for record in records[:2]] == ["Team A", "Team B"]


def test_infinite_goal_average_ties_break_by_goals_then_name() -> None:
    records = calculate_standings(
        [
            Match("Zulu", 3, "Zulu Opponent", 0),
            Match("Beta", 2, "Beta Opponent", 0),
            Match("Alpha", 2, "Alpha Opponent", 0),
        ]
    )

    assert [record.team for record in records[:3]] == ["Zulu", "Alpha", "Beta"]
