from fastid.trace import decorator_trace


@decorator_trace(name='test_decorator_trace_async')
async def func_decorator_trace_async() -> bool:
    return True


async def test_decorator_trace_async():
    assert await func_decorator_trace_async()
