# Codex Session Log

**Project:** Football League Standings CLI
**Date:** 9 October 2026
**Working directory:** `football-standing`
**AI assistant:** OpenAI Codex CLI (used through VS Code)

## Session 1: Create the initial module files

### User request

Read `AGENTS.md`. Create the empty module files in `league/`: `models.py`, `parser.py`, `standings.py`, `formatter.py`, and `cli.py`. Each file should contain a one-line docstring, with no logic yet.

### AI actions

1. Read `AGENTS.md` and checked the existing files in `league/`.
2. Created the five requested Python module files.
3. Added a one-line docstring to each file.
4. Checked the Git status to confirm the new files.

### Result

The five module files were created successfully. No application logic was added during this session.

### Files created

* `league/models.py`
* `league/parser.py`
* `league/standings.py`
* `league/formatter.py`
* `league/cli.py`

### Notes

The existing changes to `.gitignore`, `AGENTS.md`, and `CONVENTIONS.md` were left untouched.

## Session 2: Implement the CSV Parser

### User request

> Read AGENTS.md. Implement Piece 3, the parser, and its tests. Only touch these files:
> - league/models.py
> - league/parser.py
> - tests/test_parser.py
>
> models.py: a frozen dataclass Match with fields home_team (str), home_goals (int), away_team (str), away_goals (int). Type hints everywhere.
>
> parser.py:
> - class ParseError(ValueError)
> - parse_matches(lines: Iterable[str]) -> list[Match]. It takes lines of text and does NO file reading.
> - Input format: home_team,home_goals,away_team,away_goals
> - Skip blank lines. Strip whitespace around every field.
> - Raise ParseError for: wrong number of fields, empty team name, goals that are not whole numbers, negative goals, and a team playing itself.
> - Every error message must include the line number (counting from 1, blank lines included) and the offending line text.
>
> tests/test_parser.py: use pytest. Cover a valid line, whitespace trimming, blank lines skipped, each error case above, and that the line number in the message is correct when a bad line comes after blank lines.
>
> Keep it simple and readable. Do not add features I did not ask for. When done, run python -m pytest and show me the result.

### AI response and implementation summary

The assistant said it would read the repository instructions and current files, implement the parser and focused tests in the three allowed files, then run `python -m pytest` as requested. It implemented a frozen `Match` dataclass, `ParseError`, and `parse_matches`, which splits comma-separated lines, strips fields, skips blank lines, validates field count, team names, integer and nonnegative goals, and prevents a team playing itself. Error messages include the 1-based line number and line text. Pytest cases cover valid input, whitespace trimming, blank lines, invalid inputs, and line numbering after blank lines.

### Files changed

* `league/models.py` — replaced the module docstring with the frozen `Match` dataclass.
* `league/parser.py` — replaced the module docstring with parser implementation and validation.
* `tests/test_parser.py` — created parser tests.

### Tests and results

Ran `python -m pytest`. Result: **11 passed in 0.02s** (pytest reported 11 tests collected; exit code 0).

No implementation or test errors were encountered.
