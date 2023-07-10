from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from instance import Instance
from UI.result import Result

form_note = uic.loadUiType("./UI/quiz_cate.ui")[0]


class CateWindow(QDialog, QWidget, form_note):
    def __init__(self):
        super(CateWindow, self).__init__()
        self.initUi()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_start.clicked.connect(self.btn_quiz_function)

        self.btn_cates = [self.btn_cate01, self.btn_cate02, self.btn_cate03, self.btn_cate04, self.btn_cate05, self.btn_cate06, self.btn_cate07, self.btn_cate08,
                          self.btn_cate09, self.btn_cate10, self.btn_cate11, self.btn_cate12, self.btn_cate13, self.btn_cate14, self.btn_cate15, self.btn_cate16]
        self.btn_cate_funcs = [self.btn_cate_function01, self.btn_cate_function02, self.btn_cate_function03, self.btn_cate_function04, self.btn_cate_function05, self.btn_cate_function06, self.btn_cate_function07, self.btn_cate_function08,
                               self.btn_cate_function09, self.btn_cate_function10, self.btn_cate_function11, self.btn_cate_function12, self.btn_cate_function13, self.btn_cate_function14, self.btn_cate_function15, self.btn_cate_function16]
        for c in range(len(self.btn_cates)):
            self.btn_cates[c].clicked.connect(self.btn_cate_funcs[c])
            self.set_icon(c)

    def initUi(self):
        self.setupUi(self)

    def set_icon(self, i):  # 카테고리 아이콘
        height = Result.height / 20
        pixmap = QPixmap("./UI/icon/menu_icon{}.png".format(i+1))
        pixmap = pixmap.scaledToHeight(height)

        icon = QIcon()  # QIcon 생성
        icon.addPixmap(pixmap)  # 아이콘에 이미지 설정

        self.btn_cates[i].setIcon(icon)
        self.btn_cates[i].setIconSize(QSize(height, height))

    def btn_quiz_function(self):
        Instance.changeWindow("quiz2")

    def btn_learing_function(self):
        Instance.changeWindow("learning")

    def btn_cate_function01(self):
        Result.cate = 0

    def btn_cate_function02(self):
        Result.cate = 1

    def btn_cate_function03(self):
        Result.cate = 2

    def btn_cate_function04(self):
        Result.cate = 3

    def btn_cate_function05(self):
        Result.cate = 4

    def btn_cate_function06(self):
        Result.cate = 5

    def btn_cate_function07(self):
        Result.cate = 6

    def btn_cate_function08(self):
        Result.cate = 7

    def btn_cate_function09(self):
        Result.cate = 8

    def btn_cate_function10(self):
        Result.cate = 9

    def btn_cate_function11(self):
        Result.cate = 10

    def btn_cate_function12(self):
        Result.cate = 11

    def btn_cate_function13(self):
        Result.cate = 12

    def btn_cate_function14(self):
        Result.cate = 13

    def btn_cate_function15(self):
        Result.cate = 14

    def btn_cate_function16(self):
        Result.cate = 15
