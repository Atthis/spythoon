from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QStackedLayout
from PyQt5.QtGui import QPalette , QColor, QBrush, QPixmap
from utils import BgSetter

import os
from pathlib import Path
# Define current path for assets
CURR_DIR = Path(__file__).resolve().parent

# TILE CLASS, SUBELEMENT OF THE ARENA GRID CLASS
class Tile(QWidget):
    """
    Class defining the tile composing the arena map
    """
    def __init__(self, name:str, sideSize:int, parent: QWidget | None = ...) -> None:
        super().__init__(parent)
        self.objectName = name
        self.setAutoFillBackground(True)
        self.setFixedSize(sideSize, sideSize)

    def setColor(self, r:int, g:int, b:int, a:int = 255) -> None:
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
    """
    Class creating a grid for the arena. It uses the tile class to populate the grid, based on a number of rows and columns
    """
    def __init__(self, row:int, col:int, widget:QWidget, sideSize:int, parent: QWidget | None = ...) -> None:
        """
        The init method set the grid, reset margins and adjust the widget size to exactly fit the grid
        """
        super().__init__()

        self.objectName = 'arenaGrid'
        self.parent = parent
        # self.setFixedSize(QWidget.minimumSize(self))

        # Layout settings
        self._layout = QGridLayout()
        self._layout.setSpacing(0)
        self.setGrid(row, col, widget, sideSize)
        self.setLayout(self._layout)
        self._layout.setContentsMargins(0,0, 0, 0)
        self.adjustSize() # Redraw the widget to fit size with all tiles
    
    def setGrid(self, row:int, col:int, widget:QWidget, sideSize:int) -> None:
        """
        Set arena grid with inputs rows and columns number, and populate the grid with the specified widget
        """
        for i in  range(0, row):
            for j in range(0, col):
                tile =  widget(f"{i}{j}", sideSize, self)
                tile.setColor(255, 255, 255, 0)
                self._layout.addWidget(tile, i, j)

    def setTileColor(self, posX:int, posY:int, r:int, g:int, b:int, a:int) -> None:
        """
        Set color for a specific tile based on its position
        """
        self._layout.itemAtPosition(posY, posX).widget().setColor(r, g, b, a)


# GLOBAL ARENA WIDGET
class ArenaWidget(QWidget):
    """
    Class containing all the elements of the local arena: the grid and the background. It overlays the 2 elements so it can reproduce the painting effect of the players on the arena image
    """
    def __init__(self, parent: QWidget | None = ...) -> None:
        """
        After setting basic values for the widget, set the layout and create both the grid and background widgets.
        Insert the 2 widgets in the layout stacked, and define the front layout.
        """
        super().__init__(parent)

        self.objectName = 'arenaWidget'
        layout = QStackedLayout(self, objectName = "mainLayout")
        self.setLayout(layout)

        arenaBg = BgSetter("arenaBg", 'bgArena_v2.jpg', CURR_DIR, 1300, 600, self)
        arenaGrid = ArenaGrid(12, 26, Tile, 50, self)

        layout.insertWidget(0, arenaBg)
        layout.insertWidget(1, arenaGrid)
        layout.setStackingMode(QStackedLayout.StackingMode.StackAll)
        layout.setCurrentIndex(1)

        # Coloring the spawn areas for test
        # arenaGrid.setTileColor(3, 1, 150, 150, 0, 255)
        # arenaGrid.setTileColor(2, 2, 150, 150, 0, 255)
        # arenaGrid.setTileColor(1, 3, 150, 150, 0, 255)
        # arenaGrid.setTileColor(24, 8, 0, 0, 150, 255)
        # arenaGrid.setTileColor(23, 9, 0, 0, 150, 255)
        # arenaGrid.setTileColor(22, 10, 0, 0, 150, 255)