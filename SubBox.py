#! /usr/bin/python3
import sys
import re
from Frames import FramesTed, FM_WORDS, FM_WORDS_TEXT
from PyQt5.QtCore import pyqtSignal
from TedCommon import NUMBER_LB_TOTAL, NUMBER_LB_LINE, MAXIMUM_HEIGT_LABEL
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget,\
    QVBoxLayout, QHBoxLayout, QLabel

# Globa regex
REPLACE_WORD_TO_ASTERISC = r"[a-zA-Z0-9]"
# REPLACE_WORD_TO_DICTIONARY = r"[/,/./-/_]"
POINTER_WORD = '*'


class SubLabel(QLabel):
    """ Subtitle Label Class """
    def __init(self, parent=None):
        super(SubLabel, self).__init__(parent)
        self.setMaximumHeight(MAXIMUM_HEIGT_LABEL)
        self.text = " "
        # self.textDsply = " "
        self.lst_chr = []

    def clear(self):
        """ clear """
        self.text = " "
        # self.textDsply = " "
        self.lst_chr = []

    def displayWord(self, word=None):
        """ display word """
        if word is None:
            return " "

        if self.lst_chr == []:
            return self.text

        re_word = word[::-1]
        re_word = re.sub(r"\w", POINTER_WORD, re_word, len(self.lst_chr))
        return re_word[::-1]

    def displayText(self):
        """ display text """
        self.setText(self.displayWord(self.text))

    def playKey(self, key=None):
        """ play key """
        if self.lst_chr == []:
            return True

        if key is None:
            return False

        if self.lst_chr[0].upper() == key:
            self.lst_chr.pop(0)

        self.displayText()

        if self.lst_chr == []:
            return True

        return False

    def init(self, word=None):
        """ init Sub Label """
        self.clear()
        if word is not None:
            self.text = word
            self.lst_chr = list(re.sub(r'[\W]', '', word))
            # self.textDsply = re.sub(REPLACE_WORD_TO_ASTERISC, POINTER_WORD, word)
            # self.setText(self.displayWord(self.text))
            self.displayText()


class SubWdg(QWidget):
    """ video widget class """
    subtitleFrameComplete = pyqtSignal()

    def __init__(self, parent=None):
        super(SubWdg, self).__init__(parent)
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
            lst.append(SubLabel())
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
                self.lstLabels[index].init(word[FM_WORDS_TEXT])
                self.lstPlay.append(self.lstLabels[index])
            else:
                self.lstLabels[index].init(" ")

    def playKey(self, key=None):
        """ play key """
        if self.lstPlay == []:
            # print ("Palabras completas")
            self.subtitleFrameComplete.emit()
            return True

        if self.lstPlay[0].playKey(key=key) is True:
            self.lstPlay.pop(0)

        if self.lstPlay == []:
            # print ("Palabras completas")
            self.subtitleFrameComplete.emit()
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
        self.subWdg = SubWdg()
        self.subWdg2 = SubWdg()

        # addingo to main layout
        # self.main_layout.addLayout(self.subBox)
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.subWdg)
        self.main_layout.addWidget(self.subWdg2)
        self.widget.setLayout(self.main_layout)

        # frames
        self.frames = FramesTed(f_json="Frames_ted.json")
        fm = self.frames.get_current_frame()
        self.subWdg.initWords(frame=fm)
        self.subWdg2.initWords(frame=fm)
        self.subWdg.hide()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(640, MAXIMUM_HEIGT_LABEL * 2)
    player.show()
    sys.exit(app.exec_())
