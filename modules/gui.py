import sys

from PyQt5.QtCore import QObject, Qt, QThread, QTimer, pyqtSignal
from PyQt5.QtGui import QIcon, QMovie
from PyQt5.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QDesktopWidget,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)


class BotWorker(QObject):
    finished = pyqtSignal()

    def run(self) -> None:
        self.finished.emit()


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


class MainPage(QWidget):
    def __init__(self):
        super().__init__()
        self.elems = {}
        self.setting_elems = {}
        self.set_layout()

    def set_layout(self) -> None:
        layout = QGridLayout()
        self.elems = {
            "settings": (self.layout_settings(), 0, 0, 1, 2),
            "log_box": (QGroupBox(""), 1, 0, 1, 2),
            "btn_on": (QPushButton("Start"), 2, 0),
            "btn_off": (QPushButton("Stop"), 2, 1),
            "btn_calibrate": (QPushButton("Calibrate"), 3, 0, 1, 2),
        }
        # Styles for elements
        self.elems["settings"][0].setStyleSheet(self.settings_styles())
        self.elems["log_box"][0].setStyleSheet(self.log_box_styles())
        [
            btn[0].setStyleSheet(self.btn_styles())
            for k, btn in self.elems.items()
            if "btn" in k
        ]
        [layout.addWidget(*elem) for k, elem in self.elems.items()]
        self.setLayout(layout)

    def layout_settings(self) -> dict:
        """GroupBox - раздел настройки"""
        combo = QComboBox()
        combo.addItems(["Страж"])
        self.setting_elems = {
            "camp": QCheckBox("Палатка"),
            "maid": QCheckBox("Горничные"),
            "char": combo,
        }
        settings = QGroupBox("Настройки")
        settings_hbox = QHBoxLayout()
        settings.setLayout(settings_hbox)
        [settings_hbox.addWidget(elem) for k, elem in self.setting_elems.items()]
        return settings

    def settings_styles(self) -> str:
        """Стили для settings GroupBox"""
        styles = """
            font-size: 16px;
            max-height: 70px;
        """
        return styles

    def btn_styles(self) -> str:
        """Стили для основых кнопок"""
        styles = """
            height: 40px;
            font-size: 18px;
            color: white;
            background-color: #263238;
            border: none;
        """
        return styles

    def log_box_styles(self) -> str:
        styles = """
            font-size: 16px;
            background-color: white;
        """
        return styles


class ActivationPage(QWidget):
    def __init__(self):
        super().__init__()
        self.set_layout()

    def set_layout(self) -> None:
        layout = QFormLayout()
        layout.setFormAlignment(Qt.AlignCenter)
        layout.addRow(QLabel("Введите код активации"))
        layout.addRow(QLineEdit())
        layout.addRow(QPushButton("Активировать"))
        layout.addRow(QPushButton("Купить код"))
        self.setLayout(layout)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_title = "БДО"
        self.app_icon = "assets/gui/logo.png"
        self.app_window_size = [500, 550]
        self.elems = {}
        self.init_ui()
        print(self.elems)

    def run_long_task(self) -> None:
        # Create QThread/Worker object
        self.thread = QThread()
        self.worker = BotWorker()
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Start the thread
        self.thread.start()
        # Final resets
        self.longRunningBtn.setEnabled(False)

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

    def switch_page(self):
        self.stacked_layout.setCurrentIndex(self.page_combo.currentIndex())

    def set_layout(self) -> None:
        # central widget
        wid = QWidget(self)
        self.setCentralWidget(wid)
        # Create a top-level layout
        layout = QVBoxLayout()
        # Create and connect the combo box to switch between pages
        self.page_combo = QComboBox()
        self.page_combo.addItems(["Бот", "Активация"])
        self.page_combo.activated.connect(self.switch_page)
        # Create the stacked layout
        self.stacked_layout = QStackedLayout()
        # Create the first page
        self.main_page = MainPage()
        self.elems.update(self.main_page.elems)
        self.elems.update(self.main_page.setting_elems)
        self.stacked_layout.addWidget(self.main_page)
        # Create the second page
        self.activation_page = ActivationPage()
        self.stacked_layout.addWidget(self.activation_page)
        # Add the combo box and the stacked layout to the top-level layout
        layout.addWidget(self.page_combo)
        layout.addLayout(self.stacked_layout)

        wid.setLayout(layout)

    def set_main_styles(self) -> None:
        """Основные стили"""
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
