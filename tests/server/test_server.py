# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__fileDir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__libdir__ = os.path.dirname(__fileDir__)
sys.path.append(__libdir__)
__srcDir__ = os.path.join(__libdir__ , 'src', 'api')
sys.path.append(__srcDir__)

import random

from dotenv import load_dotenv
load_dotenv()

PLAYER=os.getenv('PLAYER_ID')
ARENA=os.getenv('ARENA')
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
SERVER=os.getenv('SERVER')
PORT=int(os.getenv('PORT'))

# Import of main class
from src.api.spythoon import PytactxPainter

def createAgent(playerId):
    return PytactxPainter(playerId=playerId, arena=ARENA, username=USERNAME, password=PASSWORD, server=SERVER, port=PORT)

agent1 = createAgent("🍉 joueur1")
agent2 = createAgent("🍉 joueur3")
agent3 = createAgent("🍉 joueur5")
agent4 = createAgent("🫐 joueur2")
agent5 = createAgent("🫐 joueur4")
agent6 = createAgent("🫐 joueur6")


agents = [agent1, agent2, agent3, agent4, agent5, agent6]


### A TESTER
# - changement statut case quand joueur fire
# - changement profil joueur quand fire
# - arrêt peinture cases quand joueur ne tire pas
# - cumul des points quand cases se peignent
# - arrêt de partie si temps imparti écoulé
# - 
# - 

for agent in agents:
    agent.paint(False)
    
agent1.rotate(3)
agent3.rotate(0)
agent5.rotate(0)
agent2.rotate(1)
agent4.rotate(2)
agent6.rotate(2)

while True:

    for agent in agents:
        agent.move()
        # agent.rotate((agent.getDirection() +1) % 4)
        # willFire = random.randint(1, 10)

        agent.paint(True)
        # if willFire < 7:
            # agent.paint(True)
        # else:
            # agent.paint(False)

        agent.update()

