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

def calcRelScore(map, teamScore) -> float:
    mapSurface = len(map) * len(map[0])
    return truncate((teamScore / mapSurface * 500), 1)

def test_calcRelScore():
   map = [
        [0, 0, 0],
        [0, 0, 0]
    ]
   assert calcRelScore(map, 2) == 166.6

def updateScore(map: [[int]]) -> tuple[float, float]:
    team1Score = 0
    team2Score = 0
    team1Possession, team2Possession = updatePossession(map)
    team1Score = calcRelScore(map, team1Possession)
    team2Score = calcRelScore(map, team2Possession)
    return (team1Score, team2Score)

def updatePossession(map:[[int]]) -> tuple[int, int]:
    team1Possession = 0
    team2Possession = 0
    for row in map :
        for tileValue in row:
            match tileValue:
                case 1:
                    # team1Possession, team1Score = updateScore(team1Possession, team1Score, map)
                    team1Possession += 1
                case 2:
                    # team2Possession, team2Score = updateScore(team2Possession, team2Score, map)
                    team2Possession += 1
    return (team1Possession, team2Possession)

def test_updateScore():
    map = [
        [1, 1, 1],
        [2, 2, 2]
    ]
    assert updateScore(map) == (250, 250)

    