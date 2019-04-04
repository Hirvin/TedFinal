#! /usr/bin/python3

import json

HEAD_F = "header"
FRAMES_F = "frames"
FM_WORDS = "words"
FM_WORDS_TEXT = "word"
END_FRAME_TIME = "end_time"
INIT_FRAME_TIME = "start_time"
FM_OFFSET = "offset"


class FramesTed(object):
    """ Frames from subtitles """
    def __init__(self, f_json=None):
        if f_json is not None:
            with open(f_json, "r") as j_file:
                self.__FramesData = json.load(j_file)
                self.__index = 0
                self.__n_frames = len(self.__FramesData[FRAMES_F])
                self.__f_json = f_json
        else:
            self.__FramesData = None

    def get_head(self):
        """ return head """
        if self.__FramesData is None:
            return None

        return self.__FramesData[HEAD_F]

    def get_frames(self):
        """ return Frames """
        if self.__FramesData is None:
            return None

        return self.__FramesData[FRAMES_F]

    def get_current_frame(self):
        if self.__FramesData is None:
            return None

        return self.__FramesData[FRAMES_F][self.__index]

    def next_frame(self):
        """ set next frame """
        if self.__FramesData is None:
            return False

        if (self.__index + 1) < self.__n_frames:
            self.__index += 1
            return True

        return False

    def prev_frame(self):
        """ set prev frame """
        if self.__FramesData is None:
            return False

        if self.__index > 0:
            self.__index -= 1
            return True

        return False

    def save(self):
        """ save """
        if self.__FramesData is None:
            return False

        with open(self.__f_json, "w") as j_file:
            json.dump(self.__FramesData, j_file)

    # times
    def getEndTime(self):
        """ return end Time """
        return self.__FramesData[FRAMES_F][self.__index][END_FRAME_TIME]

    def getInitTime(self):
        """ return init time """
        return self.__FramesData[FRAMES_F][self.__index][INIT_FRAME_TIME]

    def getOffset(self):
        """ return offset """
        return self.__FramesData[HEAD_F][FM_OFFSET]

    def get_text_from_frame(self):
        """ return text from current frame"""
        if self.__FramesData is None:
            return None

        words = self.__FramesData[FRAMES_F][self.__index][FM_WORDS]

        wordLst = []
        for word in words:
            if word is not None:
                wordLst.append(word[FM_WORDS_TEXT])
        return " ".join(wordLst)
