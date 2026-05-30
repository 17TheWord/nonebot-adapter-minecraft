import asyncio

from nonebot.adapters.minecraft.store import ResultStore
import pytest


@pytest.mark.asyncio
async def test_result_store_fetch_result():
    store = ResultStore()
    seq = store.get_seq()

    fetch_task = asyncio.create_task(store.fetch(seq, 1))
    await asyncio.sleep(0)

    result = {"echo": str(seq), "status": "OK", "data": {"message": "pong"}}
    store.add_result(result)

    assert await fetch_task == result
    assert seq not in store._futures


@pytest.mark.asyncio
async def test_result_store_fetch_timeout_cleans_future():
    store = ResultStore()
    seq = store.get_seq()

    with pytest.raises(asyncio.TimeoutError):
        await store.fetch(seq, 0.01)

    assert seq not in store._futures


@pytest.mark.asyncio
async def test_result_store_ignores_unknown_echo():
    store = ResultStore()
    seq = store.get_seq()

    fetch_task = asyncio.create_task(store.fetch(seq, 1))
    await asyncio.sleep(0)

    store.add_result({"echo": "unknown", "status": "OK"})
    store.add_result({"echo": str(seq + 1), "status": "OK"})

    assert not fetch_task.done()

    fetch_task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await fetch_task
    assert seq not in store._futures
