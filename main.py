# --- ANTIX ANTI-CHEAT CORE SYSTEM v0.9 (TRIPLE-CHECK SECURITY) ---
from fastapi import FastAPI
from pydantic import BaseModel

# Initialize the Antix Web API
app = FastAPI(title="Antix Anti-Cheat Network API")

# Global blacklist database
banned_hwids = ["HWID-6666-BAD"]

# Define the data structure incoming from the game
# Added network_lag_ms to perform the final verification before BAN
class PlayerTelemetry(BaseModel):
    name: str
    hwid: str
    accuracy: int
    reaction_time: int
    recoil_consistency: int
    network_lag_ms: int 

# The live API endpoint for the game server
@app.post("/scan-player")
def scan_player_endpoint(player: PlayerTelemetry):
    # Pre-connection HWID Filter
    if player.hwid in banned_hwids:
        return {"action": "BAN", "reason": "Hardware ID blacklisted globally."}
        
    # LEVEL 1 CHECK: Hard Rules (Obvious Rage Cheater)
    if player.accuracy > 95 and player.reaction_time < 50:
        return trigger_final_verification(player, "Robotic reaction time and accuracy.")
        
    # LEVEL 2 CHECK: Deep Scan Phase (Suspicious/Closet Cheater)
    elif player.accuracy > 90 or player.reaction_time < 80:
        if player.recoil_consistency > 85:
            return trigger_final_verification(player, "Failed deep recoil consistency scan.")
        else:
            return {"action": "ALLOW", "reason": "Legitimate pro player verified."}
            
    # Safe Player
    return {"action": "ALLOW", "reason": "Verified legitimate gameplay."}

# LEVEL 3 CHECK: The Ultimate Verification before issuing a BAN
def trigger_final_verification(player, previous_reason):
    # If network lag is unstable/high (above 150ms), it could be a false positive due to lag (rubberbanding)
    if player.network_lag_ms > 150:
        return {
            "action": "SUSPEND", 
            "reason": f"Flagged for [{previous_reason}], but final ban put on hold due to high network lag ({player.network_lag_ms}ms). Retesting required."
        }
    
    # If the network is perfect, but they still have robotic stats: 100% Confirmed Cheater
    banned_hwids.append(player.hwid)
    return {"action": "BAN", "reason": f"CONFIRMED CHEATER. Passed triple-check verification. Logic error: {previous_reason}"}
