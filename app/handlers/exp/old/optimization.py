import asyncio

from app.services.profiling.time import async_timeit


# TODO: Переписать мою библиотеку на join

@async_timeit
async def main():
    s = ""
    for i in range(1000000):
        s.join(f'{i}')


# main took 0.157543 seconds to complete
# main took 0.254896 seconds to complete

# main took 1.786474 seconds to complete
# main took 0.551372 seconds to complete

# join лучше, когда изменяемая строка и оптимизировать нельзя
if __name__ == "__main__":
    asyncio.run(main())
