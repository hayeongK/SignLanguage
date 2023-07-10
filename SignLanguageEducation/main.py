import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

from UI.quiz import QuizWindow
from UI.quiz2 import QuizWindow2
from UI.mode import ModeWindow
from UI.learning import LearningWindow
from UI.word import WordWindow
from UI.quiz_note import NoteWindow
from instance import Instance
from UI.result import Result
from UI.quiz_cate import CateWindow

if __name__ == "__main__":
    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    Result.width = screen_rect.width()
    Result.height = screen_rect.height()

    Instance.windows["mode"] = ModeWindow()
    Instance.windows["quiz"] = QuizWindow()
    Instance.windows["quiz2"] = QuizWindow2()
    Instance.windows["word"] = WordWindow()
    Instance.windows["note"] = NoteWindow()
    Instance.windows["learning"] = LearningWindow()
    Instance.windows["cate"] = CateWindow()

    # # WindowClass의 인스턴스 생성
    Instance.windows["mode"].setWindowFlags(
        Qt.FramelessWindowHint)  # 최대, 최소, 닫기 UI 삭제
    Instance.windows["mode"].showMaximized()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
