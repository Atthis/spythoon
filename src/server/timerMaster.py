from typing import Any

import sys
import os
LIB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(LIB_DIR)
SRC_DIR = os.path.join(LIB_DIR , 'src')
sys.path.append(SRC_DIR)

from src.server.j2l.pytactx.agent import Agent

class ITimerMaster:
    def start(self) -> None:
        """
        Start the time master, saving the current timestamp
        """
        ...

    def getRoundDuration(self) -> int:
        """
        return the party timer
        """
        ...

    def setRoundDuration(self, timer:int) -> None:
        """
        Set the party duration, in seconds
        """
        ...

    def getCurrTimestamp(self) -> int:
        """
        Return the current timestamp from the server
        """
        ...

    def getRemainingTime(self) -> int:
        """
        Return remaining time based on the startTimestamp and the currTimestamp
        """
        ...

    def setRemainingTime(self) -> None:
        """
        set the remaining time depending on the elapsed time
        """
        ...

class TimerMaster(ITimerMaster):
    def __init__(self, agent: Agent, roundDuration: int=300) -> None:
        self.__pytactxAgent = agent
        self.__roundDuration = roundDuration
        self.__startTimestamp = None
        self.__remainingTime = None

    def start(self) -> None:
        self.__startTimestamp = self.__pytactxAgent.game["t"]

    def getRoundDuration(self) -> int:
        return self.__roundDuration

    def setRoundDuration(self, timer:int) -> Any:
        if timer < 0:
            return "Merci de fournir un entier positif"
        self.__roundDuration = timer
        return self.__roundDuration

    def getCurrTimestamp(self) -> int:
        return self.__pytactxAgent.game["t"]

    def getRemainingTime(self) -> int:
        self.setRemainingTime()
        return self.__remainingTime

    def setRemainingTime(self) -> None :
        deltaTime = (self.getCurrTimestamp() - self.__startTimestamp) // 1000
        self.__remainingTime = self.__roundDuration - deltaTime