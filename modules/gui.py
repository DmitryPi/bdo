import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDesktopWidget,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
)


class LoadingScreen(QWidget):
    def __init__(self, duration_ms=500):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 200)
        self.duration_ms = duration_ms
        self.label_animation = QLabel(self)
        self.movie = QMovie("assets/gui/loading.gif")
        self.label_animation.setMovie(self.movie)
        self.init_ui()

    def init_ui(self) -> None:
        self.animation()
        self.show()

    def animation(self) -> None:
        timer = QTimer(self)
        self.start_animation()
        timer.singleShot(self.duration_ms, self.stop_animation)

    def start_animation(self) -> None:
        self.movie.start()

    def stop_animation(self) -> None:
        self.movie.stop()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_title = "БДО"
        self.app_icon = "assets/gui/logo.png"
        self.app_window_size = [500, 550]
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

    def set_layout(self) -> None:
        # central widget
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # settings
        combo = QComboBox()
        combo.addItems(["Страж"])
        setting_elems = {
            "camp": QCheckBox("Палатка"),
            "maid": QCheckBox("Горничные"),
            "char": combo,
        }
        settings = QGroupBox("Настройки")
        settings_hbox = QHBoxLayout()
        settings.setLayout(settings_hbox)
        [settings_hbox.addWidget(elem) for k, elem in setting_elems.items()]
        # Layout elements
        elems = {
            "settings": (settings, 0, 0, 1, 2),
            "log_box": (QGroupBox(""), 1, 0, 1, 2),
            "btn_on": (QPushButton("Start"), 2, 0),
            "btn_off": (QPushButton("Stop"), 2, 1),
            "btn_calibrate": (QPushButton("Calibrate"), 3, 0, 1, 2),
        }
        # Element styles
        elems["settings"][0].setStyleSheet(
            """
            font-size: 16px;
            max-height: 70px;
        """
        )
        elems["log_box"][0].setStyleSheet(
            """
            font-size: 16px;
            background-color: white;
        """
        )
        [
            btn[0].setStyleSheet(
                """
                height: 40px;
                font-size: 18px;
                text-transform: uppercase;
                color: white;
                background-color: #263238;
                border: none;
            """
            )
            for k, btn in elems.items()
            if "btn" in k
        ]
        # log combobox
        # layout
        layout = QGridLayout()
        [layout.addWidget(*elem) for k, elem in elems.items()]
        wid.setLayout(layout)

    def set_main_styles(self) -> None:
        """Set styles for main frame/bars"""
        # self.setStyleSheet('background-color: #121212; color: white;')
        self.statusBar().setStyleSheet(
            """
            background-color: #23282A;
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
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec())
