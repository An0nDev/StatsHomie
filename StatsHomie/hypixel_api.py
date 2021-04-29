import requests

def make_req (*, endpoint: str, uuid: str, api_key: str):
    return requests.get (f"https://api.hypixel.net{endpoint}", params = {"key": api_key, "uuid": uuid}).json ()

def get_bedwars_stats (*, uuid: str = None, api_key: str):
    player_resp = make_req (endpoint = "/player", uuid = uuid, api_key = api_key)
    if not player_resp ["success"]:
        return False, player_resp ["cause"]
    else:
        bw = player_resp ["player"] ["stats"] ["Bedwars"]
        bw ["level"] = player_resp ["player"] ["achievements"] ["bedwars_level"]
        return True, bw

def get_player_uuid (*, username: str):
    response = requests.get (f"https://api.mojang.com/users/profiles/minecraft/{username}")
    response.raise_for_status ()
    if response.status_code == 204: return None
    return response.json () ["id"]