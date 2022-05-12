# This Python file uses the following encoding: utf-8

from PySide6.QtWidgets import (QApplication)
from farmtool.config.config_farm import ConfigFarm
from farmtool.ui.main_window import MainWindow
import sys

def run():
    app = QApplication([])

    settings = ConfigFarm.instance()
    settings.load()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run()


