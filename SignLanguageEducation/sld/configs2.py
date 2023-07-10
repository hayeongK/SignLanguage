import numpy as np

# Project Settings

ACTIONS = [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("32", "3"),
    ("5", "5"),
    ("0", "0"),
    ("10", "10"),
    ("33", "3")
]


class Config2:
    # MediaPipe Settings
    MIN_DECTION_CONFIDENCE = 0.5
    MIN_TRACKING_CONFIDENCE = 0.5

    # Train & Test
    VALID_FOLDER_VIDEO = "dataset/VV_Data"
    RECOGNIZE_THRESHOLD = 0.5

    # Videos_capture
    WAIT_TIME = 7
    SEQUENCE_LENGTH = 10
    VIDEO_FOLDER = "dataset/GV_Data"
    DATASET_DB_FILE = "dataset/dataset.db"
    VALIDSET_DB_FILE = "dataset/validset.db"
    FPS = 10

    # OpenCV Settings
    CAMERA_WIDTH = 1280
    CAMERA_HEIGHT = 720

    @staticmethod
    def get_action_num():
        temp = [i[0] for i in ACTIONS]
        temp.sort(key=lambda x: int(x[0]))
        return np.array([i[0] for i in ACTIONS])

    @staticmethod
    def get_action_dict():
        return ACTIONS

    @staticmethod
    def get_action_name(action_num):
        for action in ACTIONS:
            if action_num == action[0]:
                return action[1]
