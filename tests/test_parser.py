import pytest

from league.models import Match
from league.parser import ParseError, parse_matches


def test_parse_valid_line() -> None:
    assert parse_matches(["Arsenal,2,Chelsea,1\n"]) == [
        Match("Arsenal", 2, "Chelsea", 1)
    ]


def test_strips_whitespace_around_fields() -> None:
    assert parse_matches([" Arsenal , 2 , Chelsea , 1 "]) == [
        Match("Arsenal", 2, "Chelsea", 1)
    ]


def test_skips_blank_lines() -> None:
    assert parse_matches(["\n", "  \n", "Arsenal,2,Chelsea,1\n"]) == [
        Match("Arsenal", 2, "Chelsea", 1)
    ]


@pytest.mark.parametrize(
    "line",
    [
        "Arsenal,2,Chelsea",
        "Arsenal,,Chelsea,1",
        ",2,Chelsea,1",
        "Arsenal,2,,1",
        "Arsenal,two,Chelsea,1",
        "Arsenal,-1,Chelsea,1",
        "Arsenal,2,Arsenal,1",
    ],
)
def test_invalid_line_raises_parse_error_with_line_and_text(line: str) -> None:
    with pytest.raises(ParseError) as error:
        parse_matches([line])

    assert "line 1" in str(error.value).lower()
    assert line in str(error.value)


def test_line_number_counts_blank_lines() -> None:
    bad_line = "Arsenal,2,Chelsea"
    with pytest.raises(ParseError) as error:
        parse_matches(["\n", "  \n", bad_line])

    assert "line 3" in str(error.value).lower()
    assert bad_line in str(error.value)
