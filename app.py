from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import (
    MessageEvent, TextMessage,
    TextSendMessage, ImageSendMessage
)
import os
import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi(os.getenv("LINE_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    body = request.get_data(as_text=True)
    handler.handle(body, signature)
    return "OK"

# ================== GOOGLE SHEET ==================
SHEET_ID = "15LvvL5A1X8F4HLqrUEG8dJ9lnzKuYEt2u7hlg8LH2WE"
SHEET_NAME = "Sheet1"

def read_google_sheet():
    url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:json&sheet={SHEET_NAME}"
    res = requests.get(url)
    data = res.text

    json_data = data[data.find("{"):data.rfind("}")+1]
    obj = json.loads(json_data)

    rows = obj["table"]["rows"]
    result = []

    for r in rows:
        row = [c["v"] if c else "" for c in r["c"]]
        result.append(row)

    return result
# ==================================================

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip().lower()
    if not text:
        return

    commands = (
         "รายงานkiosk", "ยอด", "รายงาน",
        "wifi", "ci",
        "เบอร์",
        "ภาษี", "vat",
        "ตารางงาน", "ตาราง",
        "help", "บอท"
    )

    if text not in commands:
        return

    messages = []

    # ===== ตารางงาน =====
    if text in ("ตารางงาน", "ตาราง"):
        sheet_data = read_google_sheet()

        reply_text = "📋 ตารางงาน\n\n"
        for row in sheet_data[1:]:
            reply_text += f"{row[0]} : {row[1]}\n"

        messages.append(TextSendMessage(text=reply_text))

    # ===== help =====
    elif text in ("help", "บอท"):
        messages.append(TextSendMessage(
            text="พิมพ์: ตารางงาน / รายงาน / wifi / เบอร์ / ภาษี"
        ))

    # ===== รายงาน =====
    elif text in ("รายงานkiosk", "ยอด", "รายงาน"):
        messages.append(TextSendMessage(
            text=(
                "📊 รายงานตู้ KIOSK\n"
                "https://smartcargo.airportthai.co.th/aotwebmanagement/reports/KisokreportComponent"
            )
        ))

    # ===== wifi =====
    elif text in ("wifi", "ci"):
        messages.append(TextSendMessage(
            text="📶 Wifi CI\nPi@FDMS464690"
        ))

    # ===== เบอร์ =====
    elif text == "เบอร์":
        messages.append(TextSendMessage(
            text="📞 ฮอน 091-568-8414"
        ))

    # ===== ภาษี =====
    elif text in ("ภาษี", "vat"):
        image_url = "https://github.com/vankokeiei/line-group-bot/blob/main/LINE_NOTE_260101_1.jpg?raw=true"
        messages.append(TextSendMessage(text="📄 เอกสารภาษี"))
        messages.append(ImageSendMessage(
            original_content_url=image_url,
            preview_image_url=image_url
        ))

    line_bot_api.reply_message(event.reply_token, messages)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
