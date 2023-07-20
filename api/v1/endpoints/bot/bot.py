from fastapi import APIRouter
from fastapi import Request, HTTPException

from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from linebot.exceptions import InvalidSignatureError

import logging
import json

from api.v1.endpoints.bot import config

logger = logging.getLogger("bot")

router = APIRouter()

line_bot_api = LineBotApi(config.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(config.LINE_CHANNEL_SECRET)

@router.get("/")
def read_root():
    return {"Hello": "World"}

@router.post("/callback")
async def callback(request: Request) -> str:
    """LINE Bot webhook callback

    Args:
        request (Request): Request Object.

    Raises:
        HTTPException: Invalid Signature Error

    Returns:
        str: OK
    """
    signature = request.headers["X-Line-Signature"]
    body = await request.body()

    print("Request body: " + body.decode())
    # logger.info("Signature: " + signature)
    
    # handle webhook body
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameter")
    return "OK"

@handler.add(MessageEvent, message=(TextMessage))
def handle_message(event) -> None:
    """Event - User sent message

    Args:
        event (LINE Event Object): Refer to https://developers.line.biz/en/reference/messaging-api/#message-event
    """
    if event.message.text == '測試push':
        # line_bot_api.push_message("C81e84ef5f16bee0fe8dafb3691c1b073", TextSendMessage(text='測試PUSH訊息~'))
        return 'ok'
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )
    return 'ok'
