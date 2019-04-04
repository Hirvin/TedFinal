#! /usr/bin/python3
import sys
from Frames import FramesTed, FM_WORDS, FM_WORDS_TEXT
from SubBox import SubWdg
from SpeechBox import SpeechWdg
from TedCommon import NUMBER_LB_TOTAL, NUMBER_LB_LINE, MAXIMUM_HEIGT_LABEL
from TedCommon import PLAY_MODE_SUB, PLAY_MODE_1_SUB, PLAY_VIDEO, SAY_MODE_1
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,\
    QVBoxLayout, QHBoxLayout, QLabel, QPushButton


class Button1(QPushButton):
    """ Button 1 """
    def __init__(self, parent=None):
        super(Button1, self).__init__(parent)
        self.mode = None
        self.setMaximumHeight(MAXIMUM_HEIGT_LABEL * 2)
        self.setMinimumHeight(MAXIMUM_HEIGT_LABEL * 2)
        self.setMinimumWidth(MAXIMUM_HEIGT_LABEL * 2)
        self.setMaximumWidth(MAXIMUM_HEIGT_LABEL * 2)

        # connect Signals
        # self.clicked.connect(self.pressButton)

    def setMode(self, mode=None):
        """ set Button Mode """
        if mode == PLAY_MODE_SUB:
            self.setText("Play")
            self.setEnabled(True)
            self.mode = PLAY_MODE_SUB
            return True
        if mode == PLAY_MODE_1_SUB:
            self.setText("Prev")
            self.setEnabled(True)
            self.mode = PLAY_MODE_1_SUB
            return True
        if mode == PLAY_VIDEO:
            self.setEnabled(False)
            self.mode = PLAY_VIDEO
            return True
        if mode == SAY_MODE_1:
            self.setEnabled(True)
            self.mode = SAY_MODE_1
            self.setText("Play")
            return True

    # def pressButton(self):
    #     """ pressButton """
    #     if self.mode == PLAY_MODE_1_SUB:
    #         print ("hola")


class Button2(QPushButton):
    """ Button 1 """
    def __init__(self, parent=None):
        super(Button2, self).__init__(parent)
        self.mode = None
        self.setMaximumHeight(MAXIMUM_HEIGT_LABEL * 2)
        self.setMinimumHeight(MAXIMUM_HEIGT_LABEL * 2)
        self.setMinimumWidth(MAXIMUM_HEIGT_LABEL * 2)
        self.setMaximumWidth(MAXIMUM_HEIGT_LABEL * 2)

        # connect signals
        # self.clicked.connect(self.pressButton)

    def setMode(self, mode=None):
        """ set Button Mode """
        if mode == PLAY_MODE_SUB:
            self.setText("Next")
            self.setEnabled(False)
            self.mode = PLAY_MODE_SUB
            return True
        if mode == PLAY_MODE_1_SUB:
            self.setText("Next")
            self.setEnabled(True)
            self.mode = PLAY_MODE_1_SUB
            return True
        if mode == PLAY_VIDEO:
            self.setEnabled(False)
            self.mode = PLAY_VIDEO
            return True
        if mode == SAY_MODE_1:
            self.setEnabled(True)
            self.mode = SAY_MODE_1
            self.setText("Say")
            return True

    # def pressButton(self):
    #     """ pressButton """
    #     if self.mode == PLAY_MODE_1_SUB:
    #         print ("hola")


class PanelBox(QWidget):
    """ video widget class """
    def __init__(self, parent=None):
        super(PanelBox, self).__init__(parent)
        self.subBox = SubWdg()
        self.speechBox = SpeechWdg()
        self.createUi()

    def createUi(self):
        """ create Ui """
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        # set playLayout
        self.playLayout = QVBoxLayout()
        self.playLayout.addWidget(self.subBox)
        self.playLayout.addWidget(self.speechBox)
        self.speechBox.hide()

        # set control Layout
        self.controLayout = QHBoxLayout()
        self.button1 = Button1()
        self.button2 = Button2()
        self.controLayout.addWidget(self.button1)
        self.controLayout.addLayout(self.playLayout)
        self.controLayout.addWidget(self.button2)
        # set info Layout
        self.infoLayout = QHBoxLayout()
        text = '<font color="blue">Hello</font> <font color="red">World</font><font color="green">!</font>'
        self.infoLabel = QLabel(text)
        self.infoLayout.addStretch()
        self.infoLayout.addWidget(self.infoLabel)
        self.infoLayout.addStretch()

        # set main layout
        self.mainLayout.addLayout(self.controLayout)
        self.mainLayout.addLayout(self.infoLayout)

    def setLabelInfo(self, text=None):
        """ set text in the label info """
        if text is not None:
            self.infoLabel.setText(text)

    def setMode(self, mode=None):
        """ set mode """
        if mode is None:
            return False

        if mode is SAY_MODE_1:
            self.speechBox.show()
            self.subBox.hide()
        elif mode is PLAY_MODE_SUB:
            self.subBox.show()
            self.speechBox.hide()

        self.button1.setMode(mode=mode)
        self.button2.setMode(mode=mode)

    def initWords(self, frame=None, mode=None):
        """ init """
        if frame is None:
            return False

        self.subBox.initWords(frame=frame)
        self.speechBox.initWords(frame=frame)
        self.setMode(mode=mode)

    def setKey(self, key=None):
        """ proccess key received """
        if key is None:
            return False
        self.infoLabel.setText(key)

    def playSpeech(self, words=None):
        """ play speech """
        if words is None:
            return False

        self.speechBox.playSpeech(words=words)
        return True


class MainWindow(QMainWindow):
    """ Main Windows """
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setWindowTitle("PyTedict")
        self.createUi()

    def createUi(self):
        """ set up the user interface """
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.main_layout = QVBoxLayout()

        # create video widget
        self.panelBox = PanelBox()

        # addingo to main layout
        # self.main_layout.addLayout(self.subBox)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.panelBox)
        self.widget.setLayout(self.main_layout)

        # frames
        self.frames = FramesTed(f_json="Frames_ted.json")
        fm = self.frames.get_current_frame()
        self.panelBox.initWords(frame=fm, mode=PLAY_VIDEO)
        # self.subWdg.initWords(frame=fm)
        # self.subWdg.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(640, MAXIMUM_HEIGT_LABEL * 2)
    player.show()
    sys.exit(app.exec_())
