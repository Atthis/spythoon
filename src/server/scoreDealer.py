from typing import Any
from utils import *

class IScoreDealer:
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
        ...

    def resetTeamScores(self) -> tuple[int, int]:
        return (0, 0)

    def updatePossessions(self, map:[[int]]) -> tuple[int, int]:
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
        team1Score = 0
        team2Score = 0
        team1Possession, team2Possession = updatePossession(map)
        team1Score = calcRelScore(map, team1Possession)
        team2Score = calcRelScore(map, team2Possession)
        return (team1Score, team2Score)