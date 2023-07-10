import cv2
import threading
import random
import urllib.request
import os.path

from PyQt5.QtWidgets import *
from PyQt5 import uic, QtCore
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QPixmap, QImage
from time import sleep

from instance import Instance
from UI.result import Result

import time
from sld.mediapipes import *
from sld.configs import Config
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sld.mediapipes import *
from sld.configs2 import Config2
from pasing import *

test_model = "quiz2.h5"

mp = MediaPipe(detection_option=["rh"])

result_arr = Config2.get_action_num()

model = Sequential()
model.add(LSTM(64, return_sequences=True, activation='relu',
          input_shape=(Config2.SEQUENCE_LENGTH, 63)))
model.add(LSTM(128, return_sequences=True, activation='relu'))
model.add(LSTM(64, return_sequences=False, activation='relu'))
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(result_arr.shape[0], activation='softmax'))
model.load_weights(test_model)


form_quiz = uic.loadUiType("./UI/quiz2.ui")[0]


class QuizWindow2(QDialog, QWidget, form_quiz):
    def __init__(self):
        super(QuizWindow2, self).__init__()
        self.initUi()

        self.btn_learn.clicked.connect(self.btn_learing_function)
        self.btn_quiz.clicked.connect(self.btn_quiz_function)
        self.btn_mode.clicked.connect(self.btn_mode_function)
        self.btn_pass.clicked.connect(self.btn_pass_function)

        self.running = False
        self.video_running = False

        self.page = 5  # 퀴즈 문제 수
        self.nth_quiz = 0
        self.lb_page_all.setText(str(self.page))
        self.lb_page.setText("")

        self.list = []
        self.answers = [self.btn_answer1, self.btn_answer2,
                        self.btn_answer3, self.btn_answer4]
        self.cate = [Result.cate01, Result.cate02, Result.cate03, Result.cate04, Result.cate05, Result.cate06, Result.cate07, Result.cate08,
                     Result.cate09, Result.cate10, Result.cate11, Result.cate12, Result.cate13, Result.cate14, Result.cate15, Result.cate16]
        self.thread_camera = threading.Thread(target=self.camera_run)
        self.start = False

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
        if not self.start:
            self.start = True
            Result.words = []
            Result.check = [False, False, False, False, False]
            self.lb_question.setText("문제 준비중")

    def select_words(self):
        self.list = random.sample(list(self.cate[Result.cate].keys()), 4)
        while True:  # 단어 겹치지 않는지 확인
            if self.list[0] in Result.words:
                self.list = random.sample(
                    list(self.cate[Result.cate].keys()), 4)
            else:
                break
        Result.words.append(self.list[0])
        self.video_thread()  # 영상 재생
        random.shuffle(self.list)

    def page_reset(self):
        # self.running = False
        self.start = False
        self.nth_quiz = 0
        self.lb_page.setText("")
        # self.nth_quiz = -1
        self.lb_question.setText("단어")
        for i in range(4):
            self.answers[i].setText(str(i+1))

    def next_word(self):
        if self.nth_quiz == self.page:  # 단어 퀴즈 끝나면
            self.page_reset()
        else:
            self.nth_quiz += 1
            self.lb_page.setText(str(self.nth_quiz))
            self.select_words()
            for i in range(4):  # 단어 보기 변경
                self.answers[i].setText("{} {}".format(
                    i+1, self.cate[Result.cate][self.list[i]]))

    def camera_run(self):
        width = Result.width * 3 / 5
        sequence = 0
        check = 0
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, Config.CAMERA_WIDTH)  # 1280
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, Config.CAMERA_HEIGHT)  # 720
        start = time.time()
        while self.running:
            ret, frame = cap.read()
            if ret:
                image, result = mp.mediapipe_detection(frame)
                mp.draw_styled_landmarks(image, result)
                cv2.rectangle(image,
                              (Config.CAMERA_WIDTH // 6,
                               Config.CAMERA_HEIGHT // 5),
                              (Config.CAMERA_WIDTH // 3,
                               Config.CAMERA_HEIGHT // 5 * 3),
                              (255, 0, 0),
                              thickness=2,
                              lineType=cv2.LINE_AA)
                remain = time.time() - start
                if remain > Config2.WAIT_TIME:
                    if self.video_running == True:
                        self.video_running = False
                    sequences = []
                    st = time.time()
                    for idx in range(Config2.SEQUENCE_LENGTH):
                        ret, frame = cap.read()
                        image, result = mp.mediapipe_detection(frame)
                        mp.draw_styled_landmarks(image, result)
                        cv2.rectangle(image,
                                      (Config.CAMERA_WIDTH // 6,
                                       Config.CAMERA_HEIGHT // 5),
                                      (Config.CAMERA_WIDTH // 3,
                                          Config.CAMERA_HEIGHT // 5 * 3),
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

                    # 판단
                    if self.start and len(Result.words) != 0:
                        if int(Config2.get_action_name(result_arr[np.argmax(res)])) > -1 and int(Config2.get_action_name(result_arr[np.argmax(res)])) < 4:
                            if self.list[int(Config2.get_action_name(result_arr[np.argmax(res)]))-1] == Result.words[-1]:
                                Result.check[len(Result.words)-1] = True

                    sequence += 1
                    start = time.time()
                    print(Config2.get_action_name(result_arr[np.argmax(res)]))
                else:
                    cv2.putText(image, 'wait %.2f sec ' % (Config2.WAIT_TIME - remain), (100, 100),
                                cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0), 5, cv2.LINE_AA)
                    check = sequence
                if self.start == True and sequence != check:
                    self.next_word()
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(
                    img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
                pixmap = QPixmap(convertToQtFormat)
                pixmap = pixmap.scaledToWidth(width)
                self.lb_camera.setPixmap(pixmap)
                cv2.waitKey(1)
        self.lb_camera.setText("카메라 준비중")

    def camera_thread(self):
        self.running = True
        self.thread_camera = threading.Thread(target=self.camera_run)
        self.thread_camera.start()

    def Video_to_frame(self, MainWindow):
        video_url = getMovieUrl(Result.words[-1])  # 영상주소 받아서 변수에 저장
        # 저장될 영상 이름
        self.savename = './video/video_{}.mp4'.format(
            self.cate[Result.cate][Result.words[-1]])
        if not os.path.isfile(self.savename):
            urllib.request.urlretrieve(
                video_url, self.savename)  # 영상 주소 접근해서 저장
        cap = cv2.VideoCapture(self.savename)  # 저장된 영상 가져오기

        ###cap으로 영상의 프레임을 가지고와서 전처리 후 화면에 띄움###
        while self.video_running:
            self.ret, self.frame = cap.read()  # 영상의 정보 저장
            if self.ret:
                self.frame = self.frame[:350, :]  # 영상 자르기
                self.rgbImage = cv2.cvtColor(
                    self.frame, cv2.COLOR_BGR2RGB)  # 프레임에 색입히기
                self.convertToQtFormat = QImage(self.rgbImage.data, self.rgbImage.shape[1], self.rgbImage.shape[0],
                                                QImage.Format_RGB888)

                self.pixmap = QPixmap(self.convertToQtFormat)
                self.p = self.pixmap.scaledToWidth(Result.width / 4)
                # self.p = self.pixmap.scaled(
                #     500, 300, QtCore.Qt.IgnoreAspectRatio)  # 프레임 크기 조정 /4:3(500:375) -> 16:9

                self.lb_question.setPixmap(self.p)
                self.lb_question.update()  # 프레임 띄우기

                sleep(0.01)  # 영상 1프레임당 0.01초로 이걸로 영상 재생속도 조절하면됨 0.02로하면 0.5배속인거임
            else:
                break
        cap.release()

    # 수어 영상 쓰레드
    def video_thread(self):
        self.video_running = True
        thread = threading.Thread(target=self.Video_to_frame, args=(self,))
        thread.daemon = True
        thread.start()
