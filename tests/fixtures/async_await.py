async def wait_and_execute(param, *args, default=None, **kwargs):
    async with session.transaction():
        result = await session.get_result(param.lower().split('.')[-1])

    async for arg in args:
        await session.update_arg(arg, default=default, **kwargs)

def proxy_generator():
    yield from range(10)
