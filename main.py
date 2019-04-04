#! /usr/bin/python3
import sys
from speechTed import get_speech, get_differences
from VideoTed import VideoWgt
from PanelBox import PanelBox
from Frames import FramesTed, FM_WORDS, FM_WORDS_TEXT
from SubBox import SubWdg
from SpeechBox import SpeechWdg
from TedCommon import NUMBER_LB_TOTAL, NUMBER_LB_LINE, MAXIMUM_HEIGT_LABEL
from TedCommon import PLAY_MODE_SUB, PLAY_MODE_1_SUB, PLAY_VIDEO, SAY_MODE_1
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,\
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QKeyEvent

filename = "/home/hirvin/Documents/Myprojects/TED/video.mp4"


class MainWindow(QMainWindow):
    """ Main Windows """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.videoPlayer = VideoWgt()
        self.frames = FramesTed(f_json="Frames_ted.json")
        self.mode = None
        self.setWindowTitle("PyTedict")
        self.createUi()
        self.initMain()

    def createUi(self):
        """ set up the user interface """
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.main_layout = QVBoxLayout()

        # create video widget
        self.panelBox = PanelBox()

        # addingo to main layout
        # self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.videoPlayer)
        self.main_layout.addWidget(self.panelBox)
        self.widget.setLayout(self.main_layout)

        # conect slots
        self.panelBox.button1.clicked.connect(self.pressButton1)
        self.panelBox.button2.clicked.connect(self.pressButton2)
        self.videoPlayer.videoFrameComplete.connect(self.videoFrameComplete)
        self.panelBox.subBox.subtitleFrameComplete.connect(self.subtitleFrameComplete)
        # self.clicked.connect(self.pressButton)

    def initMain(self):
        """ init Main """
        # frames
        # self.mode = PLAY_MODE_SUB
        self.mode = SAY_MODE_1 # solo pruebas
        fm = self.frames.get_current_frame()
        self.panelBox.initWords(frame=fm, mode=self.mode)
        self.videoPlayer.openVideo(filename=filename)
        self.playVideo(init_time=0)

    def playVideo(self, init_time=None, end_time=None):
        """ play video """
        if init_time is None:
            init_time = self.frames.getInitTime()
        if end_time is None:
            end_time = self.frames.getEndTime()
        offset = self.frames.getOffset()
        # print (f"init time is {init_time}")
        self.videoPlayer.play(init_time=init_time, end_time=end_time, offset=offset)
        # self.mode = PLAY_VIDEO
        self.panelBox.setMode(PLAY_VIDEO)

    # Slots
    def pressButton1(self):
        """ pressButton """
        if (self.mode == PLAY_MODE_SUB) or (self.mode == SAY_MODE_1):
            self.playVideo()
        elif self.mode == PLAY_MODE_1_SUB:
            if self.frames.prev_frame():
                fm = self.frames.get_current_frame()
                self.panelBox.initWords(frame=fm, mode=self.mode)
                self.playVideo()
            else:
                self.playVideo()

    def pressButton2(self):
        """ pressButton """
        if self.mode == PLAY_MODE_1_SUB:
            if self.frames.next_frame():
                fm = self.frames.get_current_frame()
                self.panelBox.initWords(frame=fm, mode=self.mode)
                self.playVideo()
            else:
                self.playVideo()
        elif self.mode == SAY_MODE_1:
            # aqui va el speech
            textFrame = self.frames.get_text_from_frame()
            self.panelBox.setLabelInfo("Say something!")
            speech = get_speech()
            print (f"You had to say: {textFrame}")
            wordSpeech = get_differences(originalText=textFrame, speechText=speech)
            print (wordSpeech)
            self.panelBox.playSpeech(words=wordSpeech)

    def videoFrameComplete(self):
        """ video frame is completed """
        print ("Video Frame is Completed")
        self.panelBox.setMode(self.mode)

    def subtitleFrameComplete(self):
        """ subtitle frame is completed """
        print ("Subtitle Frame is Completed")
        self.mode = SAY_MODE_1
        self.panelBox.setMode(self.mode)

    # events
    def keyPressEvent(self, event):
        """ key press event """
        if type(event) == QKeyEvent:
            key = event.key()
            # print (chr(key))
            if self.mode == PLAY_MODE_SUB:
                self.panelBox.setKey(chr(key))
                self.panelBox.subBox.playKey(key=chr(key))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MainWindow()
    # player.resize(640, 880)
    player.show()
    sys.exit(app.exec_())
