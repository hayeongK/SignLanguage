from PyQt5.QtWidgets import *
from PyQt5 import uic
from UI.wordInfo import WordInfo
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from instance import Instance
from UI.result import Result

form_mode = uic.loadUiType("./UI/mode.ui")[0]


class ModeWindow(QDialog, QWidget, form_mode):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_mode1.clicked.connect(self.move_mode1)
        self.btn_mode2.clicked.connect(self.move_mode2)

        # 그림
        height = Result.height / 5*2
        pixmap = QPixmap("./UI/icon/mode.png")
        pixmap = pixmap.scaledToHeight(height)
        icon = QIcon()  # QIcon 생성
        icon.addPixmap(pixmap)  # 아이콘에 이미지 설정
        self.btn_mode2.setIcon(icon)
        self.btn_mode2.setIconSize(QSize(height, height))

    def move_mode1(self):
        WordInfo.mode = 0
        self.move_mode()

    def move_mode2(self):
        WordInfo.mode = 1
        self.move_mode()

    def move_mode(self):
        WordInfo.cate = 0
        Instance.changeWindow("learning")
