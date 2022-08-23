# line 伺服器傳訊息過來時, line-bot要回傳, 故要載入line官方釋出的SDK來做開發
# SDK: Software development kit
# line-bot-sdk-python: https://github.com/line/line-bot-sdk-python

# flask, django(有畫面/網頁的): 兩個python架設伺服器主流的套件

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

# access 存取權杖
# 啟動line webhook
line_bot_api = LineBotApi('ibFd6ZFPtJY8UXj9yNUJJNe6sixEN1XGyATQKQG9NLT1WWKE20BMGy6k6mRsC33MtucI4FoZUpCbp4mLIA5ihw5bbAqOUXRufDfiqp9q5Vm0S9QNIsEkAYSWlXNrnDuA+olPM4r4hbEjoOsNyb+vHgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('c54c9635645437e4401118ee8cb31b72')

# 接收line傳來的訊息的程式碼
@app.route("/callback", methods=['POST'])  #若有人從網址進入後使用callback, 就會接收到對方的資訊
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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

#接收程式碼後讀取我們要回復的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

if __name__ == "__main__": # 確保程式碼不會剛被載入(import)就被執行
    app.run()