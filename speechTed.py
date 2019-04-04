#! /usr/bin/python3

import speech_recognition as sr
import diff_match_patch as dmp_module

# ql->setText('<font color="blue">Hello</font> <font color=\"red\">World</font><font color=\"green">!</font>);


def get_audio():
    """ get audio from microphone """
    # obtain audio from the microphone
    record = sr.Recognizer()
    with sr.Microphone() as source:
        print ("Say something!")
        audio = record.listen(source)
        return audio
    return None

def get_speech():
    """ get speech from audio """
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    # recognize speech using Sphinx
    try:
        # for testing purposes, we're just using the default API key
        # instead of `r.recognize_google(audio)`
        speechText = str(r.recognize_google(audio))
        print("Google Speech Recognition thinks you said " + speechText)
        return speechText
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


def get_differences(originalText=None, speechText=None):
    """ get diferences """
    if originalText is None:
        return None

    if speechText is None:
        return None

    dmp = dmp_module.diff_match_patch()
    diff = dmp.diff_main(speechText, originalText)
    dmp.diff_cleanupSemantic(diff)

    wordLst = []
    for words in diff:
        if words[0] is 0:
            for word in words[1].split(" "):
                # print (f"0: {word}")
                wordLst.append(word)

    return wordLst


if __name__ == '__main__':
    # print ("say something ...")
    # audio = get_audio()
    # print ("record is completed")
    # record = sr.Recognizer()
    # print (record.recognize_google_cloud(audio))

    # obtain audio from the microphone
    speech = get_speech()
    print (get_differences(originalText="this is a test for audio library", speechText=speech))

