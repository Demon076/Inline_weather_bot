import asyncio
import json
import logging


import aiofiles

from app.services.profiling.time import async_timeit
from app.services.weather.api.get_weather import get_weather


def start_logging():
    open('log.log', 'w').close()
    logging.basicConfig(handlers=[logging.FileHandler('log.log')],
                        level=logging.INFO
                        )


@async_timeit
async def main():
    dic = {str(i): f'{value + 1}' for i, value in enumerate(range(30))}
    asyncio.create_task(get_weather(city="Moscow"))
    asyncio.create_task(get_weather(city="Moscow"))
    asyncio.create_task(get_weather(city="Moscow"))
    async with aiofiles.open('log.json', 'w') as file:
        await file.write(json.dumps([]))

    async with aiofiles.open("log.json", 'r') as file:
        jn = await file.read()
        jn = json.loads(jn)
    for i in range(999):
        jn.append(dic)
    async with aiofiles.open('log.json', 'w') as file:
        await file.write(json.dumps(jn, indent=4))

    async with aiofiles.open("log.json", 'r') as file:
        jn = await file.read()
        jn = json.loads(jn)
    jn.append(dic)
    async with aiofiles.open('log.json', 'w') as file:
        await file.write(json.dumps(jn, indent=4))

# main took 0.311652 seconds to complete
# main took 0.123885 seconds to complete
if __name__ == "__main__":
    asyncio.run(main())
