from random import choice, randint
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QGridLayout, QHBoxLayout
from PyQt5.QtGui import QPalette , QColor, QBrush, QImage, QPixmap

from arenaWidget import ArenaWidget

# Only needed for access to command line arguments
import sys
import os
from pathlib import Path
# Define current path for assets
CURR_DIR = Path(__file__).resolve().parent

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Mon app")  

        palette = self.palette()
        color = QColor(255, 255, 255)
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)

        mainWindow = QWidget(self, objectName = "mainWindow")
        layout = QGridLayout(mainWindow, objectName = "test")
        mainWindow.setLayout(layout)

        # Infos widget : teams colors/numbers and timer
        infosWidget = QWidget(mainWindow, objectName = "infosWidget")
        # infosWidget.setMinimumHeight(300)
        infosLayout = QHBoxLayout(infosWidget, objectName = "infosLayout")
        infosLayout.setSpacing(100)
        infosLayout.addWidget(QLabel("Team 1", objectName = "team1Infos"))
        infosLayout.addWidget(QLabel("05:00", objectName = "timeInfos"))
        infosLayout.addWidget(QLabel("Team 2", objectName = "team2Infos"))

        # Arena init
        arenaWidget = ArenaWidget(mainWindow)

        # Scores widget
        scoreWidget = QWidget(mainWindow, objectName = "scoreWidget")
        scoreLayout = QHBoxLayout(scoreWidget, objectName = "scoreLayout")
        scoreWidget.setLayout(scoreLayout)
        scoreLayout.setSpacing(300)
        scoreLayout.addWidget(QLabel("00.00", objectName = "Team1Score"))
        scoreLayout.addWidget(QLabel("00.00", objectName = "Team2Score"))
        
            
        layout.addWidget(infosWidget, 0, 0, Qt.AlignCenter)
        layout.addWidget(arenaWidget, 1, 0, Qt.AlignCenter)
        layout.addWidget(scoreWidget, 2, 0, Qt.AlignCenter)

        self.setCentralWidget(mainWindow)

    def mousePressEvent(self, e) -> None:
        self.setWindowTitle('MOUSE PRESS event')

    def mouseReleaseEvent(self, e) -> None:
        self.setWindowTitle('MOUSE RELEASE event')

######
######

app = QApplication(sys.argv)
# screenSize = app.desktop().availableGeometry().size()
screenSize = QSize(1600, 800)
# Create a Qt widget, which will be our window.
window = MainWindow()
window.show()  # IMPORTANT!!!!! Windows are hidden by default.

# Start the event loop.
app.exec()


# Your application won't reach here until you exit and the event
# loop has stopped.