import cv2
import threading
import random

from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QImage

from instance import Instance
from UI.result import Result

import time
import os
from sld.mediapipes import *
from sld.configs import Config
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sld.mediapipes import *
from sld.configs import Config

import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

form = resource_path('quiz.ui')

# form = os.path.dirname(os.path.abspath(__file__)) + '\quiz.ui'

form_quiz = uic.loadUiType(form)[0]

test_model = "quiz1.h5"

mp = MediaPipe(detection_option=["pose", "lh", "rh"])

result_arr = Config.get_action_num()

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu',
          input_shape=(Config.SEQUENCE_LENGTH, 258)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(result_arr.shape[0], activation='softmax'))
model.load_weights(test_model)


class QuizWindow(QDialog, QWidget, form_quiz):
    def __init__(self):
        super(QuizWindow, self).__init__()
        self.initUi()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_quiz.clicked.connect(self.btn_quiz_function)
        self.btn_mode.clicked.connect(self.btn_mode_function)
        self.btn_pass.clicked.connect(self.btn_pass_function)

        self.running = False

        self.page = 5  # 문제 갯수
        self.lb_page_all.setText(str(self.page))
        self.lb_page.setText("")
        self.nth_quiz = 0  # 몇번째 퀴즈인지

        self.th = threading.Thread(target=self.camera_run)

    def initUi(self):
        self.setupUi(self)

    def btn_learing_function(self):
        if self.running:
            self.running = False
        self.page_reset()
        Instance.changeWindow("learning")

    def btn_quiz_function(self):
        if self.running:
            self.running = False
        self.page_reset()
        Instance.changeWindow("note")

    def btn_mode_function(self):
        if self.running:
            self.running = False
        self.page_reset()
        Instance.changeWindow("mode")

    def btn_pass_function(self):
        if self.nth_quiz == self.page:  # 단어 퀴즈 끝나면
            self.page_reset()
        else:
            self.lb_page.setText(str(self.nth_quiz + 1))
            if self.nth_quiz == 0:
                self.select_words()
                Result.check = [False, False, False, False, False]
                self.btn_pass.setText("다음")
            self.lb_question.setText(
                Result.quiz_words[Result.words[self.nth_quiz]])
            self.nth_quiz += 1

    def select_words(self):
        Result.words = random.sample(
            list(Result.quiz_words.keys())[1:], self.page)

    def page_reset(self):
        self.lb_page.setText("")
        self.nth_quiz = 0
        self.lb_question.setText("단어")
        self.btn_pass.setText("시작")

    def camera_run(self):
        width = Result.width * 3 / 5
        sequence = 0
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)  # 1280
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)  # 720
        start = time.time()
        while self.running:
            ret, frame = cap.read()
            if ret:
                image, result = mp.mediapipe_detection(frame)
                mp.draw_styled_landmarks(image, result)
                cv2.circle(image,
                           (Config.CAMERA_WIDTH // 2, Config.CAMERA_HEIGHT // 5),
                           Config.CAMERA_HEIGHT // 12 * 2,
                           (255, 0, 0),
                           thickness=2,
                           lineType=cv2.LINE_AA)
                # 원의 중심, 반지름, 선의 색, 굵기, 선 표현법
                cv2.rectangle(image,
                              (Config.CAMERA_WIDTH // 5,
                               Config.CAMERA_HEIGHT // 30 * 11),
                              (Config.CAMERA_WIDTH - Config.CAMERA_WIDTH //
                                  5, Config.CAMERA_HEIGHT),
                              (255, 0, 0),
                              thickness=2,
                              lineType=cv2.LINE_AA)
                remain = time.time() - start
                if remain > Config.WAIT_TIME:
                    sequences = []
                    st = time.time()
                    for idx in range(Config.SEQUENCE_LENGTH):
                        ret, frame = cap.read()
                        image, result = mp.mediapipe_detection(frame)
                        mp.draw_styled_landmarks(image, result)
                        cv2.circle(image,
                                   (Config.CAMERA_WIDTH // 2,
                                    Config.CAMERA_HEIGHT // 5),
                                   Config.CAMERA_HEIGHT // 12 * 2,
                                   (255, 0, 0),
                                   thickness=2,
                                   lineType=cv2.LINE_AA)
                        cv2.rectangle(image,
                                      (Config.CAMERA_WIDTH // 5,
                                       Config.CAMERA_HEIGHT // 30 * 11),
                                      (Config.CAMERA_WIDTH - Config.CAMERA_WIDTH //
                                       5, Config.CAMERA_HEIGHT),
                                      (255, 0, 0),
                                      thickness=2,
                                      lineType=cv2.LINE_AA)
                        keypoints = mp.extract_keypoints(result)
                        sequences.append(keypoints)
                        cv2.putText(image, 'capture %d frame' % (idx), (100, 100),
                                    cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)

                        img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        convertToQtFormat = QImage(
                            img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                        pixmap = QPixmap(convertToQtFormat)
                        pixmap = pixmap.scaledToWidth(width)
                        # scaledToHeight(200, Qt.SmoothTransformation)
                        self.lb_camera.setPixmap(pixmap)
                        # cv2.imshow("utils", image)
                        cv2.waitKey(2)
                    res = model.predict(np.expand_dims(sequences, axis=0))[0]
                    if len(Result.words) > 0:
                        if str(result_arr[np.argmax(res)]) == Result.words[self.nth_quiz-1]:
                            Result.check[self.nth_quiz-1] = True
                            self.btn_pass_function()
                    sequence += 1
                    start = time.time()
                else:
                    cv2.putText(image, 'wait %.2f sec ' % (Config.WAIT_TIME - remain), (100, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5, cv2.LINE_AA)
                # cv2.imshow("utils", image)
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(
                    img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap(convertToQtFormat)
                pixmap = pixmap.scaledToWidth(width)
                # scaledToHeight(200, Qt.SmoothTransformation)
                self.lb_camera.setPixmap(pixmap)
                cv2.waitKey(1)
        self.lb_camera.setText("카메라 준비중")

    def start(self):
        self.running = True
        self.th = threading.Thread(target=self.camera_run)
        self.th.start()
