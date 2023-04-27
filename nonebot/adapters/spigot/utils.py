from typing import Union

from .message import Message, MessageSegment


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
    return {"message": messageList}
