import random
from src.api.spythoon import PytactxPainter

# def createPlayer(playerId: str, arena: str, username: str, password: str, server: str, port: int) -> PytactxPainter:
#     player = PytactxPainter(playerId, arena, username, password, server, port)

#     return player


# def gameLoopActions(player):
#     player.rotate(random.randint(1, 10) % 4)
#     player.move()
#     player.update()

class MyPainter(PytactxPainter):
    def __init__(self, playerId: str = None, arena: str = None, username: str = None, password: str = None, server: str = None, port: int = 1883) -> None:
        super().__init__(playerId, arena, username, password, server, port)
    
    def gameLoopActions(self):
        self.move()
        willFire = random.randint(1, 10)

        # self.paint(True)
        if willFire < 7:
            self.paint(True)
        else:
            self.paint(False)
            
        self.rotate(random.randint(1, 10) % 4)
        self.update()