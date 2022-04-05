from PyQt5.QtWidgets import *
from PyQt5 import uic

from instance import Instance
from UI.wordInfo import WordInfo

form_note = uic.loadUiType("./UI/quiz_cate.ui")[0]


class CateWindow(QDialog, QWidget, form_note):
    def __init__(self):
        super(CateWindow, self).__init__()
        self.initUi()
        # self.show()
        # self.showMaximized()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_start.clicked.connect(self.btn_quiz_function)
        self.listWidget.itemClicked.connect(self.chkItemClicked)

    def initUi(self):
        self.setupUi(self)

    def chkItemClicked(self):
        # print(self.listWidget.currentItem().text())
        return

    def btn_quiz_function(self):
        if WordInfo.mode == 0:
            Instance.window.changeWindow("cate", "quiz")
        else:
            Instance.window.changeWindow("cate", "quiz2")

    def btn_learing_function(self):
        Instance.window.changeWindow("cate", "learning")
