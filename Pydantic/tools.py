import httpx
from typing import Optional
from pydantic_ai import RunContext
from agent import football_agent  # import agent từ file khác
from PydanticModel import MatchQuery, PlayerQuery, TeamQuery

API_KEY = "8ff6223a5f0353ebd66184bb599804d0"
BASE_URL = "https://v3.football.api-sports.io"

async def get_team_id(team_name: str) -> Optional[int]:
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/teams",
            params={"search": team_name},
            headers={"x-apisports-key": API_KEY}
        )
        data = res.json()
        if data["response"]:
            return data["response"][0]["team"]["id"]
        return None

@football_agent.tool
async def get_matches(ctx: RunContext, input: MatchQuery) -> dict:
    print("using get_matches tool")

    team1_id = await get_team_id(input.team1_name)
    if not team1_id:
        return {"error": f"Không tìm thấy đội '{input.team1_name}'"}

    team2_id = await get_team_id(input.team2_name) if input.team2_name else None

    params = {
        "season": input.season,
        "team": team1_id
    }

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/fixtures",
            params=params,
            headers={"x-apisports-key": API_KEY}
        )
        fixtures = res.json()

    if "response" not in fixtures or not fixtures["response"]:
        return {"matches": []}

    if team2_id:
        filtered = [
            match for match in fixtures["response"]
            if match["teams"]["home"]["id"] == team2_id or match["teams"]["away"]["id"] == team2_id
        ]
        return {"matches": filtered}
    else:
        return {"matches": fixtures["response"]}

@football_agent.tool
async def get_players_by_team_and_season(ctx: RunContext, input: TeamQuery) -> dict:
    print('using get_players_by_team_and_season tools')
    team_id = await get_team_id(input.team_name)
    if not team_id:
        return {"error": f"Không tìm thấy đội '{input.team_name}'"}

    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{BASE_URL}/players",
            params={"team": team_id, "season": input.season},
            headers={"x-apisports-key": API_KEY}
        )
        data = res.json()

    return data

@football_agent.tool
async def get_player_info(ctx: RunContext, input: PlayerQuery) -> dict:
    print("using get_player_info tool ")
    team_id = await get_team_id(input.team_name)
    if not team_id:
        return {"error": f"Không tìm thấy đội bóng '{input.team_name}'"}

    params = {
        "search": input.player_name,
        "team": team_id,
        "season": input.season
    }

    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{BASE_URL}/players", params=params, headers={"x-apisports-key": API_KEY})
            if res.status_code != 200:
                return {"error": f"Lỗi API: {res.status_code} - {res.text}"}

            data = res.json()
            if not data.get("response"):
                return {"error": f"Không tìm thấy cầu thủ '{input.player_name}' trong đội '{input.team_name}' mùa {input.season}"}

            player_data = data["response"][0]

            info = {
                "name": player_data["player"]["name"],
                "age": player_data["player"].get("age"),
                "nationality": player_data["player"].get("nationality"),
                "height": player_data["player"].get("height"),
                "weight": player_data["player"].get("weight"),
                "team": player_data["statistics"][0]["team"]["name"],
                "position": player_data["statistics"][0]["games"].get("position"),
                "appearances": player_data["statistics"][0]["games"].get("appearences"),
                "goals": player_data["statistics"][0]["goals"].get("total"),
                "assists": player_data["statistics"][0]["goals"].get("assists"),
            }

            return {
                "summary": info,
                "raw_json": data
            }

        except httpx.RequestError as e:
            return {"error": f"Lỗi kết nối: {str(e)}"}
