import wiotp.sdk.device
import time
import os
import datetime
from ibm_watson import TextToSpeechV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import playsound

authenticator = IAMAuthenticator('1uMWLtaB5gI6HluwS47oy1uqDOmJeLJICi7B-ECWOtT6')
text_to_speech = TextToSpeechV1(
    authenticator=authenticator
    )

text_to_speech.set_service_url('https://api.eu-gb.text-to-speech.watson.cloud.ibm.com/instances/43e154dd-ff43-4304-a48b-5ea87abdf7cd')

myConfig = {
    "identity": {
        "orgId": "unneo9",
        "typeId": "ESP32",
        "deviceId": "12345"

    },
    "auth": {
        "token": "12345678"
    }
}
client=wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
client.connect()


def myCommandCallback(cmd):
    print("Message received from IBM IO Platform: %s" % cmd.data['command'])
    m=cmd.data['command']
    with open('medicine.mp3', 'wb') as audio_file:
        audio_file.write(
            text_to_speech.synthesize(
                'You have to take '+m+' medicine now',
                voice='en-US_AllisonV3Voice',
                accept='audio/mp3'
            ).get_result() .content)
    playsound.playsound('medicine.mp3')
    os.remove('medicine.mp3')
while True:
        client.commandCallback = myCommandCallback
client.disconnect()

                                                                 
