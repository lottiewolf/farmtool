# This Python file uses the following encoding: utf-8

import sys
from PySide6.QtWidgets import (QApplication)
from config.ConfigFarm import ConfigFarm
from ui.MainWindow import MainWindow

if __name__ == "__main__":
    app = QApplication([])

    farm_config = ConfigFarm.instance()
    farm_config.load()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

