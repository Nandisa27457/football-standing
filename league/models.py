"""Data models used by the league app."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    home_team: str
    home_goals: int
    away_team: str
    away_goals: int
