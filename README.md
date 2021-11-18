# 딥러닝 기반 심리안정 음성챗봇 "Buddy"

### 학교다니기힘드시조 유튜브 채널
Link: https://www.youtube.com/channel/UCxddhezhExZczcUuW3oXsRw

### Prototype
학교다니기힘드시조 버디 시연 영상: [https://youtu.be/1pYcX_lvk3s](https://youtu.be/1pYcX_lvk3s) 

학교다니기힘드시조 버디 포스터 세션: [https://youtu.be/PufsP0f8ERM](https://youtu.be/PufsP0f8ERM)

### Check List
[Buddy Model 개발 전]
> - [x] Protortype : https://colab.research.google.com/drive/1lsNvfFOJMP1bbe8FWg5V194kjx9KUCMX?usp=sharing (확인 시 이화인 계정 필요)
> - [x] KoBERT 모델 일반 대화 학습

[Buddy Model 개발]
> - [x] 얼굴인식 API 삽입
> - [x] STT API 삽입
> - [x] 가상서버 or 드라이브 만들기
> - [x] 학습시킨 Model을 API 형태로 서비스화 하기
> - [x] 각 Output들이 서로의 Input이 되도록 코드 연결 
> - [x] Raspberry Pi 탑재

[Model 완성 후]
> - [x] 스피커 3D 디자인 모델링
> - [x] 스피커 3D Printing
> - [x] PIR 센서 감도 조작
> - [x] 스피커 제작

---
Buddy Project
----------------------

### Poroject Repository

Dev repository: https://github.com/LeeJungA43/Chatbot_Buddy

~~Multi-Speaker Tacotron 모델: https://github.com/LeeJungA43/mstt~~

KoBERT를 활용한 채팅봇 모델: https://github.com/LeeJungA43/buddy_KoBERT

### 기술 실행시 참고 글

Face Recognition: https://temp-ha3.tistory.com/3 

STT: https://wanivlog.tistory.com/3 

챗봇: https://github.com/School-is-hard/buddy_KoBERT 의 train 파일 속 Buddy_Chatbot_KoBERT.ipynb

Multi-Speaker-Tacotron: https://lee-jung-ah.tistory.com/1

### POSTER

<img src="/img/poster.jpg" width="800px" title="px(픽셀) 크기 설정" alt="poster"></img><br/>

### 프로젝트의 목적

>기본적으로 현대 청년층의 심리장애 및 우울증 환자 수가 증가하고 있고, 이것이 코로나시대와 겹쳐지면서 '코로나 블루'라는 신조어까지 생기는 상황이다. 이러한 우울증이 병원에 갈 수 없는 한밤중이나 휴일에 심해질 때, 그 곁에서 불안정한 심신을 위로하고 우울감을 조절할 수 있는 조언을 해줄 수 있는 스피커가 있다면 효과적일 것이라 생각했다.
>
>그래서 생각해낸 것이 바로 딥러닝 기반 음성챗봇이다. AIhub에서 제공하는 '웰니스 대화 스크립트 데이터셋'을 사용하여 챗봇을 학습을 시킨다면 우울함을 겪고 있는 사용자에게 적절한 위로의 대답을 할 수 있을 것이라 생각했다. 그리고 텍스트로 대화하는 것 보다는, 실제 음성으로 대화를 하면 더욱 심신 안정에 효과적일 것이라 생각하여 음성챗봇으로 구현하기로 결정했다.


### Project Flow-Chart

![flow chart](https://user-images.githubusercontent.com/71166763/142354835-5473b056-340f-440f-83a2-1976f29320d5.jpg)


### Project Senario

1. 적외선 센서로 사용자의 인기척 감지
2. 사용자의 얼굴을 촬영하여 표정 속 감정 분석
3. 우울함이 감지되면 먼저 말을 걸고, 그렇지 않을 경우 이름을 부를 때 까지 대기
4. 대화가 시작되면 사용자의 발화를 녹음 후 text로 변환
5. 배포한 API를 통해 사용자 발화 목적 분류 및 답변 생성
6. 생성된 답변을 목소리로 변환
7. 스피커를 통해 재생

### Reference

>Multi-Speaker-Tacotron: https://github.com/carpedm20/multi-speaker-tacotron-tensorflow
>
>cognitive-services-speech-sdk: https://github.com/Azure-Samples/cognitive-services-speech-sdk
>
>azure-sdk-for-python: https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/cognitiveservices/azure-cognitiveservices-vision-face
>
>WellnessConversation-LanguageModel: https://github.com/nawnoes/WellnessConversation-LanguageModel


