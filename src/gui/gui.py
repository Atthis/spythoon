from random import choice, randint
import typing
import json
import time
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QPoint, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QGridLayout, QHBoxLayout, QStackedLayout
from PyQt5.QtGui import QPalette , QColor, QBrush, QImage, QPixmap


# Only needed for access to command line arguments
import sys
import os

LIB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(LIB_DIR)
SRC_DIR = os.path.join(LIB_DIR , 'src')
sys.path.append(SRC_DIR)

from utils import BgSetter
from arenaWidget import ArenaWidget
from src.server.referee import Referee
from src.server.utils import secondsToMinutesSeconds
from src.api.spythoon import PytactxPainter
from mainPlayer import MyPainter

# ENV variables config
from dotenv import load_dotenv
load_dotenv()
ARBITRE=os.getenv('ARBITRE')
ARENA=os.getenv('ARENA')
USERNAME=os.getenv('USERNAME')
PASSWORD=os.getenv('PASSWORD')
SERVER=os.getenv('SERVER')
PORT=int(os.getenv('PORT'))
DURATION=int(os.getenv('DURATION'))

# # Import json rules file
# Try catch to retrieve rules data
try:
    with open(os.path.join(SRC_DIR, 'server', 'serverRules.json')) as json_data:
        serverRulesdict = json.load(json_data)
except Exception as e:
    print(f"Une erreur est survenue dans le chargement des données : {e}")


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Spythoon - Peignez votre territoire !")
        self.setFixedSize(QSize(1470, 860))


        palette = self.palette()
        color = QColor(255, 255, 255)
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)

        mainWindow = QWidget(self, objectName = "mainWindow")
        layout = QStackedLayout(mainWindow, objectName = "mainWindowLayout")
        mainWindow.setLayout(layout)

        bgWidget = BgSetter("appBg", 'bgUI.jpg', CURR_DIR, self.width(), self.height(), self)

        uiWidget = QWidget(self, objectName = "uiWidget")
        uiLayout = QGridLayout(uiWidget, objectName = "uiLayout")
        uiWidget.setLayout(uiLayout)

        # Infos widget : teams colors/numbers and timer
        self.infosWidget = QWidget(uiWidget, objectName = "infosWidget")
        # infosWidget.setMinimumHeight(300)
        infosLayout = QHBoxLayout(self.infosWidget, objectName = "infosLayout")
        infosLayout.setSpacing(100)
        infosLayout.addWidget(QLabel("Team #1", objectName = "team1Infos"))
        infosLayout.addWidget(QLabel("05:00", objectName = "timeInfos"))
        infosLayout.addWidget(QLabel("Team #2", objectName = "team2Infos"))

        # Arena init
        self.arenaWidget = ArenaWidget(uiWidget)

        # Scores widget
        self.scoreWidget = QWidget(uiWidget, objectName = "scoreWidget")
        scoreLayout = QHBoxLayout(self.scoreWidget, objectName = "scoreLayout")
        self.scoreWidget.setLayout(scoreLayout)
        scoreLayout.setSpacing(300)
        scoreLayout.addWidget(QLabel("00.00", objectName = "Team1Score"))
        scoreLayout.addWidget(QLabel("00.00", objectName = "Team2Score"))
            
        uiLayout.addWidget(self.infosWidget, 0, 0, Qt.AlignCenter)
        uiLayout.addWidget(self.arenaWidget, 1, 0, Qt.AlignCenter)
        uiLayout.addWidget(self.scoreWidget, 2, 0, Qt.AlignCenter)

        layout.insertWidget(0, bgWidget)
        layout.insertWidget(1, uiWidget)
        layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        layout.setCurrentIndex(1)

        self.setCentralWidget(mainWindow)

        # Timer defragmenting the loop to simulate a While True condition
        self.timer = QTimer()
        self.timer.setTimerType(Qt.PreciseTimer)
        self.timer.setInterval(300)
        self.timer.timeout.connect(self.onTimerUpdate)

        self.connectReferee()

    ### Tile coloration tests
    def updateMap(self, map) -> None:
        for rowIndex, row in enumerate(map):
            for tileIndex, tile in enumerate(row):
                match tile:
                    case 1:
                        self.arenaWidget.arenaGrid.setTileColor(tileIndex, rowIndex, 255, 55, 223, 122)
                    case 2:
                        self.arenaWidget.arenaGrid.setTileColor(tileIndex, rowIndex, 0, 125, 153, 122)
            # match player["team"]:
            #     case 1:
            #         self.arenaWidget.arenaGrid.setTileColor(player["x"], player["y"], 255, 55, 223, 122)
            #     case 2:
            #         self.arenaWidget.arenaGrid.setTileColor(player["x"], player["y"], 0, 125, 153, 122)

    #### -- Connexion and game loop methods -- ####
    def connectReferee(self):
        self.timer.start()

        self.player = MyPainter("🍉 joueur1", ARENA, USERNAME, PASSWORD, SERVER, PORT)

    def onTimerUpdate(self):
        self.player.gameLoopActions()
        currentMap = self.player.scanNearbyTiles()

        print(self.player.scanNearbyPlayers())

        arenaInfos = self.player.getArenaInfos()

        self.updateMap(currentMap)

######
######

app = QApplication(sys.argv)
# screenSize = app.desktop().availableGeometry().size()
screenSize = QSize(1470, 860)
# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Import styling
with open(os.path.join(CURR_DIR, 'appStyle.qss'), 'r') as styleFile:
    appStyle = styleFile.read()
    app.setStyleSheet(appStyle)

# Start the event loop.
app.exec()

# Your application won't reach here until you exit and the event
# loop has stopped.