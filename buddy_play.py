import requests
import cognitive_face as CF
import cv2
from play_audio import play_audio
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# Azure Speech 서비스 key와 지역 할당
speech_key, service_region = "1d5adb57698441c4a0ae848fc8c565c7", "koreacentral"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# Face Recogntion
KEY = "PASTE YOUR KEY"
CF.Key.set(KEY)

BASE_URL = 'https://koreacentral.api.cognitive.microsoft.com/face/v1.0/'
CF.BaseUrl.set(BASE_URL)

camera = cv2.VideoCapture(0)

# STT/TTS 사전 설정. 한국어와 여성의 음성을 선택
speech_config.speech_synthesis_language = "ko-KR"
speech_config.speech_synthesis_voice_name = "ko-KR-SunHiNeural"

count = 0
break_check = 0

def face_capture():
    while True:
        ret, image = camera.read()
        happiness, anger, contempt, disgust, fear, sadness =[0, 0, 0, 0, 0, 0]
        if(int(camera.get(1)) % 60 == 0):
            print('Saved image ' + str(int(camera.get(1))))
            cv2.imwrite("emotions/frame.png", image)
            img_url = './emotions/frame.png'
            faces = CF.face.detect(img_url, True, False, "age, gender, emotion")

            for i in faces:
                happiness = i['faceAttributes']['emotion']['happiness']
                anger = i['faceAttributes']['emotion']['anger']
                contempt = i['faceAttributes']['emotion']['contempt']
                disgust = i['faceAttributes']['emotion']['disgust']
                fear = i['faceAttributes']['emotion']['fear']
                sadness = i['faceAttributes']['emotion']['sadness']

            #사진 삭제
            if os.path.isfile(img_url):
                    os.remove(img_url)
               
            return happiness, anger, contempt, disgust, fear, sadness

while True:
    # PIR 센서 반응을 기다림. 그리고 만약 반응이 있으면 if로 넘어감.
    """
    Python에서 PIR 센서 동작하는 란
    """
    # if pir 반응이 있을 때 조건으로 해서, 아래 전부를 if란 안에 넣기.
    """
    if 구문
    """

    # 마이크 동작
    """
    음성이 잡힐 때 까지 동작
    """

    # Face API 실행

    happiness, anger, contempt, disgust, fear, sadness = face_capture()
    bad_expression = anger + contempt + disgust + fear + sadness
    
    if happiness < bad_expression:
        # 무슨 일이 있으신가요? 기분이 안좋아보여요. 제가 도울 수 있는게 있으면 말해주세요.
        play_audio("./audio/Opening.wav")
        camera.release()
        cv2.destroyAllWindows()

    # 마이크 녹음 동작. 음성이 잡힐 때 까지 대기. 잡히면 wav 파일 생성.
    """
    마이크 대기 및 녹음 구문
    """

    # 후일 이 부분의 조건을 wav 파일이 저장되었을 때, 로 수정해야 함
    while True:
        # 반복적 Face API 실행
        """
        Face API 실행 구문
        """

        # 반복적 마이크 녹음
        """
        마이크 대기 및 녹음 구문
        """

        # STT API로 question 발화를 문자로 변환. 파일 이름 수정 필요.
        audio_input = speechsdk.AudioConfig(filename="./audio/buddytest04.wav")
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,
                                                       language="ko-KR", audio_config=audio_input)
        the_question = speech_recognizer.recognize_once_async().get()

        # 해당 .py 파일이 있는 곳에 audio 파일을 만들어두고 필요한 음성은 미리 저장해둘 것!
        if '종료' in the_question.text:  # 종료를 원할 때
            # 네. 종료하겠습니다.
            play_audio("./audio/end.wav")
            count = 0
            break_check = 1
            
            break

        elif '음악' in the_question.text:  # 음악 재생을 바랄 때
            # 음악을 재생합니다.
            play_audio("./audio/music_start.wav")
            count = 0
            break_check = 1
            break

        elif '버디' in the_question.text:  # 이름을 불렀을 때
            # 네, 부르셨나요?
            play_audio("./audio/call_name.wav")

        elif count > 10: # 기준 수치 초과
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

    if break_check == 1:
        break
