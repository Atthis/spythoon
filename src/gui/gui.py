from random import choice, randint
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QGridLayout, QStackedLayout
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

        mainWindow = QWidget(objectName = "mainWindow")
        layout = QGridLayout(mainWindow)
        mainWindow.setLayout(layout)

        arenaWidget = ArenaWidget(mainWindow)
        layout.addWidget(arenaWidget, 0, 0, Qt.AlignCenter)

        # mainContainer = QWidget(objectName = "mainContainer")
        # layout = QStackedLayout(mainContainer, objectName = "VertLay")
        # # layout = QGridLayout(mainContainer, objectName = "VertLay")
        # mainContainer.setLayout(layout)

        # arenaBg = ArenaBg(1300, 600, 'bgArena.jpg', mainContainer)
        # arenaGrid = ArenaGrid('arena', 12, 26, Tile, 50, mainContainer)

        # layout.insertWidget(0, arenaBg)
        # layout.insertWidget(1, arenaGrid)
        # layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        # layout.setCurrentIndex(1)

        # arenaGrid.setTileColor(3, 1, 150, 150, 0, 255)
        # arenaGrid.setTileColor(2, 2, 150, 150, 0, 255)
        # arenaGrid.setTileColor(1, 3, 150, 150, 0, 255)
        # arenaGrid.setTileColor(24, 8, 0, 0, 150, 255)
        # arenaGrid.setTileColor(23, 9, 0, 0, 150, 255)
        # arenaGrid.setTileColor(22, 10, 0, 0, 150, 255)

        # ######
        # # CORRIGER CET ELEMENT ⇒ ON A PLUS ACCES A ITEMATPOSITION CAR ARENA N'EST PLUS UN LAYOUT MAIS UN WIDGET
        # ######
        # # spawnAreas = [arena.itemAtPosition(1, 3).widget(), arena.itemAtPosition(2,2).widget(), arena.itemAtPosition(3,1).widget(), arena.itemAtPosition(8, 24).widget(), arena.itemAtPosition(9,23).widget(), arena.itemAtPosition(10, 22).widget()]
        # # for area in spawnAreas:
        # #     area.setColor(0, 0, 0)
        
        # print('============')        

        # # layout.addWidget(arena, 1, 0, Qt.AlignCenter)
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