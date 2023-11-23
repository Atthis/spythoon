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
# from pathlib import Path
# Define current path for assets
# CURR_DIR = Path(__file__).resolve().parent
# LIB_DIR = CURR_DIR.resolve().parent.parent
# sys.path.append(LIB_DIR)
# SRC_DIR = os.path.join(LIB_DIR, 'src', 'server')
# sys.path.append(SRC_DIR)
# print(SRC_DIR)

LIB_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(LIB_DIR)
SRC_DIR = os.path.join(LIB_DIR , 'src')
sys.path.append(SRC_DIR)

from utils import BgSetter
from arenaWidget import ArenaWidget
from src.server.referee import Referee
from src.server.utils import secondsToMinutesSeconds

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
        infosWidget = QWidget(uiWidget, objectName = "infosWidget")
        # infosWidget.setMinimumHeight(300)
        infosLayout = QHBoxLayout(infosWidget, objectName = "infosLayout")
        infosLayout.setSpacing(100)
        infosLayout.addWidget(QLabel("Team #1", objectName = "team1Infos"))
        infosLayout.addWidget(QLabel("05:00", objectName = "timeInfos"))
        infosLayout.addWidget(QLabel("Team #2", objectName = "team2Infos"))

        # Arena init
        arenaWidget = ArenaWidget(uiWidget)

        # Scores widget
        scoreWidget = QWidget(uiWidget, objectName = "scoreWidget")
        scoreLayout = QHBoxLayout(scoreWidget, objectName = "scoreLayout")
        scoreWidget.setLayout(scoreLayout)
        scoreLayout.setSpacing(300)
        scoreLayout.addWidget(QLabel("00.00", objectName = "Team1Score"))
        scoreLayout.addWidget(QLabel("00.00", objectName = "Team2Score"))
            
        uiLayout.addWidget(infosWidget, 0, 0, Qt.AlignCenter)
        uiLayout.addWidget(arenaWidget, 1, 0, Qt.AlignCenter)
        uiLayout.addWidget(scoreWidget, 2, 0, Qt.AlignCenter)

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

    def connectReferee(self):
        self.timer.start()

        self.referee = Referee(ARBITRE, ARENA, USERNAME, PASSWORD, SERVER, PORT, DURATION)
        # # Reset arena
        # referee.openArena(True)
        self.referee.resetArena()
        self.referee.update()
        time.sleep(3)
        self.referee.update()

        # # Set Referee map to Arena map
        self.referee.setRefereeMap(self.referee.getGameInfos()["map"])
        self.referee.update()
        time.sleep(0.3)

        # # Define arena rules from the json
        self.referee.setArenaRules(serverRulesdict)
        self.referee.update()
        time.sleep(1)

        # # Create players and their rules from the json
        self.referee.createPlayers(serverRulesdict)
        self.referee.update()
        time.sleep(0.3)

        self.referee.printInfoToArena("⌛ En attente des joueurs ...")
        self.referee.update()
        time.sleep(10)
        ### TODO Wait for all players to connect 
        readyPlayers = []

        while len(readyPlayers) < len(self.referee.getCurrentRange()):
            self.referee.update()
            time.sleep(0.3)
            for player in self.referee.getCurrentRange().values():
                if not player["idle"]:
                    if player["clientId"] not in readyPlayers :
                        readyPlayers.append(player["clientId"])
            print(readyPlayers)

        # # Launch party msg
        self.referee.printInfoToArena("🟢 C'est parti !")
        self.referee.update()
        time.sleep(2)

        # # Timer and scores msg
        self.referee.printInfoToArena(f"| ⏰ {secondsToMinutesSeconds(DURATION)} | 👑 🍉 Fuschia : {self.referee.getTeamsScores()[0]} / 🫐 Turquoise : {self.referee.getTeamsScores()[1]}.")
        self.referee.update()
        time.sleep(0.3)

        # # Request current timestamp
        self.referee.startTimeMaster()

        self.referee.setOldRange(self.referee.getCurrentRange())

    def onTimerUpdate(self):
        print(self.referee.getCurrentRange())
        # #  referee direction changes to apply updates
        self.referee.rotate((self.referee.getDir()+1)%4)

        # # For each player
        for player in self.referee.getCurrentRange().values():
            # Set profile
            self.referee.setPlayerProfileOnFire(player)

            # If fire and ammo
            if self.referee.getCurrentRange()[player["clientId"]]["nFire"] > self.referee.getOldRange()[player["clientId"]]["nFire"]:
                # Update tile status
                self.referee.updateRefereeMap(player["x"], player["y"], player["team"])
                # Update teams score
                self.referee.updateScores(self.referee.getRefereeMap())
                # Decrease player ammo
                self.referee.decreasePlayerAmmo(player)
                # Push new map state to the server
                self.referee.updateArenaMap()

        # # Calcul remaining time and Update arena info with new time and scores
        self.referee.printInfoToArena(f"| ⏰ {secondsToMinutesSeconds(self.referee.getRemainingTime())} | 👑 🍉 Fuschia : {self.referee.getTeamsScores()[0]} / 🫐 Turquoise : {self.referee.getTeamsScores()[1]}.")

        # # Sent all requests to server
        self.referee.update()

        if self.referee.isGameOver() :
            self.referee.printInfoToArena(f"| 🔔 PARTIE TERMINEE ! | 👑 🍉 Fuschia : {self.referee.getTeamsScores()[0]} / 🫐 Turquoise : {self.referee.getTeamsScores()[1]}.")
            self.referee.update()
            self.timer.stop()

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