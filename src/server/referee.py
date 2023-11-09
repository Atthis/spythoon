# Referee interface
from typing import Callable, Any
import time
import j2l.pytactx.agent as pytactx
from utils import *

class IReferee:
    
    def update(slef) -> None:
        """
        Fetch the last values of referee data from server
        And send buffered requests in one shot to limit bandwidth.
        To be call in the main loop at least every 10 msecs. 
        """
    
    def rotate(self, dir:int) -> None:
        """
        Request a rotation of the agent on the grid.
        Dir should be integers values from 0 (east) to 3 (south).
        The request will be send the next update() call
        """
        ...

    def setRefereeTeam(self, team:int) -> None:
        """
        Set the team the referee belong to, so it is not in one of the players' team
        """
        ...

    def setArenaRules(self, rulesFile:dict[str, Any]) -> None:
        """
        Define all the rules of the arena based on a file
        """
        ...

    def setPlayers(self, rulesFile:dict[str, Any]) -> None:
        """
        Create all arena players based on the rules file
        """
        ...

    def printInfoToArena(self, info:str) -> None:
        """
        Print the input string to the arena info area
        """
        ...

    def closeArena(self, close:bool) -> None:
        """
        Close arena so no other player can join
        """
        ...

    def resetArena(self) -> None:
        """
        Reset the entire arena
        """
        ...

    def resetTeamScores(self) -> tuple[int, int]:
        """
        Set the teams score to 0
        """
        ...

    def setRefereeMap(self) -> [[int]]:
        """
        retrieve arena map at the begining of the game, so referee can update a copy locally
        """
        ...

    def updateRefereeMap(self, map:[[int]], x: int, y: int) -> [[int]]:
        """
        update the referee map
        """
        ...

    def updateArenaMap(self, map:[[int]]) -> None:
        """
        Update the arena map with the referee copy
        """
        ...

    def getCurrentRange(self) -> dict[str, Any]:
        """
        retrieve the current range of the referee from the server
        """
        ...

    def setPlayerProfileOnFire(self, playerIsFiring:bool) -> None:
        """
        set the player profile depending on if it is firing or not
        """
        ...

    def updatePossessions(self, map:[[int]]) -> tuple[int, int]:
        """
        Calculate the number of tiles each team own, and return the values
        """

    def updateScores(self, map:[[int]]) -> tuple[float, float]:
        """
        Calcul teams scores depending on map tiles status, and return new scores
        """
        ...

    def decreasePlayerAmmo(self, player:dict[str, Any]) -> None:
        """
        Update player ammo on each shoot
        """
        ...

    def setPartyTimer(self, timer:int) -> None:
        """
        Set the party duration, in seconds
        """
        ...

    def getCurrTimestamp(self) -> int:
        """
        Retrieve current timestamp from the server
        """

    def updatePartyTimer(self, startTimestamp: int) -> int:
        """
        Update the party timer based on the startTimestamp and the currTimestamp
        """
        ...

    def isGameOver(self) -> bool:
        """
        Return true if game is over, depending on specific conditions
        """
        ...

class Referee(IReferee):
    def __init__(self, playerId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883) -> None:
        self.__pytactxAgent = pytactx.Agent(playerId, arena, username, password, server, port)

        while len(self.__pytactxAgent.game) == 0:
            self.__pytactxAgent.lookAt((self.__pytactxAgent.dir+1) %4)
            self.__pytactxAgent.update()
    
    # Here all rules defines by referee

    def setPlayerProfileOnFire(self, player:dict[str, Any]):
        """
        if player["fire"]:
            profile 1
        else:
            profile 2
        """

    def setRefereeTeam(self, team:int) -> None:
        """
        Set the team the referee belong to, so it is not in one of the players' team
        """
        ...

    def setArenaRules(self, rulesFile:dict[str, Any]) -> None:
        """
        Define all the rules of the arena based on a file
        """
        ...

    def setPlayers(self, rulesFile:dict[str, Any]) -> None:
        """
        Create all arena players based on the rules file
        """
        ...

    def printInfoToArena(self, info:str) -> None:
        """
        Print the input string to the arena info area
        """
        ...

    def closeArena(self, close:bool) -> None:
        """
        Close arena so no other player can join
        """
        ...

    def resetArena(self) -> None:
        """
        Reset the entire arena
        """
        ...

    def resetTeamScores(self) -> tuple[int, int]:
        """
        Set the teams score to 0
        """
        ...

    def setRefereeMap(self) -> [[int]]:
        """
        retrieve arena map at the begining of the game, so referee can update a copy locally
        """
        ...

    def updateRefereeMap(self, map:[[int]], x: int, y: int) -> [[int]]:
        """
        update the referee map
        """
        ...

    def updateArenaMap(self, map:[[int]]) -> None:
        """
        Update the arena map with the referee copy
        """
        ...

    def getCurrentRange(self) -> dict[str, Any]:
        """
        retrieve the current range of the referee from the server
        """
        ...

    def setPlayerProfileOnFire(self, playerIsFiring:bool) -> None:
        """
        set the player profile depending on if it is firing or not
        """
        ...

    def updatePossessions(self, map:[[int]]) -> tuple[int, int]:
        """
        Calculate the number of tiles each team own, and return the values
        """

    def updateScores(self, map:[[int]]) -> tuple[float, float]:
        """
        Calcul teams scores depending on map tiles status, and return new scores
        """
        ...

    def decreasePlayerAmmo(self, player:dict[str, Any]) -> None:
        """
        Update player ammo on each shoot
        """
        ...

    def setPartyTimer(self, timer:int) -> None:
        """
        Set the party duration, in seconds
        """
        ...

    def getCurrTimestamp(self) -> int:
        """
        Retrieve current timestamp from the server
        """

    def updatePartyTimer(self, startTimestamp: int) -> int:
        """
        Update the party timer based on the startTimestamp and the currTimestamp
        """
        ...

    def isGameOver(self) -> bool:
        """
        Return true if game is over, depending on specific conditions
        """
        ...