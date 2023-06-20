import asyncio

from more_itertools import chunked

from classes.alchemy import Alchemy
from classes.swapi import Swapi

MAX_CHUNK_SIZE = 10


async def main():
    await Alchemy.create_engine().create_tables()
    swapi = Swapi()
    characters_count = await swapi.get_total_count_characters()
    chunked_tasks = chunked(
        [swapi.get_character_by_id(i) for i in range(1, characters_count + 1)],
        MAX_CHUNK_SIZE,
    )
    for chunk in chunked_tasks:
        for task in asyncio.as_completed(chunk):
            await Alchemy.insert_character_into_db(await task)
    await Alchemy.engine_off()


if __name__ == "__main__":
    asyncio.run(main())
