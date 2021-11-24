#This is for PC version
#Before executing this code, You must install opencv-python library first.
import base64
import requests
from time import sleep
import cv2
import os
from recode_audio import recode_audio
from play_audio import play_audio
import random

run_check = 0

camera = cv2.VideoCapture(0)

while True:
    print("녹음 시작")
        #녹음
    recode_audio(5)

    print("촬영 시작")
    #촬영
    ret, image = camera.read()
    cv2.imwrite("emotions/frame.png", image)
    img_url = './emotions/frame.png'

    if (run_check == 0): # 0은 대기중이란 뜻
        
        # 대화가 한 번 종료됐다가 다시 돌아왔을 경우, 상태정보와 침묵정보를 초기화 해야 하므로 여기서 선언
        state = 0.0
        silence = 0

        # 파이썬 딕셔너리 형식으로 보낼 file 설정
        files = {"images": open(img_url, 'rb'),
                 "wave": open('./audio/user_voice.wav', 'rb'),
                 "state": str(state)}
        print("전송 시작")
        # API 사용. file을 서버로 전송
        res = requests.post('<API 주소>', files=files)
        # json dict() 형식으로 return 되어오는 데이터를 받는다.
        data = res.json()

        # str 형식으로 전달받은 wav 데이터(key: response)를 다시 바이너리로 변환
        # 이때 문자열 앞뒤로 b' ' 붙어있는 걸 떼줘야 한다
        encode = data['response'][2:-1]
        decode = base64.b64decode(encode)

        # buddy의 답변 저장
        f = open('./audio/response.wav', 'wb')
        f.write(decode)
        f.close()

        # 대화를 시작할지 체크
        # run_check가 1이 되면 다시 반복될 때 else 부분으로 넘어간다
        run_check = int(data['run_check'])
        state = float(data['state'])

        print("답변 재생 시작")
        # 버디의 답변 재생
        play_audio('./audio/response.wav')
    else: # run_check = 1 = 대화를 시작했다
        # 파이썬 딕셔너리 형식으로 보낼 file 설정
        files = {"images": open(img_url, 'rb'),
                 "wave": open('./audio/user_voice.wav', 'rb'),
                 "state": str(state),
                 "silence": str(silence)}

        print("전송 시작")
        # API 사용. file을 서버로 전송
        res = requests.post('<API 주소>', files=files)
        data = res.json()

        # str 형식으로 전달받은 wav 데이터(key: response)를 다시 바이너리로 변환
        # 이때 문자열 앞뒤로 b' ' 붙어있는 걸 떼줘야 한다
        encode = data['response'][2:-1]
        decode = base64.b64decode(encode)

        # buddy의 답변 저장
        f = open('./audio/response.wav', 'wb')
        f.write(decode)
        f.close()

        # 상태에 관한 정보들 갱신
        run_check = int(data['run_check'])
        state = float(data['state'])
        silence = int(data['silence'])
        music = int(data['music'])
        
        print("답변 재생 시작")    
        play_audio('./audio/response.wav')

        if music == 1:
            print("음악")
            # 음악을 재생
            n = random.randrange(1, 7)
            play_audio('./music/music'+n+'.wav')

        # 침묵이 3분 가량 지속된 것
        # 사용자가 대화하고 싶지 않은 상태라고 판단
        elif silence > 15:
            # 대기모드 상태로 돌입하므로 run_check와 state를 초기화한다
            run_check = 0
            state = 0

    if run_check==0 & silence <= 15:
        print("종료")
        # 침묵으로 빠져나온 것이 아니라, 종료나 음악 키워드로 빠져나온 상태
        # 사용자가 버디 종료를 원한 것이므로 바로 말을 걸면 안되니 일정시간 대기한다
        # 임의로 10분(600초)으로 설정했다.

        sleep(600)

if os.path.isfile(img_url):
    os.remove(img_url)
camera.release()
cv2.destroyAllWindows()