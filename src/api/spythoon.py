# Player interface
from typing import Any
import time
import j2l.pytactx.agent as pytactx


class IPainter:
    def getCoordinates(self) -> tuple[int, int]:
        """
        Return the actual coordinates x and y
        """
        ...

    def getDirection(self) -> int:
        """
        Return actual direction as integer from 0 to 3
        0: Est
        1: South
        2: West
        3: North
        """
        ...

    def getTeam(self) -> int:
        """
        Return team number
        """
        ...

    def isPainting(self) -> bool:
        """
        Return True if painting is active, False if painting is inactive
        """
        ...

    def update(self) -> None:
        """
        Fetch the last values of player data from server
        And send buffered requests in one shot to limit bandwidth.
        To be call in the main loop at least every 10 msecs.
        """
        ...

    def move(self) -> None:
        """
        Request a relative move on the grid in front of the previous agent position
        The request will be send the next update() call
        """
        ...

    def rotate(self, dir:int) -> None:
        """
        Request a rotation of the agent on the grid.
        Dir should be integers values from 0 (east) to 3 (south).
        The request will be send the next update() call
        """
        ...

    def paint(self, active:bool):
        """
        Request an activation (active:True) or a deactivation (active:False) of the paint trail.
        The request will be send the next update() call
        """
        ...

    def scanNearbyTiles(self) -> dict[str,Any]:
        """
        Request infos on nearest tiles status : neutral, ally painted or enemy painted
        Return a dictionnary of tiles with their status
        """
        ...

    def scanNearbyPlayers(self) -> dict[str,Any]:
        """
        Request a list of nearby players with their team number and position.
        Return a dictionnary of all nearby players
        """
        ...

    # def moveToBonus(self, x:int, y:int) -> None:
        # """
        # Request a one step move towards the specified x,y absolute direction on the grid.
        # The request will be send the next update() call
        # """
        # ...


class PytactxPainter(IPainter):
    def __init__(self, playerId:str or None=None, arena:str or None=None, username:str or None=None, password:str or None=None, server:str or None=None, port:int=1883) -> None:
        self.__pytactxAgent = pytactx.Agent(playerId, arena, username, password, server, port)

        while len(self.__pytactxAgent.game) == 0:
            self.__pytactxAgent.lookAt((self.__pytactxAgent.dir+1) %4)
            self.__pytactxAgent.update()

    def getCoordinates(self) -> tuple[int, int]:
        # self.__pytactxAgent.update()
        # print(self.__pytactxAgent.x)
        return (self.__pytactxAgent.x, self.__pytactxAgent.y)

    def getDirection(self) -> int:
        return self.__pytactxAgent.dir

    def getTeam(self) -> int:
        return self.__pytactxAgent.team

    def isPainting(self) -> bool:
        return self.__pytactxAgent.isFiring

    def update(self) -> None:
        time.sleep(0.3)
        self.__pytactxAgent.update()
    
    def move(self) -> None:
        match (self.__pytactxAgent.dir):
            case 0:
                self.__pytactxAgent.move(1, 0)
            case 1:
                self.__pytactxAgent.move(0, -1)
            case 2:
                self.__pytactxAgent.move(-1, 0)
            case 3:
                self.__pytactxAgent.move(0, 1)

    def rotate(self, dir:int) -> None:
        self.__pytactxAgent.lookAt(dir)

    def paint(self, active:bool):
        self.__pytactxAgent.fire(active)

    def scanNearbyTiles(self) -> dict[str,Any]:
        return self.__pytactxAgent.map

    def scanNearbyPlayers(self) -> dict[str,Any]:
        return self.__pytactxAgent.range