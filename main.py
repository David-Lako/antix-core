# --- ANTIX ANTI-CHEAT CORE SYSTEM v0.8 (PRODUCTION EDITION) ---
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the Antix Web API
app = FastAPI(title="Antix Anti-Cheat Network API")

# Global blacklist database
banned_hwids = ["HWID-6666-BAD"]

# Define the data structure incoming from the game
class PlayerTelemetry(BaseModel):
    name: str
    hwid: str
    accuracy: int
    reaction_time: int
    recoil_consistency: int

# The live API endpoint for the game server
@app.post("/scan-player")
def scan_player_endpoint(player: PlayerTelemetry):
    # Pre-connection HWID Filter
    if player.hwid in banned_hwids:
        return {"action": "BAN", "reason": "Hardware ID blacklisted globally."}
        
    # Level 1 Check: Hard Rules
    if player.accuracy > 95 and player.reaction_time < 50:
        banned_hwids.append(player.hwid)
        return {"action": "BAN", "reason": "Robotic reaction time and accuracy."}
        
    # Level 2 Check: Deep Scan Phase
    elif player.accuracy > 90 or player.reaction_time < 80:
        if player.recoil_consistency > 85:
            banned_hwids.append(player.hwid)
            return {"action": "BAN", "reason": "Failed deep recoil consistency scan."}
        else:
            return {"action": "ALLOW", "reason": "Legitimate pro player."}
            
    # Safe Player
    return {"action": "ALLOW", "reason": "Verified gameplay."}
