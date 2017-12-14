from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('sRYigBQ4TKs4v1CbEaHPY6+pXvrY//AV1Ah4T04FRdqKDxWBpgy7IQwFT9YV6v0/hASPJmdXHtF0OnVBU9zf4NcPjry8/MA2/5ruLY/tYsZ8bzm/hVaXKTGZZfX39IIyU42i5Lbrnl/P91grLzC/6wdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('5d7e27ec0103a47f7eb6d15d18f41412')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()