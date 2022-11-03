import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import QApplication, QDesktopWidget, QLabel, QMainWindow, QWidget


class LoadingScreen(QWidget):
    def __init__(self, window_size=[]):
        super().__init__()
        self.setWindowFlags(
            Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFixedSize(200, 200)
        self.label_animation = QLabel(self)
        self.movie = QMovie("assets/gui/loading.gif")
        self.label_animation.setMovie(self.movie)
        self.init_ui()

    def init_ui(self) -> None:
        self.animation()
        self.show()

    def animation(self, ms=500) -> None:
        timer = QTimer(self)
        self.start_animation()
        timer.singleShot(ms, self.stop_animation)

    def start_animation(self) -> None:
        self.movie.start()

    def stop_animation(self) -> None:
        self.movie.stop()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_title = "App title"
        self.app_icon = "assets/gui/logo.png"
        self.app_window_size = [550, 500]
        self.loading_screen = LoadingScreen(window_size=self.app_window_size)
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
        pass

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
    app = QApplication(sys.argv)
    main_window = MainWindow()
    sys.exit(app.exec_())
