from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap, QImage
from time import sleep
import urllib.request
import threading
import cv2
import os.path

from instance import Instance
from UI.result import Result
from UI.wordInfo import WordInfo
from pasing import *

form_note = uic.loadUiType("./UI/quiz_note.ui")[0]


class NoteWindow(QDialog, QWidget, form_note):
    def __init__(self):
        super(NoteWindow, self).__init__()
        self.initUi()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_quiz.clicked.connect(self.btn_quiz_function)
        self.btn_mode.clicked.connect(self.btn_mode_function)

        self.words = [self.label_word1, self.label_word2,
                      self.label_word3, self.label_word4, self.label_word5]
        self.checks = [self.label_check1, self.label_check2,
                       self.label_check3, self.label_check4, self.label_check5]
        self.btn_videos = [self.btn_video1, self.btn_video2,
                           self.btn_video3, self.btn_video4, self.btn_video5]
        self.btn_video_funcs = [self.btn_video_function1, self.btn_video_function2,
                                self.btn_video_function3, self.btn_video_function4, self.btn_video_function5]
        self.nth_video = 0
        for i in range(5):
            self.btn_videos[i].clicked.connect(self.btn_video_funcs[i])
        self.thread = threading.Thread(
            target=self.Video_to_frame, args=(self,))
        self.score = 0

    def initUi(self):
        self.setupUi(self)

    def btn_learing_function(self):
        Instance.changeWindow("learning")

    def btn_quiz_function(self):
        if WordInfo.mode == 0:
            Instance.changeWindow("quiz")
        else:
            Instance.changeWindow("cate")

    def btn_mode_function(self):
        Instance.changeWindow("mode")

    def set_result(self):
        for i in range(5):
            self.words[i].setText("-")
        for i in range(5):
            self.checks[i].setText("X")
        self.score = 0
        # 초기화 후 세팅
        for i in range(len(Result.words)):
            self.words[i].setText(Result.all_words[Result.words[i]])
        for i in range(5):
            if Result.check[i]:
                self.checks[i].setText("O")
                self.score += 1
            else:
                self.checks[i].setText("X")
        self.lb_score.setText("{}/5".format(self.score))
        self.lb_video.setText("")

    def Video_to_frame(self, MainWindow):
        width = Result.width * 2 / 5
        video_url = getMovieUrl(
            Result.words[self.nth_video])  # 영상주소 받아서 변수에 저장
        # 저장될 영상 이름
        self.savename = './video/video_{}.mp4'.format(
            Result.all_words[Result.words[self.nth_video]])
        if not os.path.isfile(self.savename):
            urllib.request.urlretrieve(
                video_url, self.savename)  # 영상 주소 접근해서 저장
        cap = cv2.VideoCapture(self.savename)  # 저장된 영상 가져오기

        ###cap으로 영상의 프레임을 가지고와서 전처리 후 화면에 띄움###
        while True:
            self.ret, self.frame = cap.read()  # 영상의 정보 저장
            if self.ret:
                self.rgbImage = cv2.cvtColor(
                    self.frame, cv2.COLOR_BGR2RGB)  # 프레임에 색입히기
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaledToWidth(width)
                # self.p = self.pixmap.scaled(
                #     500, 300, QtCore.Qt.IgnoreAspectRatio)  # 프레임 크기 조정 /4:3(500:375) -> 16:9

                self.lb_video.setPixmap(self.p)
                self.lb_video.update()  # 프레임 띄우기

                sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임
            else:
                break
        cap.release()

    # 수어 영상 쓰레드
    def video_thread(self):
        if not self.thread.is_alive():
            self.thread = threading.Thread(
                target=self.Video_to_frame, args=(self,))
            self.thread.daemon = True
            self.thread.start()

    # UI 버튼과 연결
    def btn_video_function1(self):
        self.nth_video = 0
        self.video_thread()

    def btn_video_function2(self):
        self.nth_video = 1
        self.video_thread()

    def btn_video_function3(self):
        self.nth_video = 2
        self.video_thread()

    def btn_video_function4(self):
        self.nth_video = 3
        self.video_thread()

    def btn_video_function5(self):
        self.nth_video = 4
        self.video_thread()
