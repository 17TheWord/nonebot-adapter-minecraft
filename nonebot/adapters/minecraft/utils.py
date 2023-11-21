from typing import Union

from nonebot.utils import logger_wrapper

from .message import Message, MessageSegment

log = logger_wrapper("Minecraft")


def get_msg(message: Union[str, Message, MessageSegment]):
    messageList = []
    if isinstance(message, str):
        messageList.append(MessageSegment.text(message).data)
    elif isinstance(message, MessageSegment):
        messageList.append(message.data)
    elif isinstance(message, Message):
        for msg in message:
            messageList.append(msg.data)
    else:
        return None
    return messageList


def get_actionbar_msg(message: Union[str, Message, MessageSegment]):
    messageList = []
    if isinstance(message, str):
        messageList.append(MessageSegment.actionbar(message).data)
    elif isinstance(message, MessageSegment) and message.type == "actionbar":
        messageList.append(message.data)
    elif isinstance(message, Message):
        return message
    else:
        return None
    return messageList
