# Allow import without error 
# "relative import with no known parent package"
# In vscode, add .env file with PYTHONPATH="..." 
# with the same dir to allow intellisense
import os
import sys
__fileDir__ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
__libdir__ = os.path.dirname(__fileDir__)
sys.path.append(__libdir__)
__srcDir__ = os.path.join(__libdir__ , 'src', 'server')
sys.path.append(__srcDir__)

import random
import json
import time

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
from src.server.referee import Referee

# Import json rules file
# Try catch to retrieve rules data
try:
    with open(os.path.join(__srcDir__, 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")


def createReferee():
    return Referee(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)

referee = createReferee()

referee.resetArena()
referee.printInfoToArena("")

## TESTS REFEREE CLASS FUNCTIONS
print("==========================")
time.sleep(5)
print("---SetArenaRules & createPlayers---")
print(referee.getGameInfos())
print("--------------------------")
print(referee.getCurrentRange())
referee.setArenaRules(serverRulesdict)
referee.createPlayers(serverRulesdict)
referee.update()

print("---rotate---")
i = 0
while i < 5:
    referee.rotate(i%4)
    print(referee.getDir())
    i += 1
    referee.update()

print("---PrintInfoToArena---")
referee.printInfoToArena("Ici CAEN !!!")
referee.update()
time.sleep(5)

print("---getCurrTimestamp---")
print(referee.getCurrTimestamp())
referee.update()
time.sleep(5)
print(referee.getCurrTimestamp()) # previous time + 5000
referee.update()



## TESTS TIMERMASTER INSTANCE FUNCTIONS
print("---setPartyTimer---")
print(referee.setPartyTimer(-10)) # Merci de fournir un entier positif
print(referee.setPartyTimer(20)) # 20

print("---getPartyTimer---")
print(referee.getPartyTimer()) # 20

print("---updatePartyTimer---")
referee.updatePartyTimer(10)
print(referee.getPartyTimer()) # 15

## TESTS TIMEDEALER INSTANCE FUNCTIONS
print("---resetTeamScore---")
print(referee.resetTeamScores()) # (0, 0)

print("==========================")
time.sleep(10)
print(referee.getGameInfos())
print("--------------------------")
print(referee.getCurrentRange())
time.sleep(10)