import base64
import requests
from time import sleep
from play_audio import play_audio
"""
필요 import
"""

run_check = 0

# 첫번째 while 문
# PIR 부분을 채운다면 그 아래의 두번째 while문 전체를 이 안으로
"""
PIR 센서 동작부분
"""

# 두번째 while 문
# PIR 센서가 동작하면 작동하는 부분.
# while 반복문 조건은 PIR에 반응이 있느냐, 없느냐로 수정해야 함
while True:
    if (run_check == 0): # 0은 대기중이란 뜻
        """
        녹음 & 촬영
        """

        # 대화가 한 번 종료됐다가 다시 돌아왔을 경우, 상태정보와 침묵정보를 초기화 해야 하므로 여기서 선언
        state = 0.0
        silence = 0

        # 파이썬 딕셔너리 형식으로 보낼 file 설정
        files = {"images": open('<png 위치 및 파일 이름>', 'rb'),
                 "wave": open('<사용자 음성 녹음 wav 위치 및 파일 이름>', 'rb'),
                 "state": str(state)}

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

        # 버디의 답변 재생
        play_audio('./audio/response.wav')
    else: # run_check = 1 = 대화를 시작했다
        """
        녹음 & 촬영
        """

        # 파이썬 딕셔너리 형식으로 보낼 file 설정
        files = {"images": open('<png 위치 및 파일 이름>', 'rb'),
                 "wave": open('<사용자 음성 녹음 wav 위치 및 파일 이름>', 'rb'),
                 "state": str(state),
                 "silence": str(silence)}

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

        play_audio('./audio/response.wav')

        if music == 1:
            # 음악을 재생
            play_audio('./music/music'+'.wav')

        # 침묵이 3분 가량 지속된 것
        # 사용자가 대화하고 싶지 않은 상태라고 판단
        elif silence > 15:
            # 대기모드 상태로 돌입하므로 run_check와 state를 초기화한다
            run_check = 0
            state = 0

    if silence <= 15:
        # 침묵으로 빠져나온 것이 아니라, 종료나 음악 키워드로 빠져나온 상태
        # 사용자가 버디 종료를 원한 것이므로 바로 말을 걸면 안되니 일정시간 대기한다
        # 임의로 10분(600초)으로 설정했다.
        sleep(600)

    # PIR에서 감지되는 인물이 사라지면 두번째 while문 탈출
