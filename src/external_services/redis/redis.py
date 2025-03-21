import redis.asyncio as redis

pool = redis.ConnectionPool(host="localhost", port=6379, db=0, decode_responses=True)


async def get_redis() -> redis.Redis:
    client: redis.Redis = redis.Redis(connection_pool=pool)
    yield client
    await client.aclose()
