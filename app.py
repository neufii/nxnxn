#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

from flask import Flask, request
import json
import requests

# ตรง YOURSECRETKEY ต้องนำมาใส่เองครับจะกล่าวถึงในขั้นตอนต่อๆ ไป
global LINE_API_KEY
LINE_API_KEY = 'Bearer sRYigBQ4TKs4v1CbEaHPY6+pXvrY//AV1Ah4T04FRdqKDxWBpgy7IQwFT9YV6v0/hASPJmdXHtF0OnVBU9zf4NcPjry8/MA2/5ruLY/tYsZ8bzm/hVaXKTGZZfX39IIyU42i5Lbrnl/P91grLzC/6wdB04t89/1O/w1cDnyilFU='

app = Flask(__name__)

chatbot = ChatBot("NBot")

conversation = [u"สวัสดี",u"ดีจ้า",u"ทำไรอยู่",u"กินข้าว"]

chatbot.set_trainer(ListTrainer)
chatbot.train(conversation)
 
@app.route('/')
def index():
    return 'This is NxNxN Server.'
@app.route('/bot', methods=['POST'])

def bot():
    # ข้อความที่ต้องการส่งกลับ
    replyStack = list()
   
    # ข้อความที่ได้รับมา
    msg_in_json = request.get_json()
    msg_in_string = json.dumps(msg_in_json)

    #write log
    print(msg_in_string)
    
    # Token สำหรับตอบกลับ (จำเป็นต้องใช้ในการตอบกลับ)
    replyToken = msg_in_json["events"][0]['replyToken']
    
    # ส่วนนี้ดึงข้อมูลพื้นฐานออกมาจาก json (เผื่อ)
    userID =  msg_in_json["events"][0]['source']['userId']
    msgType =  msg_in_json["events"][0]['message']['type']

    print("userId\t"+userID)
    print("msgType\t"+msgType)
    
    # ตรวจสอบว่า ที่ส่งเข้ามาเป็น text รึป่าว (อาจเป็น รูป, location อะไรแบบนี้ได้ครับ)
    #if msgType != 'text':
    #    reply(replyToken, ['Only text is allowed.'])
    #    return 'OK',200
    
    # ตรงนี้ต้องแน่ใจว่า msgType เป็นประเภท text ถึงเรียกได้ครับ
    #text = msg_in_json["events"][0]['message']['text'].lower().strip()
    
    if msgType != 'text':
            reply(replyToken, ['Only text is allowed.'])
            return 'OK',200
    
    text = msg_in_json["events"][0]['message']['text'].lower().strip()

    print("TEXT\t"+text)

    response = chatbot.get_response(text)
    # ตอบข้อความ "นี่คือรูปแบบข้อความที่รับส่ง" กลับไป
    
    # ทดลอง Echo ข้อความกลับไปในรูปแบบที่ส่งไปมา (แบบ json)
    replyStack.append(response)
    print("replyToken\t" + replyToken)
    reply(replyToken, replyStack[:5])

    
    return 'OK', 200
 
def reply(replyToken, textList):
    # Method สำหรับตอบกลับข้อความประเภท text กลับครับ เขียนแบบนี้เลยก็ได้ครับ
    print("REPLY BEGIN")
    LINE_API = 'https://api.line.me/v2/bot/message/reply'
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization': LINE_API_KEY
    }
    msgs = []
    for text in textList:
        msgs.append({
            "type":"text",
            "text":text
        })
    data = json.dumps({
        "replyToken":replyToken,
        "messages":msgs
    })
    requests.post(LINE_API, headers=headers, data=data)
    print("REPLY END")
    return

if __name__ == '__main__':
    app.run()