from telegram_main import main, dirname
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox, QWidget
import sys
import threading
import os


class TrayApplication(QMainWindow):
    def __init__(self):
        super(TrayApplication, self).__init__()
        # Adding an icon
        self.icon = QIcon(os.path.join(dirname, "icon.png"))
        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)

        # Creating the options
        self.menu = QMenu()

        self.option1 = QAction("info")
        self.quit = QAction("quit")

        self.menu.addAction(self.option1)
        self.menu.addAction(self.quit)

        self.option1.triggered.connect(lambda: self.show_message())
        self.quit.triggered.connect(lambda: QCoreApplication.exit())

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("Post to TelegramBot app")
        self.tray.setVisible(True)
        self.tray.sgow()

    @staticmethod
    def show_message():
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Info")
        msg.setText("Telegram Bot made by Kostiantyn Vasko\n"
                    "main functionality it's notifications to telegram.")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


def gui():
    app = QApplication([])
    app.setQuitOnLastWindowClosed(False)
    _ = TrayApplication()
    # application.show()
    sys.exit(app.exec())


def main_app():
    main_trd = threading.Thread(target=main)
    gui_trd = threading.Thread(target=gui)

    main_trd.start()
    gui_trd.start()


if __name__ == '__main__':
    main_app()
