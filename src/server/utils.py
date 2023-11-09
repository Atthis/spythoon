import math
from typing import Any

def truncate(number, digits) -> float:
    # Improve accuracy with floating point operations, to avoid truncate(16.4, 2) = 16.39 or truncate(-1.13, 2) = -1.12
    nbDecimals = len(str(number).split('.')[1]) 
    if nbDecimals <= digits:
        return number
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

def secondsToMinutesSeconds(s) -> None:
   min = s // 60
   sec = s % 60
   return "%02d:%02d" % (min, sec)

def test_timeStampToTimer() -> None:
   time1 = 300
   assert secondsToMinutesSeconds(time1) == "05:00"
   
   time2 = 4225
   assert secondsToMinutesSeconds(time2) == "70:25"

def calcRelScore(mapX, mapY, teamScore) -> float:
   return truncate((teamScore / (mapX * mapY) * 500), 1)

def test_calcRelScore():
   assert calcRelScore(26, 12, 2) == 3.2

def updateScore(teamPossession, teamScore, mapX, mapY) -> tuple[int, int]:
   teamPossession = teamPossession + 1
   teamScore = calcRelScore(mapX, mapY, teamPossession)
   return (teamPossession, teamScore)

def updatePossession(Map:dict[Any], mapX, mapY) -> tuple[float, float]:
    team1Possession = 0
    team1Score = 0
    team2Possession = 0
    team2Score = 0
    for row in Map :
        for tileValue in row:
            match tileValue:
                case 1:
                    team1Possession, team1Score = updateScore(team1Possession, team1Score, mapX, mapY)
                case 2:
                    team2Possession, team2Score = updateScore(team2Possession, team2Score, mapX, mapY)
    return (team1Score, team2Score)

# def test_updatePossession():
#     map = [
#         [1, 1, 1],
#         [2, 2, 2]
#     ]
#     mapSurface = len(map) * len(map[0])

    