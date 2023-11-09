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

from src.server.utils import *
from src.server.scoreDealer import ScoreDealer

def createDealer():
    return ScoreDealer()

dealer = createDealer()

map = [
    [1, 2, 1, 2, 1], 
    [2, 1, 2, 1, 2], 
    [0, 0, 0, 0, 0]
]

def test_resetTeamScores():
    assert dealer.resetTeamScores() == (0, 0)

def test_updatePossessions():
    mapError = 0
    assert type(dealer.updatePossessions(mapError)) == str

    assert dealer.updatePossessions(map) == (5, 5)

def test_updateScores():
    mapError = 0
    assert type(dealer.updatePossessions(mapError)) == str
    
    assert dealer.updateScores(map) == (166.6, 166.6)