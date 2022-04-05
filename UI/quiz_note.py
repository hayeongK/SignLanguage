from PyQt5.QtWidgets import *
from PyQt5 import uic

from instance import Instance

form_note = uic.loadUiType("./UI/quiz_note.ui")[0]


class NoteWindow(QDialog, QWidget, form_note):
    def __init__(self):
        super(NoteWindow, self).__init__()
        self.initUi()
        # self.show()
        # self.showMaximized()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_quiz.clicked.connect(self.btn_quiz_function)
        self.btn_mode.clicked.connect(self.btn_mode_function)

    def initUi(self):
        self.setupUi(self)

    def btn_learing_function(self):
        Instance.window.changeWindow("note", "learning")

    def btn_quiz_function(self):
        Instance.window.changeWindow("note", "cate")

    def btn_mode_function(self):
        Instance.window.changeWindow("note", "mode")
