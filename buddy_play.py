import requests
import cognitive_face as CF
from play_audio import play_audio
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech import AudioDataStream, SpeechConfig, SpeechSynthesizer, SpeechSynthesisOutputFormat
from azure.cognitiveservices.speech.audio import AudioOutputConfig

# Azure Speech 서비스 key와 지역 할당
speech_key, service_region = "1d5adb57698441c4a0ae848fc8c565c7", "koreacentral"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

# STT/TTS 사전 설정. 한국어와 여성의 음성을 선택
speech_config.speech_synthesis_language = "ko-KR"
speech_config.speech_synthesis_voice_name = "ko-KR-SunHiNeural"

count = 0
break_check = 0

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
    """
    Face API 실행 구문 (def로 face_chapture 함수를 만들어 사용하는 것이 간편)
    """

    # if anger > 0.5 or contempt > 0.5 or distgust > 0.5 or fear > 0.5 or sadness > 0.5:
    # 부정적 감정이 50% 이상이라고 나타날 때(아니면 다섯개 합한게 50% 이상이어도 괜찮을듯)
        # 무슨 일이 있으신가요? 기분이 안좋아보여요. 제가 도울 수 있는게 있으면 말해주세요.
        #play_audio("./audio/Opening.wav")

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
            res = requests.post('<API가 실행되는 IP Adress>', json=data)
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
