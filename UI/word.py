import urllib.request
import threading
import sys
import cv2

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtGui import QPixmap, QImage
# open cv에서는 영상을 프레임단위로 가져오기 때문에 sleep을 통해서 프레임을 연결시켜주어 영상으로 보이게 만드는 것임
from time import sleep


#from UI.quiz import QuizWindow
from instance import Instance
from UI.wordInfo import WordInfo
from pasing import *

form_word = uic.loadUiType("./UI/word.ui")[0]


class WordWindow(QDialog, QWidget, form_word):
    def __init__(self):
        super(WordWindow, self).__init__()
        self.initUi()
        # self.show()

        # self.showMaximized()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_quiz.clicked.connect(self.btn_quiz_function)

        self.btn_cates = [self.btn_cate01, self.btn_cate02, self.btn_cate03, self.btn_cate04, self.btn_cate05, self.btn_cate06, self.btn_cate07, self.btn_cate08,
                          self.btn_cate09, self.btn_cate10, self.btn_cate11, self.btn_cate12, self.btn_cate13, self.btn_cate14, self.btn_cate15, self.btn_cate16]
        self.btn_cate_funcs = [self.btn_cate_function01, self.btn_cate_function02, self.btn_cate_function03, self.btn_cate_function04, self.btn_cate_function05, self.btn_cate_function06, self.btn_cate_function07, self.btn_cate_function08,
                               self.btn_cate_function09, self.btn_cate_function10, self.btn_cate_function11, self.btn_cate_function12, self.btn_cate_function13, self.btn_cate_function14, self.btn_cate_function15, self.btn_cate_function16]
        for c in range(len(self.btn_cates)):
            self.btn_cates[c].clicked.connect(self.btn_cate_funcs[c])

    def initUi(self):
        self.setupUi(self)

    def btn_learing_function(self):
        Instance.window.changeWindow("word", "learning")

    def btn_quiz_function(self):
        Instance.window.changeWindow("word", "quiz")

    def setWord(self):
        self.lb_word.setText(WordInfo.word)
        if len(WordInfo.explain) > 60:  # 띄어쓰기
            temp = WordInfo.explain[0]
            for i in range(1, len(WordInfo.explain)):
                if i % 60 == 0:
                    temp += (WordInfo.explain[i] + "\n")
                else:
                    temp += WordInfo.explain[i]
            self.lb_explain.setText(temp)
        else:
            self.lb_explain.setText(WordInfo.explain)
        self.lbs = [self.lb_img1, self.lb_img2]
        for i in range(len(WordInfo.picture)):
            self.get_picture(WordInfo.picture[i], self.lbs[i])
        self.video_thread()

    def get_picture(self, link, lb):
        self.url = link
        img_data = urllib.request.urlopen(self.url).read()
        img_obj = QPixmap()
        img_obj.loadFromData(img_data)
        img_obj = img_obj.scaledToHeight(240)
        lb.setPixmap(img_obj)

    def Video_to_frame(self, MainWindow):

        video_url = WordInfo.video  # 영상주소 받아서 변수에 저장
        savename = './video/video_{}.mp4'.format(WordInfo.word)  # 저장될 영상 이름

        urllib.request.urlretrieve(video_url, savename)  # 영상 주소 접근해서 저장

        cap = cv2.VideoCapture(savename)  # 저장된 영상 가져오기 프레임별로 계속 가져오는 듯

        ###cap으로 영상의 프레임을 가지고와서 전처리 후 화면에 띄움###
        while True:
            self.ret, self.frame = cap.read()  # 영상의 정보 저장
            if self.ret:
                self.rgbImage = cv2.cvtColor(
                    self.frame, cv2.COLOR_BGR2RGB)  # 프레임에 색입히기
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaled(
                    400, 300, QtCore.Qt.IgnoreAspectRatio)  # 프레임 크기 조정

                self.lb_video.setPixmap(self.p)
                self.lb_video.update()  # 프레임 띄우기

                sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임

            else:
                break

        cap.release()
        cv2.destroyAllWindows()

    # 이게 영상 재생 쓰레드 돌리는거 얘를 조작하거나 함수를 생성해서 연속재생 관리해야할듯
    def video_thread(self):
        thread = threading.Thread(target=self.Video_to_frame, args=(self,))
        thread.daemon = True  # 프로그램 종료시 프로세스도 함께 종료 (백그라운드 재생 X)
        thread.start()

    def btn_cate_function01(self):
        WordInfo.cate = 0
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function02(self):
        WordInfo.cate = 1
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function03(self):
        WordInfo.cate = 2
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function04(self):
        WordInfo.cate = 3
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function05(self):
        WordInfo.cate = 4
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function06(self):
        WordInfo.cate = 5
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function07(self):
        WordInfo.cate = 6
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function08(self):
        WordInfo.cate = 7
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function09(self):
        WordInfo.cate = 8
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function10(self):
        WordInfo.cate = 9
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function11(self):
        WordInfo.cate = 10
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function12(self):
        WordInfo.cate = 11
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function13(self):
        WordInfo.cate = 12
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function14(self):
        WordInfo.cate = 13
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function15(self):
        WordInfo.cate = 14
        Instance.window.changeWindow("word", "learning")

    def btn_cate_function16(self):
        WordInfo.cate = 15
        Instance.window.changeWindow("word", "learning")
