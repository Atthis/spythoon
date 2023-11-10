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

def test_setRoundDuration():
    timer = -10
    assert timeMaster.setRoundDuration(timer) == "Merci de fournir un entier positif"
    
    timer = 599
    assert timeMaster.setRoundDuration(timer) == 599

def test_getPartyTime():
    timeMaster.setRoundDuration(577)
    assert timeMaster.getRoundDuration() == 577

def test_updateRoundDuration():
    startTS = 10000
    currTS = 15000
    timeMaster.setRoundDuration(20)
    assert timeMaster.updateRoundDuration(startTS, currTS) == 15