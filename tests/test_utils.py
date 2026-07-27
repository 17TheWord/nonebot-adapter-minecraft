import json
from uuid import UUID

from nonebot.adapters.minecraft.exception import ActionFailed
from nonebot.adapters.minecraft.utils import DataclassEncoder, handle_api_result
import pytest


def test_handle_api_result_returns_data():
    assert handle_api_result({"status": "OK", "data": {"message": "pong"}}) == {"message": "pong"}


def test_handle_api_result_returns_none_for_none_result():
    assert handle_api_result(None) is None


def test_handle_api_result_raises_action_failed():
    with pytest.raises(ActionFailed) as exc_info:
        handle_api_result({"status": "FAILED", "message": "bad request", "reason": "invalid"})

    assert exc_info.value.message == "bad request"
    assert exc_info.value.info["reason"] == "invalid"


def test_dataclass_encoder_serializes_uuid():
    uuid = UUID("12345678-1234-5678-1234-567812345678")

    assert json.loads(json.dumps({"uuid": uuid}, cls=DataclassEncoder)) == {"uuid": str(uuid)}
