from random import choice, randint
import typing
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QSize, Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QWidget, QGridLayout, QStackedLayout
from PyQt5.QtGui import QPalette , QColor, QBrush, QImage, QPixmap

# Only needed for access to command line arguments
import sys
import os
from pathlib import Path
# Define current path for assets
CURR_DIR = Path(__file__).resolve().parent

# TILE CLASS, SUBELEMENT OF THE ARENA GRID CLASS
class Tile(QWidget):
    def __init__(self, name:str, sideSize:int, parent: QWidget | None = ...):
        super().__init__(parent)

        self.objectName = name
        self.setAutoFillBackground(True)
        self.setFixedSize(sideSize, sideSize)

    def setColor(self, r:int, g:int, b:int, a:int = 255):
        """
        Define tile color based on rgb values
        """
        palette = self.palette()
        color = QColor(r, g, b)
        color.setAlpha(a)
        palette.setColor(QPalette.Window, color)
        self.setPalette(palette)
    
    # Mouse event coloration test
    # def mouseReleaseEvent(self, e) -> None:
    #     if e.button() == Qt.LeftButton:
    #         if self.palette().color(QPalette.Window).name(QColor.HexArgb) == '#00ffffff':
    #             self.setColor(0, 0, 0, 255)
    #         else :
    #             self.setColor(255, 255, 255, 0)



# ARENA GRID CLASS TO MANAGE PAINTED TILES BY TEAMS
class ArenaGrid(QWidget):
    def __init__(self, row:int, col:int, widget:QWidget, sideSize:int, parent: QWidget | None = ...) -> None:
        super().__init__()

        self.objectName = 'arenaGrid'
        self.parent = parent
        self.setFixedSize(QWidget.minimumSize(self))

        # Layout settings
        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self.setGrid(row, col, widget, sideSize)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0, 0, 0)
        self.adjustSize() # Redraw the widget to fit size with all tiles
    
    def setGrid(self, row:int, col:int, widget:QWidget, sideSize:int):
        """
        Set arena grid with inputs rows and columns number, and populate the grid with the specified widget
        """
        for i in  range(0, row):
            for j in range(0, col):
                tile =  widget(f"{i}{j}", sideSize, self)
                tile.setColor(255, 255, 255, 0)
                self._layout.addWidget(tile, i, j)

    def setTileColor(self, posX:int, posY:int, r:int, g:int, b:int, a:int):
        self._layout.itemAtPosition(posY, posX).widget().setColor(r, g, b, a)


# ARENA BACKGROUND CLASS TO DISPLAY THE ARENA BACKGROUND
class ArenaBg(QWidget):
    def __init__(self, width:int, height:int, img:str, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.objectName = 'arenaBackground'
        self.setFixedSize(width, height)
        self.setAutoFillBackground(True)

        pixmap = QPixmap(os.fspath(CURR_DIR / img))
        palette = self.palette()
        brush = QBrush(pixmap.scaled(width, height, Qt.IgnoreAspectRatio))
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)


# GLOBAL ARENA WIDGET
class ArenaWidget(QWidget):
    def __init__(self, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.objectName = 'arenaWidget'
        # mainContainer = QWidget(self, objectName = "mainContainer")
        # layout = QStackedLayout(mainContainer, objectName = "mainLayout")
        layout = QStackedLayout(self, objectName = "mainLayout")
        self.setLayout(layout)

        arenaBg = ArenaBg(1300, 600, 'bgArena.jpg', self)
        arenaGrid = ArenaGrid(12, 26, Tile, 50, self)

        layout.insertWidget(0, arenaBg)
        layout.insertWidget(1, arenaGrid)
        layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        layout.setCurrentIndex(1)

        arenaGrid.setTileColor(3, 1, 150, 150, 0, 255)
        arenaGrid.setTileColor(2, 2, 150, 150, 0, 255)
        arenaGrid.setTileColor(1, 3, 150, 150, 0, 255)
        arenaGrid.setTileColor(24, 8, 0, 0, 150, 255)
        arenaGrid.setTileColor(23, 9, 0, 0, 150, 255)
        arenaGrid.setTileColor(22, 10, 0, 0, 150, 255)

        # self.setFixedSize(QWidget.minimumSize(self))
        # self.adjustSize()
        
        # self.setCentralWidget(self)