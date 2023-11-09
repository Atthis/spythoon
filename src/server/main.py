# import of standard libraries
import time
import os
import json
import copy

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

# Import pytactX class and utils
import j2l.pytactx.agent as pytactx
from referee import Referee
from utils import *

# Import json rules file
# Try catch to retrieve rules data
try:
    with open(os.path.join(__fileDir__, 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")

# Referee creation
# referee = pytactx.Agent(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)
referee = Referee(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)
referee.printInfoToArena("⌛ Initialisation de l'arbitre...")

# Reset arena
# referee.openArena(True)
referee.resetArena()
referee.update()
time.sleep(1)

# # Define arena rules from the json
referee.setArenaRules(serverRulesdict)
referee.update()
time.sleep(1)


# # Create players and their rules from the json
referee.createPlayers(serverRulesdict)
referee.update()
time.sleep(0.3)

# Close arena to new player
# referee.openArena(False)
# referee.update()
# time.sleep(0.3)


# Retrieve map status
time.sleep(5)
# referee.updateRefereeMap(referee.getGameInfos()["map"])

# Set starting scores
team1Score, team2Score = referee.resetTeamScores()

# Launch party msg
referee.printInfoToArena("🟢 C'est parti !")
referee.update()
time.sleep(2)

# Reset party timer and retrieve current timestamp
referee.setPartyTimer(300)

# 
referee.printInfoToArena(f"| ⏰ {secondsToMinutesSeconds(referee.getPartyTimer())} | 👑 🍉 Fuschia : {team1Score} / 🫐 Turquoise : {team2Score}.")
referee.update()
time.sleep(0.3)


# Request current timestamp
startTimestamp = referee.getCurrTimestamp()

# Main loop for referee update 
while True:
    # referee direction changes to apply updates
    referee.rotate((referee.getDir()+1)%4)

    for player in referee.getCurrentRange().values():
        referee.setPlayerProfileOnFire(player)

        if player["fire"] and player["ammo"]:
            referee.updateRefereeMap(player["x"], player["y"], player["team"])
            referee.updateScores(referee.getRefereeMap())
            referee.printInfoToArena(f"Scores - team 1 : {team1Score} / team 2 : {team2Score}.")
            referee.decreasePlayerAmmo(player)
            referee.updateArenaMap()
    
    remainingTime = secondsToMinutesSeconds(referee.updatePartyTimer(startTimestamp))
    referee.printInfoToArena(f"| ⏰ {remainingTime} | 👑 🍉 Fuschia : {team1Score} / 🫐 Turquoise : {team2Score}.")
    
    # For each player, apply changes if fire
    # for player in currRange.values():
    #     # If player fire, apply profile which slow its movments
    #     ## SETPROFILEONFIRE()
    #     if player["fire"]:
    #         referee.rulePlayer(player["clientId"], "profile", 1)
    #     else:
    #         referee.rulePlayer(player["clientId"], "profile", 0)

    #     # If player fire and got ammo, change tile status and calc new score
    #     if player["fire"] and player["ammo"]:
    #         ## UPDATEARENAMAP
    #         globalMap[player["y"]][player["x"]] = player["team"]

    #         # calcul de la nouvelle possession et du score de chaque équipe
    #         ## UPDATESCORES
    #         # team1Score, team2Score = updateScore(globalMap)

    #         # Affichage du score dans la GUI
    #         ## PRINTINFOTOARENA
    #         referee.ruleArena("info", f"Scores - team 1 : {team1Score} / team 2 : {team2Score}.")

    #         # Reduction des ammo du joueur
    #         ## DECREASEPLAYERAMMO
    #         referee.rulePlayer(player["playerId"], "ammo", player["ammo"] -1)

    # # Envoi du nouvel etat de la carte
    # referee.ruleArena("map", globalMap)

    # # Mise a jour du timer de la carte
    # #   - recuperation tn
    # currTimestamp = referee.game["t"]
    # #   - recuperer le delta de temps entre les 2 boucles 
    # deltaTime = (currTimestamp - startTimestamp) // 1000

    # # if referee.isGameOver() :
    # #     referee.ruleArena("info", "Partie terminée !")
    # #     referee.ruleArena("pause", True)

    # print(secondsToMinutesSeconds(partyTimer - deltaTime))

    # Envoi des requetes et reception des MAJ du serveur
    referee.update()