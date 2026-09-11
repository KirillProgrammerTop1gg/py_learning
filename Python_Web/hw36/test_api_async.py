import asyncio
import aiohttp
import time

TOTAL_REQUESTS_QUANTITY = 1000
SEM_LIMIT = 100
url = "http://127.0.0.1:8000/participants"

sem = asyncio.Semaphore(SEM_LIMIT)


async def send_request(session, i):
    async with sem:
        async with session.post(
            url,
            json={
                "name": "nick",
                "email": f"example{i+1}@test.com",
                "age": 17,
                "event": "yoga",
            },
        ) as res:
            await res.text()


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, i) for i in range(TOTAL_REQUESTS_QUANTITY)]
        await asyncio.gather(*tasks)

    print(f"Work time: {round(time.time() - start_time, 2)}s")


asyncio.run(main())
