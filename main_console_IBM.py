# This is a sample Python script.
import json

import pyttsx3
import speech_recognition as sr
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import ApiException
from ibm_watson import AssistantV2

# default values
apiKey = '3wzqnO6g5i07plIGHOknaVrpvFpGrxn2yZDTtODtYjwM'
serviceURL = 'https://api.eu-de.assistant.watson.cloud.ibm.com/instances/33def831-08fe-4325-a3a7-8e17ef26ccae'
version = '2021-06-14'
assisstantID = 'ed016102-9fae-4fe5-849e-32753872f9fb'
#

try:
    # Invoke a method

    authenticator = IAMAuthenticator(apikey=apiKey)
    assistant = AssistantV2(version=version, authenticator=authenticator)
    assistant.set_service_url(service_url=serviceURL)

    response = assistant.create_session(
        assistant_id=assisstantID
    ).get_result()

    # sessionid is retrieved on successful auth
    sessionId = json.loads(json.dumps(response))['session_id']
    print("session id: " + sessionId + "\n")
except Exception as ex:
    print("Failed to establish connection: " + repr(ex))




# files handling
engine = pyttsx3.init()  # for tts
engineToFile = pyttsx3.init() # for mp3 file
textFile = open("speachToText.txt", "a")  # create & append
# to store 'texts' for 'speech.mp3'
store = ""


def stt():
    # speech to text
    r = sr.Recognizer()

    with sr.Microphone() as mic:

        while 1:
            try:

                tts('you can speak now!')

                audio_data = r.record(mic, duration=5)

                # used google since pocketphinx(offline) was not as accurate as i needed it to be.
                text = r.recognize_google(audio_data)
                val = ibm(text=text)

                if val == 1:
                    return

            except ApiException as e:
                print('process failed with exception' + repr(e) + str(e.code) + ": " + e.message)
            except sr.UnknownValueError:
                tts('Audio is Unintelligible, Try again...')
            except Exception as f:
                print('process failed with exception' + repr(f))


def ibm(text):

    res = assistant.message(
        assistant_id=assisstantID,
        session_id=sessionId,
        input={'message_type': 'text',
               'text': text
               }
    ).get_result()
    print(json.dumps(res, indent=2) + "\n" + "\n")
    print(text + "\n")

    # quit command
    tts(json.loads(json.dumps(res))['output']['generic'][0]['text'])
    if 'thanks, bye.' == json.loads(json.dumps(res))['output']['generic'][0][
        'text'] or 'thank you for using the Assistant.' == json.loads(json.dumps(res))['output']['generic'][0][
        'text']:
        return 1


def tts(text):
    # text to speech
    engine.say(text)
    tostore(text, store)
    tofile("Assistant: " + text + "\n")
    print("Assistant: " + text + "\n")
    engine.runAndWait()


# concat texts for further operations
def tostore(text, st=store):
    st = st + text + "\n"


# save communication to file
def tofile(text):
    if textFile.writable():
        textFile.write(text + "\n")
        textFile.flush()


# save to speech.mp3
def ttsTofile(text):
    engineToFile.save_to_file(text, "speech.mp3")
    engineToFile.runAndWait()


print('wait...')

# launch speech to text first
stt()

# store values and close
tofile(store)
ttsTofile(store)
textFile.close()
