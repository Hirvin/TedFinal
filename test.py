#! /usr/bin/python3
import sys
import vlc
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QFrame,\
    QVBoxLayout, QSlider

VIDEO_TIMER_INTERVAL = 500


class VideoWgt(QVBoxLayout):
    """ video widget class """
    def __init__(self, parent=None):
        super(VideoWgt, self).__init__(parent)
        # vlc code
        # creating vlc instance
        self.instance = vlc.Instance()
        # creating vlc media player
        self.media_player = self.instance.media_player_new()

        # internal vairables
        self.__end_time = 0

        self.createUi()
        self.openVideo()

    def play(self, init_time=None, end_time=None):
        """ play video """
        if not self.media_player.is_playing():
            if end_time is not None:
                self.__end_time = end_time
                self.timer.start()

            self.media_player.play()
            self.timer_slider.start()

            if init_time is not None:
                print ("set time")
                self.media_player.set_time(100000)

    def stop(self):
        """ stop video """
        if self.media_player.is_playing():
            self.media_player.stop()
            self.timer_slider.stop()

    def pause(self):
        """ pause video """
        if self.media_player.is_playing():
            self.media_player.pause()
            self.timer_slider.stop()

    def createUi(self):
        """ set up the user interface """
        self.videoframe = QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor(QPalette.Window,
                              QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        # slider
        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setToolTip("Position")
        self.position_slider.setMaximum(1000)

        # set timer
        self.timer = QTimer(self)
        self.timer.setInterval(500)
        self.timer.timeout.connect(self.updateTime)
        self.timer_slider = QTimer(self)
        self.timer_slider.setInterval(200)
        self.timer_slider.timeout.connect(self.updateSlider)

        # layout
        self.addWidget(self.videoframe)
        self.addWidget(self.position_slider)

    def openVideo(self):
        """ open video """
        filename = "/home/hirvin/Documents/Myprojects/TED/video.mp4"
        # create the media
        if sys.version < '3':
            filename = unicode(filename)

        self.media = self.instance.media_new(filename)
        self.media_player.set_media(self.media)
        self.media.parse()
        print (self.media.get_duration())
        self.media_player.set_xwindow(self.videoframe.winId())
        # time.sleep(15)
        self.play(end_time=None, init_time=100000)
        # self.timer.start()

    def updateTime(self):
        """ update time of video """
        current_time = self.media_player.get_time()
        print (current_time)
        if current_time > self.__end_time:
            self.pause()
            self.timer.stop()

    def updateSlider(self):
        """ update slider """
        self.position_slider.setValue(self.media_player.get_position() * 1000)


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
        self.video_wgt = VideoWgt()

        # addingo to main layout
        self.main_layout.addLayout(self.video_wgt)

        self.widget.setLayout(self.main_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = MainWindow()
    player.resize(640, 480)
    player.show()
    sys.exit(app.exec_())
