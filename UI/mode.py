from PyQt5.QtWidgets import *
from PyQt5 import uic
from UI.wordInfo import WordInfo

from instance import Instance

form_mode = uic.loadUiType("./UI/mode.ui")[0]


# class ModeWindow(QMainWindow, form_mode):
class ModeWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_mode1.clicked.connect(self.move_mode1)
        self.btn_mode2.clicked.connect(self.move_mode2)

    def move_mode1(self):
        WordInfo.mode = 0
        self.move_mode()

    def move_mode2(self):
        WordInfo.mode = 1
        self.move_mode()

    def move_mode(self):
        WordInfo.cate = 0
        Instance.window.changeWindow("mode", "learning")
