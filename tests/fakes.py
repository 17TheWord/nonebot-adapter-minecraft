from nonebot.exception import WebSocketClosed


class FakeRequest:
    def __init__(self, headers: dict[str, str]):
        self.headers = headers


class FakeWebSocket:
    def __init__(self, headers: dict[str, str] | None = None, messages: list[str] | None = None):
        self.request = FakeRequest(headers or {})
        self.messages = messages or []
        self.accepted = False
        self.close_code = None
        self.close_reason = None

    async def accept(self):
        self.accepted = True

    async def receive(self):
        if self.messages:
            return self.messages.pop(0)
        raise WebSocketClosed(1000, "closed")

    async def send(self, data):
        self.messages.append(data)

    async def close(self, code: int = 1000, reason: str | None = None):
        self.close_code = code
        self.close_reason = reason


class FakeWebSocketContext:
    def __init__(self, websocket: FakeWebSocket):
        self.websocket = websocket

    async def __aenter__(self):
        return self.websocket

    async def __aexit__(self, exc_type, exc, tb):
        return False
