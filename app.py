from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)

from linebot.exceptions import (InvalidSignatureError)

from linebot.models import (MessageEvent, TextMessage, ImageMessage, VideoMessage, StickerMessage, TextSendMessage)

import os
import json

from logging import getLogger, config

app = Flask(__name__)

ABS_PATH = os.path.dirname(os.path.abspath(__file__))
with open(ABS_PATH+'/config.json', 'r') as f:
    CONF_DATA = json.load(f)
    
CHANNEL_ACCESS_TOKEN = CONF_DATA['CHANNEL_ACCESS_TOKEN']
CHANNEL_SECRET = CONF_DATA['CHANNEL_SECRET']

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

config.fileConfig('logging.conf')
logger = getLogger(__name__)

@app.route("/test", methods=['GET', 'POST'])
def test():
    return 'I\'m alive!'

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    logger.info("Request body: " + body)
    
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid Signature. Please check your channel access token / channel secret")
        abort(400)
    return 'OK'






if __name__ == "__main__":
    # use 9999 for port
    port = int(os.getv("PORT", 9999))
    
    # run Flask and set Flask app port
    app.run(host="0.0.0.0", port=port)
        