import threading
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from instance import Instance
from pasing import *
from UI.wordInfo import WordInfo
from UI.result import Result

form_learning = uic.loadUiType("./UI/learning.ui")[0]


class LearningWindow(QDialog, QWidget, form_learning):
    def __init__(self):
        super(LearningWindow, self).__init__()
        self.initUi()

        self.categories = loadCategory()
        self.cate_cur = self.categories[0].category  # 카테고리
        self.cate_page = numOfPages(self.cate_cur)
        self.page = 1  # 현재 페이지
        self.nth = 1  # 단어 선택
        self.words = []
        self.th = threading.Thread(target=self.set)  # 단어 세팅 쓰레드

        self.btn_pre.clicked.connect(self.page_pre)
        self.btn_next.clicked.connect(self.page_next)

        self.btn_words = [self.btn_word01, self.btn_word02, self.btn_word03, self.btn_word04, self.btn_word05,
                          self.btn_word06, self.btn_word07, self.btn_word08, self.btn_word09, self.btn_word10]
        self.btn_word_funcs = [self.btn_word_function01, self.btn_word_function02, self.btn_word_function03, self.btn_word_function04, self.btn_word_function05,
                               self.btn_word_function06, self.btn_word_function07, self.btn_word_function08, self.btn_word_function09, self.btn_word_function10]
        for w in range(len(self.btn_words)):
            self.btn_words[w].clicked.connect(self.btn_word_funcs[w])
        self.loading()

        self.label_page_cate.setText(str(self.cate_page))

        self.btn_cates = [self.btn_cate01, self.btn_cate02, self.btn_cate03, self.btn_cate04, self.btn_cate05, self.btn_cate06, self.btn_cate07, self.btn_cate08,
                          self.btn_cate09, self.btn_cate10, self.btn_cate11, self.btn_cate12, self.btn_cate13, self.btn_cate14, self.btn_cate15, self.btn_cate16]
        self.btn_cate_funcs = [self.btn_cate_function01, self.btn_cate_function02, self.btn_cate_function03, self.btn_cate_function04, self.btn_cate_function05, self.btn_cate_function06, self.btn_cate_function07, self.btn_cate_function08,
                               self.btn_cate_function09, self.btn_cate_function10, self.btn_cate_function11, self.btn_cate_function12, self.btn_cate_function13, self.btn_cate_function14, self.btn_cate_function15, self.btn_cate_function16]
        for c in range(len(self.btn_cates)):
            self.btn_cates[c].clicked.connect(self.btn_cate_funcs[c])
            self.set_icon(c)

    def initUi(self):
        self.setupUi(self)

    def btn_quiz_function(self):
        if WordInfo.mode == 0:
            Instance.changeWindow("quiz")
        else:
            Instance.changeWindow("cate")

    def btn_mode_function(self):
        if not self.th.is_alive():
            Instance.changeWindow("mode")

    def btn_word_function(self):
        if not self.th.is_alive():
            WordInfo.word = self.words[self.nth].mean
            WordInfo.explain = getExplain(self.words[self.nth].origin_no)
            WordInfo.picture = getPictureUrl(self.words[self.nth].origin_no)
            WordInfo.video = getMovieUrl(self.words[self.nth].origin_no)
            Instance.changeWindow("word")

    def loading(self):
        for i in range(len(self.btn_words)):
            self.btn_words[i].setText("로딩중")
            self.btn_words[i].setIconSize(QSize(0, 0))

    def setWords(self):  # 단어에서 전환될 때 호출되는 함수
        self.cate_cur = self.categories[WordInfo.cate].category
        self.btn_cate_function()

    def btn_cate_function(self):  # 카테고리의 첫 페이지
        if not self.th.is_alive():
            self.page = 1
            self.loading()
            self.set_words()
            self.label_page_cate.setText(str(self.cate_page))

    def page_pre(self):
        if not self.th.is_alive():
            if not self.page == 1:
                self.page -= 1
                self.loading()
                self.set_words()

    def page_next(self):
        if not self.th.is_alive():
            if self.page != self.cate_page:
                self.page += 1
                self.loading()
                self.set_words()

    def set_words(self):
        self.th = threading.Thread(target=self.set)
        self.th.start()

    def set(self):  # 현재 카테고리와 버튼에 페이지의 단어 보이도록
        for i in range(len(self.btn_words)):
            self.btn_words[i].setText("로딩중")
        self.cate_page = numOfPages(self.cate_cur)
        self.label_page_cate.setText(str(self.cate_page))
        if WordInfo.mode == 0:
            self.label_page.setText(str(self.page))
            self.words = getWord(self.cate_cur, self.page)
            for i in range(len(self.words)):
                if self.words[i].mean.count(',') > 1:  # 띄어쓰기
                    sep = self.words[i].mean.split(',')
                    text = sep[0] + ","
                    for j in range(1, len(sep)-1):
                        if j % 2 == 1:
                            text += (sep[j] + ",\n")
                        else:
                            text += (sep[j] + ",")
                    text += sep[-1]
                    self.btn_words[i].setText(text)
                else:
                    self.btn_words[i].setIconSize(QSize(0, 0))
                    self.btn_words[i].setText(self.words[i].mean)
            for i in range(10-len(self.words)):
                self.btn_words[9-i].setText("")
        else:
            self.set_pictures()

    def set_pictures(self):  # 버튼에 수형 사진 불러오기
        height = Result.height / 6
        width = Result.width / 9
        self.label_page.setText(str(self.page))
        self.words = getWord(self.cate_cur, self.page)
        for i in range(len(self.words)):
            url = getPictureUrl(self.words[i].origin_no)[0]
            img_data = urllib.request.urlopen(url).read()

            pixmap = QPixmap()
            pixmap.loadFromData(img_data)
            # pixmap = pixmap.scaledToHeight(height)

            icon = QIcon()  # QIcon 생성
            icon.addPixmap(pixmap)  # 아이콘에 이미지 설정

            self.btn_words[i].setIcon(icon)
            self.btn_words[i].setIconSize(QSize(width, height))
            word = self.words[i].mean
            if "," not in word:
                if len(word) > 4:
                    for j in range(len(word)):
                        if j % 4 == 3:
                            word = word[:j] + '\n' + word[j:]
                self.btn_words[i].setText(word)
            else:
                self.btn_words[i].setText(word.split(",")[0])

        for i in range(10-len(self.words)):
            if len(word) > 4:
                for j in range(len(word)):
                    if j % 4 == 3:
                        word = word[:j] + '\n' + word[j:]
            self.btn_words[9-i].setText("")

    def set_icon(self, i):  # 카테고리 아이콘
        height = Result.height / 25
        pixmap = QPixmap("./UI/icon/menu_icon{}.png".format(i+1))
        pixmap = pixmap.scaledToHeight(80)

        icon = QIcon()  # QIcon 생성
        icon.addPixmap(pixmap)  # 아이콘에 이미지 설정

        self.btn_cates[i].setIcon(icon)
        self.btn_cates[i].setIconSize(QSize(height, height))

    # UI 버튼과 연결
    def btn_cate_function01(self):
        self.cate_cur = self.categories[0].category
        self.btn_cate_function()
        WordInfo.cate = 0

    def btn_cate_function02(self):
        self.cate_cur = self.categories[1].category
        self.btn_cate_function()
        WordInfo.cate = 1

    def btn_cate_function03(self):
        self.cate_cur = self.categories[2].category
        self.btn_cate_function()
        WordInfo.cate = 2

    def btn_cate_function04(self):
        self.cate_cur = self.categories[3].category
        self.btn_cate_function()
        WordInfo.cate = 3

    def btn_cate_function05(self):
        self.cate_cur = self.categories[4].category
        self.btn_cate_function()
        WordInfo.cate = 4

    def btn_cate_function06(self):
        self.cate_cur = self.categories[5].category
        self.btn_cate_function()
        WordInfo.cate = 5

    def btn_cate_function07(self):
        self.cate_cur = self.categories[6].category
        self.btn_cate_function()
        WordInfo.cate = 6

    def btn_cate_function08(self):
        self.cate_cur = self.categories[7].category
        self.btn_cate_function()
        WordInfo.cate = 7

    def btn_cate_function09(self):
        self.cate_cur = self.categories[8].category
        self.btn_cate_function()
        WordInfo.cate = 8

    def btn_cate_function10(self):
        self.cate_cur = self.categories[9].category
        self.btn_cate_function()
        WordInfo.cate = 9

    def btn_cate_function11(self):
        self.cate_cur = self.categories[10].category
        self.btn_cate_function()
        WordInfo.cate = 10

    def btn_cate_function12(self):
        self.cate_cur = self.categories[11].category
        self.btn_cate_function()
        WordInfo.cate = 11

    def btn_cate_function13(self):
        self.cate_cur = self.categories[12].category
        self.btn_cate_function()
        WordInfo.cate = 12

    def btn_cate_function14(self):
        self.cate_cur = self.categories[13].category
        self.btn_cate_function()
        WordInfo.cate = 13

    def btn_cate_function15(self):
        self.cate_cur = self.categories[14].category
        self.btn_cate_function()
        WordInfo.cate = 14

    def btn_cate_function16(self):
        self.cate_cur = self.categories[15].category
        self.btn_cate_function()
        WordInfo.cate = 15

    def btn_word_function01(self):
        self.nth = 0
        self.btn_word_function()

    def btn_word_function02(self):
        self.nth = 1
        self.btn_word_function()

    def btn_word_function03(self):
        self.nth = 2
        self.btn_word_function()

    def btn_word_function04(self):
        self.nth = 3
        self.btn_word_function()

    def btn_word_function05(self):
        self.nth = 4
        self.btn_word_function()

    def btn_word_function06(self):
        self.nth = 5
        self.btn_word_function()

    def btn_word_function07(self):
        self.nth = 6
        self.btn_word_function()

    def btn_word_function08(self):
        self.nth = 7
        self.btn_word_function()

    def btn_word_function09(self):
        self.nth = 8
        self.btn_word_function()

    def btn_word_function10(self):
        self.nth = 9
        self.btn_word_function()
