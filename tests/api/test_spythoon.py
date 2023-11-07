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

from dotenv import load_dotenv
load_dotenv()

PLAYER=os.getenv('PLAYER_ID')
ARENA=os.getenv('ARENA')
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
SERVER=os.getenv('SERVER')
PORT=int(os.getenv('PORT'))

# Import of main class
from src.api.spythoon import PytactxPainter


def createAgent(playerId):
    return PytactxPainter(playerId=playerId, arena=ARENA, username=USERNAME, password=PASSWORD, server=SERVER, port=PORT)


painter = None
# painter.update()
# print(painter.isPainting())
# painter.paint(True)
# print(painter.scanNearbyTiles())
# print(len(painter.scanNearbyTiles()))
# painter.update()
# print(painter.isPainting())
painter = createAgent(PLAYER)


def test_instanciation():
    painterTeam2 = createAgent("Team2")
    painter.update()
    painterTeam2.update()
    xt1, yt1 = painter.getCoordinates()
    xt2, yt2 = painterTeam2.getCoordinates()
    # Test if team 1 player spawn in the right area
    assert  0 <= xt1 < 26 and 0 <= yt1 < 12, "Team1 player doesn't spawn in the right position"
    # Test if team 2 player spawn in the right area
    assert  0 <= xt2 < 26 and 0 <= yt2 < 12, "Team2 player doesn't spawn in the right position"

def test_getDirection():
    painter.update()
    assert 0 <= painter.getDirection() <= 3

def test_getTeam():
    painter.update()
    assert painter.getTeam() == 1 or painter.getTeam() == 2 or painter.getTeam() == 0

def test_isPainting():
    painter.update()
    painter.paint(True)
    painter.update()
    assert painter.isPainting() == True

def test_rotate():
    currDir = painter.getDirection()
    painter.rotate(19)
    painter.update()
    newDir = painter.getDirection()
    assert currDir == newDir, "Non respect de la précondition de rotate"

    currDir = painter.getDirection()
    print(currDir)
    expectedDir = 3
    painter.rotate(expectedDir)
    painter.update()
    newDir = painter.getDirection()
    assert expectedDir == newDir, "Erreur quand respect de la précondition de rotate"

def test_move():
    painter.rotate(0)
    painter.update()
    currX, currY = painter.getCoordinates()
    painter.move()
    painter.update()
    newX, newY = painter.getCoordinates()
    assert newX == currX + 1 and newY == currY, "Erreur de déplacement sur X"

    painter.rotate(1)
    painter.update()
    currX, currY = painter.getCoordinates()
    painter.move()
    painter.update()
    newX, newY = painter.getCoordinates()
    assert newX == currX and newY == currY + 1, "Erreur de déplacement sur Y"

def test_scanNearbyTiles():
    painter.update()
    nearestTiles = painter.scanNearbyTiles()
    assert len(nearestTiles) == 12

def test_scanNearbyPlayer():
    movingPlayer = createAgent("Movin'")
    px, py = painter.getCoordinates()
    mpx, mpy = movingPlayer.getCoordinates()

    # Rotate movingPlayer to look at painter
    if mpx > px :
        movingPlayer.rotate(2)
    else:
        movingPlayer.rotate(0)
    movingPlayer.update()

    # Moving movingPlayer on x to get to painter
    while mpx != px +1 or mpx != px - 1:
        movingPlayer.move()
        movingPlayer.update()

    # Rotate movingPlayer to look at painter
    if mpy > py :
        movingPlayer.rotate(3)
    else:
        movingPlayer.rotate(1)

    # Moving movingPlayer on y to get to painter
    while mpy != py +1 or mpy != py - 1:
        movingPlayer.move()
        movingPlayer.update()

    nearbyPlayers = painter.scanNearbyPlayers()
    # Look if function retrieve nearby players
    assert len(nearbyPlayers) != 0, "Erreur dans la detection de joueurs à proximité"

    # Test if player team is OK
    assert nearbyPlayers[0].team == 1 or nearbyPlayers[0].team == 2

    # Test if player coordinates are OK
    assert nearbyPlayers[0].x >= 0 and nearbyPlayers[0].y >= 0