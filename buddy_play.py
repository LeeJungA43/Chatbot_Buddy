import requests
import cognitive_face as CF
from play_audio import play_audio
from recode_audio import recode_audio
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import pyaudio
import wave
import time
import random
import RPi.GPIO as GPIO
from picamera import PiCamera

# Azure Speech 서비스 key와 지역 할당
speech_key, service_region = "PASTE YOUR KEY", "koreacentral"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Face Recogntion
KEY = "PASTE YOUR KEY"
CF.Key.set(KEY)
BASE_URL = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)
happiness, anger, contempt, disgust, fear, sadness = [0, 0, 0, 0, 0, 0]
img_url = './emotions/frame.png'
camera = PiCamera()

# STT/TTS 사전 설정. 한국어와 여성의 음성을 선택
speech_config.speech_synthesis_language = "ko-KR"
speech_config.speech_synthesis_voice_name = "ko-KR-SunHiNeural"

count = 0
start_check = 0
break_check = 0
motion = 0

# PIR 사전 설정
GPIO.setmode(GPIO.BCM)
pirPin = 7
GPIO.setup(pirPin, GPIO.IN, GPIO.PUD_UP)

while True:
    # PIR 센서 반응을 기다림. 그리고 만약 반응이 있으면 if로 넘어감.
    
    if GPIO.input(pirPin) == GPIO.LOW:
        motion = 1
    else:
        motion = 0

    # 버디 앞에 사람이 왔을 때
    while motion == 1:
        
        # PI camera & Face API 실행
        camera.capture('/home/pi/image.jpg')
        faces = CF.face.detect(img_url, True, False, "age, gender, emotion")
        for i in faces:
            happiness = i['faceAttributes']['emotion']['happiness']
            anger = i['faceAttributes']['emotion']['anger']
            contempt = i['faceAttributes']['emotion']['contempt']
            disgust = i['faceAttributes']['emotion']['disgust']
            fear = i['faceAttributes']['emotion']['fear']
            sadness = i['faceAttributes']['emotion']['sadness']
        bad_expression = anger + contempt + disgust + fear + sadness
        
        if happiness < bad_expression: # 우울해 보일 때
            # 무슨 일이 있으신가요? 기분이 안좋아보여요. 제가 도울 수 있는게 있으면 말해주세요.
            play_audio("./audio/Opening.wav")
            start_check = 1
        else: # 우울해 보이지 않을 땐 버디 이름을 부를때까지 대기
            recode_audio(5)
            audio_input = speechsdk.AudioConfig(filename="./audio/user_voice.wav")
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                           language="ko-KR", audio_config=audio_input)
            the_question = speech_recognizer.recognize_once_async().get()
            if '버디' in the_question.text:  # 이름을 불렀을 때
                # 네, 부르셨나요?
                play_audio("./audio/call_name.wav")
                start_check = 1

        # 우울해보이거나 버디 이름을 불렀을 때
        while start_check == 1:
            #음성 녹음
            recode_audio(10)
            
            # 반복적 Face API 실행
            camera.capture('/home/pi/image.jpg')
            faces = CF.face.detect(img_url, True, False, "age, gender, emotion")
            for i in faces:
                happiness = i['faceAttributes']['emotion']['happiness']
                anger = i['faceAttributes']['emotion']['anger']
                contempt = i['faceAttributes']['emotion']['contempt']
                disgust = i['faceAttributes']['emotion']['disgust']
                fear = i['faceAttributes']['emotion']['fear']
                sadness = i['faceAttributes']['emotion']['sadness']
            bad_expression = anger + contempt + disgust + fear + sadness

            # STT API로 사용자의 발화를 문자로 변환
            audio_input = speechsdk.AudioConfig(filename="./audio/user_voice.wav")
            speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                           language="ko-KR", audio_config=audio_input)
            the_question = speech_recognizer.recognize_once_async().get()

            # 해당 .py 파일이 있는 곳에 audio 파일을 만들어두고 필요한 음성은 미리 저장해둘 것!
            if '종료' in the_question.text:  # 종료를 원할 때
                # 네. 종료하겠습니다.
                play_audio("./audio/end.wav")
                count = 0
                break_check = 1
                start_check = 0
                break

            elif '음악' in the_question.text:  # 음악 재생을 바랄 때
                # 음악을 재생합니다.
                play_audio("./audio/music_start.wav")

                # 음악 폴더에서 랜덤 음악 재생
                music_num = random.randrange(1, 10)
                play_audio("./music/music_" + str(music_num) + ".wav")

                count = 0
                break_check = 1
                start_check = 0
                break

            elif count > 10:  # 기준 수치 초과
                # 마음이 소란 스러울 때, 듣기 좋은 음악을 들어보시는 건 어떤가요? 원하신다면 음악 틀어줘, 라고 말해주세요.
                play_audio("./audio/suggestion.wav")

            else:
                data = dict()
                data['question'] = {"question": str(the_question.text)}

                # API 사용. params을 전송
                res = requests.post('<API가 실행되는 주소>', json=data)
                response = res.json()
                print(response['response'])

                # 응답받은 문자열을 TTS를 통해 음성으로 변환
                audio_config = AudioOutputConfig(filename="./audio/response.wav")
                synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
                synthesizer.speak_text_async(response['response'])

                play_audio("./audio/response.wav")

                count = count + 1

        # 우울해 보이지 않거나, 버디를 부르지 않고 자리를 떴을 때 다시 대기 상태로 돌입하기 위해 while문 탈출
        if GPIO.input(pirPin) == GPIO.LOW:
            motion = 1
        else:
            motion = 0

    if break_check == 1:
        break_check = 0
        break
