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
from utils import *

# Import json rules file
# Try catch to retrieve rules data
try:
    with open(os.path.join(__fileDir__, 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")

# Referee creation
referee = pytactx.Agent(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)
# Put referee in his own team
referee.rulePlayer(referee.clientId, "team", 0)
# referee.rulePlayer(referee.clientId, "profile", 2)

referee.ruleArena("info", "⌛ Initialisation de l'arbitre...")

# Reset arena
# referee.ruleArena("open", True)
referee.ruleArena("reset", True)
referee.update()
time.sleep(1)

# Define arena rules from the json
for arenaRule, arenaAttribute in serverRulesdict["arenaRules"].items():
    referee.ruleArena(arenaRule, arenaAttribute)
referee.ruleArena("info", "⌛ Définition des règles de la carte ...")
referee.update()
time.sleep(1)

# Create players and their rules from the json
for player, playerAttributes in serverRulesdict["playersRules"].items():
    for attributeKey, attributeValue in playerAttributes.items():
        referee.rulePlayer(player, attributeKey, attributeValue)
referee.ruleArena("info", "⌛ Création des joueurs ...")
referee.update()
time.sleep(0.3)

# Close arena to new player
# referee.ruleArena("open", False)
# referee.update()
# time.sleep(0.3)


# Retrieve map status
time.sleep(5)
globalMap = copy.deepcopy(referee.game["map"])

# Set starting scores
team1Score = 0
team2Score = 0

# Launch party msg
referee.ruleArena("info", "🟢 C'est parti !")
referee.update()
time.sleep(2)

#
referee.ruleArena("info", f"| 👑 🍉 Fuschia : {team1Score} / 🫐 Turquoise : {team2Score}.")
referee.update()
time.sleep(0.3)


# Reset party timer and retrieve current timestamp
partyTimer = 300
startTimestamp = referee.game["t"]

print('----- AVANT boucle -----')
# Main loop for referee update 
while True:
    # referee direction changes to apply updates
    referee.lookAt((referee.dir+1)%4)

    # stocke les infos des joueurs dans une variable deepcopy
    currRange = copy.deepcopy(referee.range)

    # For each player, apply changes if fire
    ## for player in referee.getCurrentRange().values()
    for player in currRange.values():
        # If player fire, apply profile which slow its movments
        ## SETPROFILEONFIRE()
        if player["fire"]:
            referee.rulePlayer(player["clientId"], "profile", 1)
        else:
            referee.rulePlayer(player["clientId"], "profile", 0)

        # If player fire and got ammo, change tile status and calc new score
        if player["fire"] and player["ammo"]:
            ## UPDATEARENAMAP
            globalMap[player["y"]][player["x"]] = player["team"]

            # calcul de la nouvelle possession et du score de chaque équipe
            ## UPDATESCORES
            team1Score, team2Score = updateScore(globalMap)

            # Affichage du score dans la GUI
            ## PRINTINFOTOARENA
            referee.ruleArena("info", f"Scores - team 1 : {team1Score} / team 2 : {team2Score}.")

            # Reduction des ammo du joueur
            ## DECREASEPLAYERAMMO
            referee.rulePlayer(player["playerId"], "ammo", player["ammo"] -1)

    # Envoi du nouvel etat de la carte
    referee.ruleArena("map", globalMap)

    # Mise a jour du timer de la carte
    #   - recuperation tn
    currTimestamp = referee.game["t"]
    #   - recuperer le delta de temps entre les 2 boucles 
    deltaTime = (currTimestamp - startTimestamp) // 1000

    # if referee.isGameOver() :
    #     referee.ruleArena("info", "Partie terminée !")
    #     referee.ruleArena("pause", True)

    print(secondsToMinutesSeconds(partyTimer - deltaTime))

    # Envoi des requetes et reception des MAJ du serveur
    referee.update()



# BOUCLE POUR RECUPERER LES REGLES, ICI SUR LES JOUEURS
# for agentId, attributes in agents.items():
#     for attributeKey, attributeValue in attributes.items():
#         referee.rulePlayer(agentId, attributeKey, attributeValue)
# referee.update()

# # # # EXAMPLES # # # #
### Changing tile status example
# referee.ruleArena("reset", True)
# referee.update()
# referee.ruleArena("mapImgs", ["", 'd3.png'])
# globalMap[0][0] = 1
# referee.ruleArena("map", globalMap)
# referee.update()
# time.sleep(5)
# referee.update()
# print(referee.map)
### Agent creation example
# agents = {
#     "Neo" : 0,
#     "Smith": 0 
# }
# referee.ruleArena("info", "⌛ Création des pnj...")
# for agentId in agents.keys() :
#     referee.rulePlayer(agentId, "profile", referee.game["profiles"].index("pnj"))

### Referee move test
# referee.moveTowards(0,0)
# referee.update()
# time.sleep(5)
# print(referee.x, referee.y)
# referee.moveTowards(25, 11)
# referee.update()
# print(referee.x, referee.y)