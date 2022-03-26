# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QApplication)
from config.config_farm import ConfigFarm
from ui.main_window import MainWindow
import sys

if __name__ == "__main__":
    app = QApplication([])

    settings = ConfigFarm.instance()
    settings.load()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

