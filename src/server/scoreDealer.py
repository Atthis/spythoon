from typing import Any
from utils import *

class IScoreDealer:
    def getTeamsScores(self) -> tuple[int, int]:
        """
        Return teams scores
        """
        ...
        
    def resetTeamScores(self) -> tuple[int, int]:
        """
        Set the teams score to 0
        """
        ...

    def updatePossessions(self, map:[[int]]) -> tuple[int, int]:
        """
        Calculate the number of tiles each team own, and return the values
        """
        ...

    def updateScores(self, map:[[int]]) -> tuple[float, float]:
        """
        Calcul teams scores depending on map tiles status, and return new scores
        """
        ...


class ScoreDealer(IScoreDealer):
    def __init__(self) -> None:
        self.__team1Score = None
        self.__team2Score = None

    def getTeamsScores(self) -> tuple[int, int]:
        return (self.__team1Score, self.__team2Score)

    def resetTeamScores(self) -> None:
        self.__team1Score = 0
        self.__team2Score = 0

    def _updatePossessions(self, map:[[int]]) -> tuple[int, int] or str:
        if not map:
            print("!! ERREUR la map est vide !")
            return ""
        team1Possession = 0
        team2Possession = 0
        for row in map :
            for tileValue in row:
                match tileValue:
                    case 1:
                        team1Possession += 1
                    case 2:
                        team2Possession += 1
        return (team1Possession, team2Possession)
    
    def updateScores(self, map:[[int]]) -> tuple[float, float]:
        if not map:
            print("!! ERREUR la map est vide !")
            return
        self.__team1Score = 0
        self.__team2Score = 0
        team1Possession, team2Possession = self._updatePossessions(map)
        self.__team1Score = calcRelScore(map, team1Possession)
        self.__team2Score = calcRelScore(map, team2Possession)
        return (self.__team1Score, self.__team2Score)