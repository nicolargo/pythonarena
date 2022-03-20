import asyncio

async def req(nb):
    return {nb: nb for ng in range(nb)}


async def main():
    tasks = []

    for i in range(0, 4):
        tasks.append(asyncio.create_task(req(i)))

    results = await asyncio.gather(*tasks)

    print(results)


if __name__ == "__main__":
    asyncio.run(main())

