import time

import os
import sys
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

# Import pytactX class
import j2l.pytactx.agent as pytactx

# Import rules json file
import json

try:
    with open(os.path.join(__fileDir__, 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")

# Referee creation
referee = pytactx.Agent(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)
referee.ruleArena("info", "⌛ Initialisation de l'arbitre...")
while ( len(referee.game) == 0 ):
    referee.update()
    referee.lookAt((referee.dir+1) %4)

referee.ruleArena("reset", True)
referee.update()
# referee.ruleArena("mapImgs", ["", os.path.join(__fileDir__, 'assets', 'team1-color.jpg')])
referee.ruleArena("mapImgs", ["", 'd3.png'])

globalMap = referee.game["map"]


globalMap[0][1] = 1
globalMap[0][2] = 1
globalMap[0][3] = 1
referee.ruleArena("map", globalMap)
referee.update()
time.sleep(5)
referee.update()
print(referee.map)



# # Création d'agents actualisés par l'arène elle-même
# agents = {
#     "Neo" : 0,
#     "Smith": 0 
# }
# referee.ruleArena("info", "⌛ Création des pnj...")
# for agentId in agents.keys() :
#     referee.rulePlayer(agentId, "profile", referee.game["profiles"].index("pnj"))


# Affichage dans l'arène du début de la partie par l'arbitre
referee.ruleArena("info", "🟢 C'est parti !")
referee.update()

# Main loop for referee update 
while True:
    # referee direction changes to apply updates
    referee.lookAt((referee.dir+1)%4)
    referee.update()

    # Actualisation des scores des agents
    # tableauScore = ""
    # for agentId in agents.keys():
    #     if ( agentId in referee.range ):
    #         nouveauScore = referee.range[agentId]["nKill"]
    #         # Ajout de vie et de munitions à chaque kill
    #         if ( nouveauScore > agents[agentId] ):
    #             referee.rulePlayer(agentId , "life", referee.range[agentId]["life"]+50)
    #             referee.rulePlayer(agentId , "ammo", referee.range[agentId]["ammo"]+10)
    #         agents[agentId] = nouveauScore
    #     tableauScore += " - 🏆"+agentId +" "+ str(agents[agentId])

    # Affichage du score des 2 bots en temps réel
    # referee.ruleArena("info", tableauScore)

# BOUCLE POUR RECUPERER LES REGLES, ICI SUR LES JOUEURS
# for agentId, attributes in agents.items():
#     for attributeKey, attributeValue in attributes.items():
#         referee.rulePlayer(agentId, attributeKey, attributeValue)
# referee.update()