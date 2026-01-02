from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage,
    TextSendMessage, ImageSendMessage
)
import os

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    try:
        signature = request.headers["X-Line-Signature"]
        body = request.get_data(as_text=True)
        handler.handle(body, signature)
    except Exception as e:
        print(e)
    return "OK"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip().lower()
    if not text:
        return

    commands = (
        "รายงานkiosk", "ยอด", "รายงาน",
        "บัตรครึ่งใบ", "บัตร",
        "wifi", "ci",
        "เบอร์",
        "ภาษี", "vat",
        "help", "บอท"
    )

    if text not in commands:
        return

    messages = []

    if text in ("help", "บอท"):
        messages.append(TextSendMessage(
            text="พิมพ์: รายงาน / wifi / เบอร์ / ภาษี"
        ))

    elif text in ("รายงานkiosk", "ยอด", "รายงาน"):
        messages.append(TextSendMessage(
            text="📊 รายงานตู้ KIOSK\nhttps://smartcargo.airportthai.co.th/aotwebmanagement/reports/KisokreportComponent"
        ))

    elif text in ("wifi", "ci"):
        messages.append(TextSendMessage(
            text="📶 Wifi CI\nPi@FDMS464690"
        ))

    elif text == "เบอร์":
        messages.append(TextSendMessage(
            text="📞 ฮอน 091-568-8414"
        ))

    elif text in ("ภาษี", "vat"):
        image_url = "https://github.com/vankokeiei/line-group-bot/blob/main/LINE_NOTE_260101_1.jpg?raw=true"
        messages.append(TextSendMessage(text="📄 เอกสารภาษี"))
        messages.append(ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        ))

    line_bot_api.reply_message(event.reply_token, messages)

if __name__ == "__main__":
    app.run(port=5000)
