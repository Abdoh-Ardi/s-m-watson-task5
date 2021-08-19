# This is a sample Python script.
import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()  # for tts

textFile = open("speachToText.txt", "a")  # create & append


def stt():
    # speech to text
    r = sr.Recognizer()

    with sr.Microphone() as mic:
        print('press enter key to exit..')

        try:
            print('you can speak now!\n for 5 seconds..')
            audio_data = r.record(mic, duration=5)

            # used google since pocketphinx(offline) was not as accurate as i needed it to be.
            text = r.recognize_google(audio_data)
            tofile(text)
        except sr.UnknownValueError as e:
            tofile('audio is unintelligible')
        except Exception as e:
            print(repr(e))


def tofile(text):
    if textFile.writable():
        textFile.write(text + "\n")
        textFile.flush()
    tts(text)


def tts(text):
    # text to speech

    engine.save_to_file(text, "speech.mp3")
    engine.runAndWait()


print('Loading, please wait...')
stt()
textFile.close()  # close file
