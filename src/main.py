import sys

from PySide6.QtWidgets import QApplication

from controllers.sorteo import SorteoController
from views.sorteo import Sorteo


class App(QApplication):
    def __init__(self):
        QApplication.__init__(self, sys.argv)

    def start(self):
        self.show_main_window()
        sys.exit(app.exec())

    def show_main_window(self):
        self.view = Sorteo()
        self.view.show()


if __name__ == "__main__":
    app = App()
    app.start()
