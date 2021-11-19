import requests
from time import sleep
"""
필요 import
"""

run_check = 0
silence = 0
state = 0.0

# 첫번째 while 문
# PIR 부분을 채운다면 그 아래의 두번째 while문 전체를 이 안으로
"""
PIR 센서 동작부분
"""

# 두번째 while 문
# PIR 센서가 동작하면 작동하는 부분.
# while 반복문 조건은 PIR에 반응이 있느냐, 없느나
while True:
    if (run_check == 0): # 0은 대기중이란 뜻
        """
        녹음 & 촬영
        """

        # 파이썬 딕셔너리 형식으로 file 설정
        files = {"images": open('./emotions/test01.png', 'rb'),
                 "wave": open('./test/buddytest06.wav', 'rb'),
                 "state": str(state)}

        # API 사용. file을 전송
        res = requests.post('http://52.231.8.193:5000/standby', files=files)
        response = res.json()

        # 사용자 표정이 안좋을땐
        print(response['response'])
        run_check = int(response['run_check'])
        state = float(response['state'])
    else: # run_check = 1 = 대화를 시작했다
        """
        녹음 & 촬영
        """

        # 파이썬 딕셔너리 형식으로 file 설정
        files = {"images": open('./emotions/test01.png', 'rb'),
                 "wave": open('./test/buddytest01.wav', 'rb'),
                 "state": str(state),
                 "silence": str(silence)}

        # API 사용. file을 전송
        res = requests.post('http://52.231.8.193:5000/chatbot', files=files)
        response = res.json()

        # 사용자 표정이 안좋을땐
        if int(response['music']) == 1:
            # 음악을 재생
            print(response['response'])
            run_check = int(response['run_check'])
            state = float(response['state'])
            silence = int(response['silence'])

        # 침묵이 1분 가량 지속
        elif silence > 5:
            print("대기모드 상태로 돌입")
            run_check = 0
            state = 0

        # 대화
        else:
            print(response['response'])
            run_check = int(response['run_check'])
            state = float(response['state'])
            silence = int(response['silence'])

    if silence == 0:
        # 종료나 음악 키워드로 빠져나왔을 시 바로 말을 걸면 안되니 일정시간 대기
        sleep(10)

    # PIR에서 감지되는 인물이 사라지면 두번째 while문 탈출
