from typing import Union

from nonebot.utils import logger_wrapper

from .message import Message, MessageSegment

log = logger_wrapper("Minecraft")


def get_msg(message: Union[str, Message, MessageSegment]):
    message_list = []
    if isinstance(message, str):
        message_list.append(MessageSegment.text(message).data)
    elif isinstance(message, MessageSegment):
        message_list.append(message.data)
    elif isinstance(message, Message):
        for msg in message:
            message_list.append(msg.data)
    else:
        return None
    return message_list
