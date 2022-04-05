import sys
import time

from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from UI.quiz import QuizWindow
from UI.quiz2 import QuizWindow2
from UI.mode import ModeWindow
from UI.learning import LearningWindow
from UI.word import WordWindow
from UI.quiz_note import NoteWindow
from UI.quiz_cate import CateWindow
from instance import Instance
from utils.WindowChanged import WindowChanged

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    Instance.window = WindowChanged(screen_rect)

    Instance.window.setWindow("quiz", QuizWindow())
    Instance.window.setWindow("quiz2", QuizWindow2())
    Instance.window.setWindow("word", WordWindow())
    Instance.window.setWindow("note", NoteWindow())
    Instance.window.setWindow("cate", CateWindow())
    Instance.window.setWindow("learning", LearningWindow())

    # # WindowClass의 인스턴스 생성

    modeWindow = ModeWindow()
    Instance.window.setWindow("mode", modeWindow)
    # # 화면 크기를 가져옴

    # # 화면 크기 고정

    modeWindow.setFixedSize(screen_rect.width(),
                            screen_rect.height() - 45)  # 0, -45
    # modeWindow.setWindowFlags(Qt.FramelessWindowHint)  # 최대, 최소, 닫기 UI 삭제

    modeWindow.showMaximized()  # 전체화면으로

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
