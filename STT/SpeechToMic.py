#!/usr/bin/env python
# coding: utf-8

# In[22]:


pip install azure-cognitiveservices-speech


# In[18]:


pip install --upgrade pip


# In[19]:


pip install azure-cognitiveservices-speech


# In[20]:


import azure.cognitiveservices.speech as speechsdk


# In[ ]:





# In[23]:



def from_mic():
    speech_key, service_region = "c248d3d2b78b4c9593fcc445d92a5bbf", "koreacentral"
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.speech_recognition_language="ko-KR"
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)
    
    print("말하세요:")
    result = speech_recognizer.recognize_once_async().get()
    print(result.text)
     
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        print("Recognized: {}".format(result.text))
    elif result.reason == speechsdk.ResultReason.NoMatch:
        print("No speech could be recognized: {}".format(result.no_match_details))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech Recognition canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            print("Error details: {}".format(cancellation_details.error_details))

from_mic()


# In[ ]:





# In[ ]:





# In[ ]:




