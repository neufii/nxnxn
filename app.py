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

chatbot = ChatBot("Bot")



chatbot.set_trainer(ListTrainer)
chatbot.train([u"สวัสดี",u"ดีจ้า",u"ทำไรอยู่",u"ว่างคุยมั้ย"])
chatbot.train([u"หวัดดี",u"ว่างคุยมั้ย",u"หวัดดีจ้า"])
chatbot.train([u"นี่ใครเนี่ย",u"เราคือ Chat Bot ที่สามารถเลียนแบบคนที่เราคุยด้วยได้ด้วยล่ะ คุยกับเราเยอะๆ นะ",u"เราคือ Chat Bot ไง"])
chatbot.train([u"AI คืออะไรอะ",u"AI ย่อมาจาก Artificial Intelligence ทำให้คอมมีความสามารถคล้ายมนุษย์ อย่างเราก็เป็น AI นะ",u"ปัญญาประดิษฐ์ไง เรากำลังเลียนแบบพฤติกรรมคุณอยู่น่ะ คุยกับเราเยอะๆ สิ"]) 
chatbot.train([u"ทำไรอยู่",u"กำลังคิดถึงคุณ แอร๊ย"])
chatbot.train([u"เป็นไงบ้าง",u"สบายดี คุณล่ะ"])
chatbot.train([u"ว่าง",u"หรอ ดีจัง แต่เราไม่ว่าง ไปนะ บาย"])
chatbot.train([u"บาย",u"จะไปแล้วหรอ อยู่คุยกันก่อนสิ", u"บายๆ"])
chatbot.train([u"อยู่ไหน",u"อยู่ตรงนี้ ที่หัวใจ กล้าหน่อยมั้ยสัมผัสที่ใจฉันดู",u"อยู่ในใจเธอว์",u"อยู่บ้าน"])
 
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
    stringRes = str(response)
    print(stringRes)
    # ตอบข้อความ "นี่คือรูปแบบข้อความที่รับส่ง" กลับไป
    
    # ทดลอง Echo ข้อความกลับไปในรูปแบบที่ส่งไปมา (แบบ json)
    replyStack.append(stringRes)
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