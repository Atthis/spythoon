from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPalette , QBrush, QPixmap

# Only needed for access to command line arguments
import os
from pathlib import Path

class BgSetter(QWidget):
    """
    Class for creating the background of a widget
    """
    def __init__(self, name: str | None, img:str, currDir : Path, width : int, height : int, parent: QWidget | None = ...) -> None:
        super().__init__(parent)

        self.objectName = name
        self.setAutoFillBackground(True)

        # Background definition        
        pixmap = QPixmap(os.fspath(currDir / "assets" / img))
        palette = self.palette()
        brush = QBrush(pixmap.scaled(width, height, Qt.IgnoreAspectRatio))
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)