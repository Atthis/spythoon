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



def createReferee():
    return Referee(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT)

referee = createReferee()

def test_setPartyTimer():
    timer = -10
    assert referee.setPartyTimer(timer) == "Merci de fournir un entier positif"
    
    timer = 599
    assert referee.setPartyTimer(timer) == 599

def test_getPartyTime():
    referee.setPartyTimer(577)
    assert referee.getPartyTimer() == 577

def test_updatePartyTimer():
    startTS = 10000
    currTS = 15000
    referee.setPartyTimer(20)
    assert referee.updatePartyTimer(startTS, currTS) == 15

print(referee.setPartyTimer(-10)) # Merci de fournir un entier positif
print(referee.setPartyTimer(20)) # 20

print(referee.getPartyTimer()) # 20

referee.updatePartyTimer(10000, 15000)
print(referee.getPartyTimer()) # 15
