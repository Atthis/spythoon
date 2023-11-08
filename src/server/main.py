# import of standard libraries
import time
import os
import sys
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
# Import rules json file

# Try catch to retrieve rules data
try:
    with open(os.path.join(__fileDir__, 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")

# Referee creation
referee = pytactx.Agent(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)
referee.rulePlayer(referee.clientId, "team", 0)

referee.ruleArena("info", "⌛ Initialisation de l'arbitre...")

# Reset de l'arene
referee.ruleArena("reset", True)
referee.update()
time.sleep(1)

# 1 - Definition des regles de l'arene : on boucle dans le dico de regles pour appliquer les regles
for arenaRule, arenaAttribute in serverRulesdict["arenaRules"].items():
    referee.ruleArena(arenaRule, arenaAttribute)

referee.ruleArena("info", "⌛ Définition des règles de la carte ...")
referee.update()
time.sleep(2)

# 2 - Creation des joueurs a partir du dico de regles
for player, playerAttributes in serverRulesdict["playersRules"].items():
    for attributeKey, attributeValue in playerAttributes.items():
        referee.rulePlayer(player, attributeKey, attributeValue)

referee.ruleArena("info", "⌛ Création des joueurs ...")
referee.update()
time.sleep(2)

# 3 - Fermeture de l'arene : referee.ruleArena("open", False)
referee.ruleArena("open", False)
referee.update()
time.sleep(0.3)

# Reset du timer en secondes  recuperation du timestamp actuel transcrit en secondes
partyTimer = 300
startTimestamp = referee.game["t"]

# Retrieve map status
globalMap = copy.deepcopy(referee.game["map"])

# Set starting scores
team1Score = 0
team2Score = 0

# Launch party msg
referee.ruleArena("info", "🟢 C'est parti !")


referee.update()
time.sleep(0.3)

print(referee.range)

# Main loop for referee update 
while True:
    # referee direction changes to apply updates
    referee.lookAt((referee.dir+1)%4)

    # stocke les infos de la map et des joueurs dans une variable deepcopy
    currRange = copy.deepcopy(referee.range)

    # infos des joueurs : position, nFire

    # Par joueur, si Fire, coloration de la case a la position du joueur
    for player in currRange.values():
        print(player)
        if player["fire"] and player["ammo"] != 0:
            match player["team"]:
                case "1":
                    globalMap[player["y"]][player["x"]] = 1
                case "2":
                    globalMap[player["y"]][player["x"]] = 2
            player["ammo"] = player["ammo"] - 1

    # Envoi du nouvel etat de la carte
    referee.ruleArena("map", globalMap)

    # Calculer le score de chaque équipe
    for row in globalMap :
        for tileValue in row:
            match tileValue:
                case 1:
                    team1Score += 1
                case 2:
                    team2Score += 1
    


    # Mise a jour du timer de la carte
    #   - recuperation tn
    currTimestamp = referee.game["t"]
    #   - recuperer le delta de temps entre les 2 boucles 
    deltaTime = (currTimestamp - startTimestamp) // 1000
    print(deltaTime)

    # if deltaTime >= partyTimer:
    #     referee.ruleArena("info", "Partie terminée !")
    #     referee.ruleArena("pause", True)

    print(secondsToMinutesSeconds(partyTimer - deltaTime))

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