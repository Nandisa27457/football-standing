"""Data models used by the league app."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Match:
    home_team: str
    home_goals: int
    away_team: str
    away_goals: int


@dataclass
class TeamRecord:
    team: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int

    @property
    def points(self) -> int:
        return 2 * self.won + self.drawn

    @property
    def goal_average(self) -> float:
        if self.goals_against == 0:
            return float("inf") if self.goals_for > 0 else 0.0
        return self.goals_for / self.goals_against
