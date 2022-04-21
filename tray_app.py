from telegram_main import main
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox
import sys
import threading


class TrayApplication(QMainWindow):
    def __init__(self):
        super(TrayApplication, self).__init__()
        # Adding an icon
        self.icon = QIcon("icon.png")

        # Adding item on the menu bar
        self.tray = QSystemTrayIcon()
        self.tray.setIcon(self.icon)
        self.tray.setVisible(True)

        # Creating the options
        self.menu = QMenu()
        self.option1 = QAction("info")
        self.quit = QAction("quit")

        self.menu.addAction(self.option1)
        self.menu.addAction(self.quit)

        self.option1.triggered.connect(lambda: self.show_message())
        self.quit.triggered.connect(quit)

        # Adding options to the System Tray
        self.tray.setContextMenu(self.menu)
        self.tray.setToolTip("Post to TelegramBot app")

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
    sys.exit(app.exec())


def main_app():
    main_trd = threading.Thread(target=main)
    gui_trd = threading.Thread(target=gui)

    main_trd.start()
    gui_trd.start()


if __name__ == '__main__':
    main_app()
