"""Tests for the command-line interface."""

import io

from league.cli import main


def test_reads_file_and_writes_output_file(tmp_path) -> None:
    input_file = tmp_path / "matches.csv"
    output_file = tmp_path / "table.csv"
    input_file.write_text("Arsenal,2,Chelsea,1\n", encoding="utf-8")

    assert main([str(input_file), "-o", str(output_file)]) == 0
    assert output_file.read_text(encoding="utf-8") == (
        "position,team,played,won,drawn,lost,gf,ga,goal_average,points\n"
        "1,Arsenal,1,1,0,0,2,1,2.000,2\n"
        "2,Chelsea,1,0,0,1,1,2,0.500,0\n"
    )


def test_reads_stdin_and_writes_stdout(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.stdin", io.StringIO("Arsenal,2,Chelsea,1\n"))

    assert main([]) == 0
    assert capsys.readouterr().out.startswith(
        "position,team,played,won,drawn,lost,gf,ga,goal_average,points\n"
    )


def test_bad_line_returns_one_and_prints_line_number(tmp_path, capsys) -> None:
    input_file = tmp_path / "bad.csv"
    input_file.write_text("Arsenal,not-a-score,Chelsea,1\n", encoding="utf-8")

    assert main([str(input_file)]) == 1
    captured = capsys.readouterr()
    assert "line 1" in captured.err.lower()
    assert captured.out == ""


def test_missing_file_returns_two_without_traceback(tmp_path, capsys) -> None:
    missing_file = tmp_path / "missing.csv"

    assert main([str(missing_file)]) == 2
    captured = capsys.readouterr()
    assert "missing.csv" in captured.err
    assert "traceback" not in captured.err.lower()
    assert captured.out == ""
