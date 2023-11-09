# Referee interface
from typing import Callable, Any
import time
import j2l.pytactx.agent as pytactx
from utils import *

class ITimerMaster:
    def setPartyTimer(self, timer:int) -> None:
        """
        Set the party duration, in seconds
        """
        ...

    def getPartyTimer(self) -> int:
        """
        return the party timer
        """
        ...

    def updatePartyTimer(self, startTimestamp: int) -> int:
        """
        Update the party timer based on the startTimestamp and the currTimestamp
        """
        ...

class TimerMaster(ITimerMaster):
    def __init__(self) -> None:
        self.partyTimer = 0

    def getPartyTimer(self) -> int:
        return self.partyTimer

    def setPartyTimer(self, timer:int) -> None:
        self.partyTimer = timer

    def updatePartyTimer(self, startTimestamp: int, currTimestamp: int) -> int:
        deltaTime = (currTimestamp - startTimestamp) // 1000
        self.setPartyTimer(self.partyTimer - deltaTime)
        return self.partyTimer