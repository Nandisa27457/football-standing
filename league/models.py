"""Data models used by the league app."""

from dataclasses import dataclass


@dataclass(frozen=True)
# Store the details of a single football match.
# frozen=True prevents the match details from being changed after creation.
class Match:
    home_team: str
    home_goals: int
    away_team: str
    away_goals: int


@dataclass
class TeamRecord:
    # Store a team's overall performance in the league.
    team: str
    played: int
    won: int
    drawn: int
    lost: int
    goals_for: int
    goals_against: int

    @property
    def points(self) -> int:
        # Calculate points using the historical rules:
        # 2 points for a win and 1 point for a draw.
        return 2 * self.won + self.drawn

    @property
    def goal_average(self) -> float:
        # Avoid division by zero when the team has conceded no goals.
        if self.goals_against == 0:
            # An unbeaten team that has scored goals has an infinite
            # goal average; otherwise, its goal average is zero.
            return float("inf") if self.goals_for > 0 else 0.0
        
        # Calculate goal average by dividing goals scored by goals conceded.
        return self.goals_for / self.goals_against
