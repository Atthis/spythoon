# Definir l'interface pour l'utilisateur

class IPlayer:
    def update():
        ...

    def move():
        ...

    def rotate():
        ...

    def paint():
        ...

    def scanNearestTiles():
        ...

    def detectNearPlayers():
        ...

    def listenBonusSpawn():
        ...

    def moveToBonus():
        ...

class Player:
    def __init__(self) -> None:
        self.hasBonus = False
        