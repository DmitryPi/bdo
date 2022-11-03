import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication,
    QDesktopWidget,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
)


class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_title = "App title"
        self.app_icon = "assets/gui/logo.png"
        self.app_window_size = [550, 500]
        self.init_ui()

    def init_ui(self) -> None:
        # window
        self.set_window(size=self.app_window_size)
        # status
        self.set_statusbar()
        # styles
        self.set_main_styles()
        # layout
        self.set_layout()
        # show
        self.show()

    def start_program(self):
        print("started program")

    def pause_program(self):
        print("pause program")

    def create_vbox(self, align="top") -> QVBoxLayout:
        """Build vertical box with alignment"""
        alignments = {
            "top": Qt.AlignTop,
            "center": Qt.AlignCenter,
            "bottom": Qt.AlignBottom,
        }
        vbox = QVBoxLayout()
        vbox.setAlignment(alignments[align])
        return vbox

    def create_hbox(self, *args, **kwargs) -> QHBoxLayout:
        hbox = QHBoxLayout(*args, **kwargs)
        return hbox

    def set_layout(self) -> None:

        button = QPushButton("Click me!")
        text = QLabel("Hello World", alignment=Qt.AlignCenter)

        layout = QVBoxLayout(self)
        layout.addWidget(text)
        layout.addWidget(button)

    def set_main_styles(self) -> None:
        """Set styles for main frame/bars"""
        # self.setStyleSheet('background-color: #121212; color: white;')
        self.statusBar().setStyleSheet(
            """
            background-color: #181818;
            color: white;
        """
        )

    def set_window(self, size=[550, 500]) -> None:
        """Set window default title/icon/size/position"""
        self.setWindowTitle(self.app_title)
        self.setWindowIcon(QIcon(self.app_icon))
        self.set_window_size(size=size)
        self.set_window_center()

    def set_window_size(self, size=[550, 500]) -> None:
        self.resize(*size)
        self.setFixedSize(self.size())

    def set_window_center(self) -> None:
        window_rect = self.frameGeometry()  # app window rect
        window_coords = (
            QDesktopWidget().availableGeometry().center()
        )  # screen center x,y
        window_rect.moveCenter(window_coords)
        self.move(window_rect.topLeft())  # move app rect to screen center

    def set_statusbar(self, msg="Ready") -> None:
        self.statusBar().showMessage(msg)


if __name__ == "__main__":
    qt_app = QApplication(sys.argv)
    ex = MainApp()
    sys.exit(qt_app.exec_())
