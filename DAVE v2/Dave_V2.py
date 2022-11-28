import speech_recognition as sr
import pyttsx3
import os
import time
from datetime import datetime as date
import random
import sys
import threading
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt
import json


class ChatBot():
    def __init__(self,name):
        self.name = name
        # self.lang="ENG"
        # self.langlist=['en-US', 0]
        self.lang="POL"
        self.langlist=['pl', 3]
        x=open("DAVE v2\\strings\\x.json",encoding='cp1250')
        self.strings=json.load(x)
        print(self.strings[self.lang]['functions']['dave']['start'] + name ,"----")

        self.text = ""
        self.note = ""


    def speech_to_text(self):
          recognizer = sr.Recognizer()
          with sr.Microphone() as mic:
               print(self.strings[self.lang]['functions']['dave']['listen'])
               recognizer.adjust_for_ambient_noise(mic, duration=0.8)
               audio = recognizer.listen(mic)
          try:
               self.text = recognizer.recognize_google(audio, language=self.langlist[0])
               print(self.strings[self.lang]['functions']['dave']['user'], self.text)
            #    print(' '.join(self.text.lower().split(" ")[:-1]))
          except:
               print("\n")
               self.text = "none"

    def note_to_text(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as mic:
            print(self.strings[self.lang]['functions']['notes']['wait'])
            recognizer.adjust_for_ambient_noise(mic, duration=0.8)
            audio = recognizer.listen(mic)
        try:
            self.note = recognizer.recognize_google(audio, language=self.langlist[0])

        except: 
            res = self.strings[self.lang]['functions']['notes']['not_understood']
            self.text_to_speech(res, self.langlist[1])
            self.note_to_text()

        res = self.strings[self.lang]['functions']['notes']['write'].replace("$noteContent",self.note)
        self.text_to_speech(res, self.langlist[1])

        if(self.just_mic_input() in self.strings[self.lang]['wakewords']['affirmation']):
                res = self.strings[self.lang]['functions']['notes']['name']
                self.text_to_speech(res, self.langlist[1])
                NoteName = self.just_mic_input()

                res = self.strings[self.lang]['functions']['notes']['name_affirmation'].replace("$NoteName",NoteName)
                self.text_to_speech(res, self.langlist[1])
                if(self.just_mic_input() in self.strings[self.lang]['wakewords']['affirmation']):
                    with open(f'DAVE v2\\notes\\{NoteName}.txt',encoding='utf-8', mode='w') as f:
                        f.write(self.note)
                    res = self.strings[self.lang]['functions']['notes']['created'].replace("$NoteName",NoteName).replace("$noteContent",self.note)
                    self.text_to_speech(res, self.langlist[1])
                else:
                    res = self.strings[self.lang]['functions']['notes']['negation']
                    self.text_to_speech(res, self.langlist[1])
                    self.note_to_text()
                    res = self.strings[self.lang]['functions']['notes']['content']
                    self.text_to_speech(res, self.langlist[1])
        elif(self.just_mic_input() in self.strings[self.lang]['wakewords']['negation']):
            res = self.strings[self.lang]['functions']['notes']['negation']
            self.text_to_speech(res, self.langlist[1])
            self.note_to_text()


    def just_mic_input(self):

        recognizer = sr.Recognizer()
        resp = ""
        with sr.Microphone() as mic:
            print(self.strings[self.lang]['functions']['dave']['wait'])
            recognizer.adjust_for_ambient_noise(mic, duration=0.8)
            audio = recognizer.listen(mic)
            resp = recognizer.recognize_google(audio, language=self.langlist[0])
            print(self.strings[self.lang]['functions']['dave']['user'], resp)

        return resp

    def wake_up(self, text):
            if(text.lower() in ai.strings[self.lang]['wakewords']['normal']):
                return "normal"
            if(text.lower() in ai.strings[self.lang]['wakewords']['notes']):
                return "notes"
            
                
    def text_to_speech(self,text,langid):
        print(self.name + "----> ", text)
        speaker = pyttsx3.init()
        voices = speaker.getProperty('voices')
        speaker.setProperty('voice', voices[langid].id)
        speaker.setProperty('rate', 150)
        speaker.say(text)
        speaker.runAndWait()

    def run_app(self, app):
        os.startfile(f'{app}')

        
    def switch_lang(self, lang):
        self.lang = lang
        if self.lang == "ENG": 
            self.langlist=['en-US', 0]
        if self.lang == "POL":
            self.langlist=['pl', 3]
        if self.lang == "ESP":
            self.langlist=['es-US',2]



if __name__ == "__main__":
    ai = ChatBot(name="Dave")
    while True:
        # ai.lang="POL"
        # ai.langlist=['pl-PL', 3]
        ai.speech_to_text()
        
        if(ai.text.lower() in ai.strings[ai.lang]['wakewords']['normal']):
            res = random.choice(ai.strings[ai.lang]['answers']['normal'])
            ai.text_to_speech(res, ai.langlist[1])
            ai.speech_to_text()
            if(ai.text.lower() in ai.strings[ai.lang]['wakewords']['system']):
                res = ai.strings[ai.lang]['answers']['system']
                ai.text_to_speech(res, ai.langlist[1])
            if(ai.text in ai.strings[ai.lang]['wakewords']['day']):
                res = ai.strings[ai.lang]['functions']['day'].replace("$date", date.today().strftime("%A")).replace("$mday", str(time.localtime().tm_mday)).replace("$mon", date.today().strftime("%B")).replace("$year", str(time.localtime().tm_year))  
                ai.text_to_speech(res, ai.langlist[1])
            if(ai.text.lower() in ai.strings[ai.lang]['wakewords']['time']):
                res = ai.strings[ai.lang]['functions']['time'].replace("$hour", str(time.localtime().tm_hour)).replace("$minute", str(time.localtime().tm_min))
                ai.text_to_speech(res, ai.langlist[1])
            if(ai.text.lower() in ai.strings[ai.lang]['wakewords']['notes']):
                res = ai.strings[ai.lang]['answers']['notes']
                ai.text_to_speech(res, ai.langlist[1])
                ai.note_to_text()

        if(ai.wake_up(ai.text.lower()) == "notes"):
            res = ai.strings[ai.lang]['answers']['notes']
            ai.text_to_speech(res, ai.langlist[1])
            ai.note_to_text()

        if(ai.text.lower() in ai.strings[ai.lang]['wakewords']['kys']):
            # res = random.choice(ai.answers_kys)
            res = random.choice(ai.strings[ai.lang]['answers']['kys'])
            ai.text_to_speech(res, ai.langlist[1])
            exit()

        if(ai.text.lower().split(" ")[0] in ai.strings[ai.lang]['wakewords']['runapps']):
            res = ai.strings[ai.lang]['functions']['runapps']['success'] + ai.text.lower().split(" ")[1]
            ai.text_to_speech(res, ai.langlist[1])
            os.startfile(ai.text.lower().split(" ")[1])
            

        if(' '.join(ai.text.lower().split(" ")[:-1]) in ai.strings[ai.lang]['functions']['langswitch']['commands'] or ai.text.lower().split(" ")[0] in ai.strings[ai.lang]['functions']['langswitch']['commands'][-1]):
            if(ai.text.lower().split(" ")[-1] in ai.strings[ai.lang]['functions']['langswitch']['langeng']):
                ai.switch_lang("ENG")
                res = ai.strings[ai.lang]['functions']['langswitch']['success'] + ai.strings[ai.lang]['functions']['langswitch']['langeng']
                ai.text_to_speech(res, ai.langlist[1])
            if(ai.text.lower().split(" ")[-1] in ai.strings[ai.lang]['functions']['langswitch']['langpol']):
                ai.switch_lang("POL")
                res = ai.strings[ai.lang]['functions']['langswitch']['success'] + ai.strings[ai.lang]['functions']['langswitch']['langpol']
                ai.text_to_speech(res, ai.langlist[1])
            if(ai.text.lower().split(" ")[-1] in ai.strings[ai.lang]['functions']['langswitch']['langesp']):
                ai.switch_lang("ESP")
                res = ai.strings[ai.lang]['functions']['langswitch']['success'] + ai.strings[ai.lang]['functions']['langswitch']['langesp']
                ai.text_to_speech(res, ai.langlist[1])
