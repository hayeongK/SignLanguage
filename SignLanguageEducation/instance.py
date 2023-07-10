from PyQt5.QtCore import Qt


class Instance:
    windows = {}
    pres_window = "mode"

    @staticmethod
    def changeWindow(form_name):
        Instance.windows[Instance.pres_window].hide()
        Instance.pres_window = form_name
        Instance.windows[form_name].setWindowFlags(
            Qt.FramelessWindowHint)  # 최대, 최소, 닫기 UI 삭제
        Instance.windows[form_name].showMaximized()

        if form_name == "word":
            Instance.windows[form_name].setWord()
        if form_name == "learning":
            Instance.windows[form_name].setWords()
        if form_name == "note":
            Instance.windows[form_name].set_result()
        if form_name == "quiz":
            # Instance.windows[form_name].select_words()
            Instance.windows[form_name].start()
        if form_name == "quiz2":
            Instance.windows[form_name].camera_thread()

