# import of standard libraries
import time
import os
import json

# File directory definition
__fileDir__ = os.path.dirname(os.path.abspath(__file__))

# ENV variables config
from dotenv import load_dotenv
load_dotenv()
ARBITRE=os.getenv('ARBITRE')
ARENA=os.getenv('ARENA')
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
SERVER=os.getenv('SERVER')
PORT=int(os.getenv('PORT'))
DURATION=int(os.getenv('DURATION'))

# # Import referee class and utils
from referee import Referee
from utils import *

# # Import json rules file
# Try catch to retrieve rules data
try:
    with open(os.path.join(__fileDir__, 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")

# # Referee creation
# referee = pytactx.Agent(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)
referee = Referee(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT, DURATION)
referee.printInfoToArena("⌛ Initialisation de l'arbitre...")

# # Reset arena
# referee.openArena(True)
referee.resetArena()
referee.update()
time.sleep(3)
referee.update()

# # Set Referee map to Arena map
referee.setRefereeMap(referee.getGameInfos()["map"])
referee.update()
time.sleep(0.3)

# # Define arena rules from the json
referee.setArenaRules(serverRulesdict)
referee.update()
time.sleep(1)

# # Create players and their rules from the json
referee.createPlayers(serverRulesdict)
referee.update()
time.sleep(0.3)

# # Close arena to new player
# referee.openArena(False)
# referee.update()
# time.sleep(0.3)

referee.printInfoToArena("⌛ En attente des joueurs ...")
referee.update()
time.sleep(10)
### TODO Wait for all players to connect 
readyPlayers = []
while len(readyPlayers) < len(referee.getCurrentRange()):
    referee.update()
    time.sleep(0.3)
    for player in referee.getCurrentRange().values():
        if not player["idle"]:
            if player["clientId"] not in readyPlayers :
                readyPlayers.append(player["clientId"])

# # Launch party msg
referee.printInfoToArena("🟢 C'est parti !")
referee.update()
time.sleep(2)

# # Timer and scores msg
referee.printInfoToArena(f"| ⏰ {secondsToMinutesSeconds(DURATION)} | 👑 🍉 Fuschia : {referee.getTeamsScores()[0]} / 🫐 Turquoise : {referee.getTeamsScores()[1]}.")
referee.update()
time.sleep(0.3)

# # Request current timestamp
referee.startTimeMaster()

referee.setOldRange(referee.getCurrentRange())

# # Main loop for referee update 
while not referee.isGameOver() :
    # #  referee direction changes to apply updates
    referee.rotate((referee.getDir()+1)%4)

    # # For each player
    for player in referee.getCurrentRange().values():
        # Set profile
        referee.setPlayerProfileOnFire(player)

        # If fire and ammo
        if referee.getCurrentRange()[player["clientId"]]["nFire"] > referee.getOldRange()[player["clientId"]]["nFire"]:
            # Update tile status
            referee.updateRefereeMap(player["x"], player["y"], player["team"])
            # Update teams score
            referee.updateScores(referee.getRefereeMap())
            # Decrease player ammo
            referee.decreasePlayerAmmo(player)
            # Push new map state to the server
            referee.updateArenaMap()

    # # Calcul remaining time and Update arena info with new time and scores
    referee.printInfoToArena(f"| ⏰ {secondsToMinutesSeconds(referee.getRemainingTime())} | 👑 🍉 Fuschia : {referee.getTeamsScores()[0]} / 🫐 Turquoise : {referee.getTeamsScores()[1]}.")

    # # Sent all requests to server
    referee.update()

referee.printInfoToArena(f"| 🔔 PARTIE TERMINEE ! | 👑 🍉 Fuschia : {referee.getTeamsScores()[0]} / 🫐 Turquoise : {referee.getTeamsScores()[1]}.")
referee.update()