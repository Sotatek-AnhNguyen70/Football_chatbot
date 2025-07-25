from pydantic import BaseModel
from typing import Optional

# Match
class MatchQuery(BaseModel):
    team1_name: str
    team2_name: Optional[str]
    season: int
# Player
class PlayerQuery(BaseModel):
    player_name: str
    team_name: str
    season: int = 2023
# Team
class TeamQuery(BaseModel):
    team_name: str
    season: int