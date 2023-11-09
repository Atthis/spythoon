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

from src.server.timerMaster import TimerMaster

def createMaster():
    return TimerMaster()

timeMaster = createMaster()

def test_setPartyTimer():
    timer = -10
    assert timeMaster.setPartyTimer(timer) == "Merci de fournir un entier positif"
    
    timer = 599
    assert timeMaster.setPartyTimer(timer) == 599

def test_getPartyTime():
    timeMaster.setPartyTimer(577)
    assert timeMaster.getPartyTimer() == 577

def test_updatePartyTimer():
    startTS = 10000
    currTS = 15000
    timeMaster.setPartyTimer(20)
    assert timeMaster.updatePartyTimer(startTS, currTS) == 15