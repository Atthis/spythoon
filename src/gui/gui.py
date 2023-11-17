from random import choice, randint
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QVBoxLayout, QGridLayout, QLayout
from PyQt5.QtGui import QPalette , QColor, QBrush, QImage, QPixmap

# Only needed for access to command line arguments
import sys
import os
from pathlib import Path

CURR_DIR = Path(__file__).resolve().parent

# TILE CLASS, SUBELEMENT OF THE ARENA GRID CLASS
class Tile(QWidget):
    def __init__(self, name:str, width, height):
        super().__init__()

        self.objectName = name
        self.setAutoFillBackground(True)
        self.setFixedSize(width, height)

    def setColor(self, r:int, g:int, b:int, a:int = 255):
        """
        Define tile color based on rgb values
        """
        palette = self.palette()
        color = QColor(r, g, b)
        color.setAlpha(a)
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)


# ARENA GRID CLASS TO MANAGE PAINTED TILES BY TEAMS
# class ArenaGrid(QGridLayout):
class ArenaGrid(QWidget):
    def __init__(self, name:str, row:int, col:int, widget:QWidget, widgetW, widgetH) -> None:
        super().__init__()

        self.objectName = name
        # self.setFixedSize(1300, 600)
        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self.setGrid(row, col, widget, widgetW, widgetH)
        self.setLayout(self._layout)
        self.setContentsMargins(0,0, 0, 0)
        self.adjustSize()
    
    def setGrid(self, row:int, col:int, widget:QWidget, widgetW, widgetH):
        """
        Set arena grid with inputs rows and columns number, and populate the grid with the specified widget
        """
        for i in  range(0, row):
            for j in range(0, col):
                tile =  widget(f"{i}{j}", widgetW, widgetH)
                tile.setColor(180, 50, 150, 100)
                self._layout.addWidget(tile, i, j)

# ARENA BACKGROUND CLASS TO DISPLAY THE ARENA BACKGROUND
class ArenaBg(QWidget):
    def __init__(self, width, height, img) -> None:
        super().__init__()

        self.setFixedSize(width, height)
        self.setAutoFillBackground(True)
        self.setContentsMargins(0, 0, 0, 0)

        pixmap = QPixmap(os.fspath(CURR_DIR / img))
        palette = self.palette()
        brush = QBrush(pixmap.scaled(width, height, Qt.IgnoreAspectRatio))
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)





class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()

        self.setWindowTitle("Mon app")        
        layout = QGridLayout(objectName = "VertLay")

        mainContainer = QWidget(objectName = "mainContainer")
        mainContainer.setLayout(layout)

        arena = ArenaGrid('arena', 12, 26, Tile, 50, 50)
        
        ######
        # CORRIGER CET ELEMENT ⇒ ON A PLUS ACCES A ITEMATPOSITION CAR ARENA N'EST PLUS UN LAYOUT MAIS UN WIDGET
        ######
        # spawnAreas = [arena.itemAtPosition(1, 3).widget(), arena.itemAtPosition(2,2).widget(), arena.itemAtPosition(3,1).widget(), arena.itemAtPosition(8, 24).widget(), arena.itemAtPosition(9,23).widget(), arena.itemAtPosition(10, 22).widget()]
        # for area in spawnAreas:
        #     area.setColor(0, 0, 0)
        
        print('============')        

        layout.addWidget(arena, 1, 0, Qt.AlignCenter)
        layout.addWidget(ArenaBg(1300, 200, 'bgArena.jpg'), 2, 0, Qt.AlignCenter)
        self.setCentralWidget(mainContainer)

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