import cv2
from PyQt5.QtCore import Qt


class WindowChanged:
    def __init__(self, screen):
        self.windows = {}
        self.pres_window = "mode"
        self.screen = screen

    def setWindow(self, window_name, window):
        self.windows[window_name.lower()] = window

    def changeWindow(self, window_before, window_name, args=None):
        if self.pres_window == window_name and args is None:
            return

        pres_window = self.windows[self.pres_window]
        # if pres_window == "start":
        #     pres_window.hide()
        # else:
        #     pres_window.close()
        pres_window.close()
        target_window = self.windows[window_name]
        if window_name == "word":
            target_window.setWord()
        if window_name == "learning":
            target_window.setWords()

        target_window.setFixedSize(
            self.screen.width(), self.screen.height() - 45)  # 0 -45
        target_window.setWindowFlags(
            Qt.FramelessWindowHint)  # 최대, 최소, 닫기 UI 삭제
        self.pres_window = window_name
        target_window.exec_()
        target_window.showMaximized()  # showMaximized
