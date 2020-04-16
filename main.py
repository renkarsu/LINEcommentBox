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

from google.cloud import datastore

app = Flask(__name__)

line_bot_api = LineBotApi('ZcEY36SPZj3pecV5+D+cYKOYe/YOujm7u7pzR3ZCwfPdD3M/llldxlT8e1/xpqJ0lY5t4jOHaVjyduzOm8hBdYIj0lJglz8Nco2oH7yNvNywInkp7tULDGb/MCe3d7EKwQ7EweXfNREXoavdCoX/egdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('d406e96cae32c0742308db05c033cd79')

datastore_client = datastore.Client()

def store_time(ureply):
    entity = datastore.Entity(key=datastore_client.key('ureply'))
    entity.update({
        'ureply': ureply
    })

    datastore_client.put(entity)

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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
#    line_bot_api.reply_message(
#        event.reply_token,
#        TextSendMessage(text=event.message.text))
    text = event.message.text
    store_time(text)


if __name__ == "__main__":
    app.run()
