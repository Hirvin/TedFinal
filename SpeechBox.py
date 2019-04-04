#! /usr/bin/python3
import sys
from Frames import FramesTed, FM_WORDS, FM_WORDS_TEXT
from TedCommon import NUMBER_LB_TOTAL, NUMBER_LB_LINE, MAXIMUM_HEIGT_LABEL
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,\
    QVBoxLayout, QHBoxLayout, QLabel

# CSS styles
CSS_BASE_SAY_COLOR = "QLabel{color: Gray; font-size: 18px; font-weight: bold;}"
CSS_CORRECT_SAY_COLOR = "QLabel{color: Green; font-size: 18px; font-weight: bold;}"


class SpeechLabel(QLabel):
    """ Subtitle Label Class """
    def __init(self, parent=None):
        super(SpeechLabel, self).__init__(parent)
        self.setMaximumHeight(MAXIMUM_HEIGT_LABEL)
        self.text = " "

    def clear(self):
        """ clear """
        self.text = " "

    def init(self, word=None):
        """ init Sub Label """
        self.clear()
        if word is not None:
            self.text = word
            self.setText(word)
            self.setBase()

    def setBase(self):
        """ set base color """
        self.setStyleSheet(CSS_BASE_SAY_COLOR)

    def setCorrect(self):
        """ set Correct color """
        self.setStyleSheet(CSS_CORRECT_SAY_COLOR)



class SpeechWdg(QWidget):
    """ video widget class """
    speechFrameComplete = pyqtSignal()

    def __init__(self, parent=None):
        super(SpeechWdg, self).__init__(parent)
        self.lstPlay = []
        self.createUi()

    def createUi(self):
        """ self create Ui """
        self.subBox = QVBoxLayout()
        self.setLayout(self.subBox)
        self.line1 = QHBoxLayout()
        self.line2 = QHBoxLayout()
        self.lstLabels = self.createLabels()

        # create Ui line 1
        # self.line1.addWidget(self.lb1)
        self.setLabels(parent=self.line1, elements=
                       self.lstLabels[:NUMBER_LB_LINE])

        # create Ui line 2
        # self.line2.addWidget(self.lb2)
        self.setLabels(parent=self.line2, elements=
                       self.lstLabels[NUMBER_LB_LINE:])

        # set layouts
        self.subBox.addLayout(self.line1)
        self.subBox.addLayout(self.line2)

    def createLabels(self):
        """ create Labels """
        lst = []
        for i in range(NUMBER_LB_TOTAL):
            lst.append(SpeechLabel())
        return lst

    def setLabels(self, parent=None, elements=None):
        """ set labels """
        parent.addStretch()
        for e in elements:
            parent.addWidget(e)
        parent.addStretch()

    def initWords(self, frame=None):
        """ init words """
        if frame is None:
            return False

        self.lstPlay = []

        for index, word in enumerate(frame[FM_WORDS]):
            if word is not None:
                # self.setStyleSheet(CSS_BASE_SAY_COLOR)
                self.lstLabels[index].init(word[FM_WORDS_TEXT])
                self.lstPlay.append(self.lstLabels[index])
            else:
                self.lstLabels[index].init(" ")

    def getIndex(self, word=None):
        """ get index from a word in lstwords """
        if word is None:
            return -1

        if self.lstPlay == []:
            return -1

        index = 0
        for e in self.lstPlay:
            if e.text == word:
                return index
            index += 1
        return -1

    def playSpeech(self, words=None):
        """ play key """
        if self.lstPlay == []:
            # print ("Palabras completas")
            self.speechFrameComplete.emit()
            return True

        if words is None:
            return False

        # if self.lstPlay[0].playKey(key=key) is True:
        #     self.lstPlay.pop(0)
        # ["foo", "bar", "baz"].index("bar")
        for word in words:
            index = self.getIndex(word=word)
            if index >= 0:
            # if word in self.lstPlay:
            #     index = self.lstPlay.index(word)
                self.lstPlay[index].setCorrect()
                self.lstPlay.pop(index)

        if self.lstPlay == []:
            # print ("Palabras completas")
            self.speechFrameComplete.emit()
            return True

        return False


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
        self.speechWdg = SpeechWdg()
        # self.subWdg2 = SubWdg()

        # addingo to main layout
        # self.main_layout.addLayout(self.subBox)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.speechWdg)
        #self.main_layout.addWidget(self.subWdg2)
        self.widget.setLayout(self.main_layout)

        # frames
        self.frames = FramesTed(f_json="Frames_ted.json")
        fm = self.frames.get_current_frame()
        self.speechWdg.initWords(frame=fm)
        # self.subWdg2.initWords(frame=fm)
        # self.speechWdg.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(640, MAXIMUM_HEIGT_LABEL * 2)
    player.show()
    sys.exit(app.exec_())
