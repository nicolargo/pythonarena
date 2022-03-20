import asyncio

async def req(nb):
    return {nb: nb for ng in range(nb)}


async def main():
    results = await asyncio.gather(*[req(i) for i in range(0, 4)])

    print(results)


if __name__ == "__main__":
    asyncio.run(main())

