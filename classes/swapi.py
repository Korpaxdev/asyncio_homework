import asyncio

from classes.models import Characters
from utils.checks import check_is_link
from utils.request import send_request


class Swapi:
    HOST = "https://swapi.dev/api"
    PEOPLE_URL = f"{HOST}/people"
    REQUIRED_FIELDS = Characters.get_column_names()
    RES_REQUIRED_KEYS = ["title", "name"]

    async def get_character_by_id(self, char_id):
        res = await send_request(self.PEOPLE_URL + f"/{char_id}")
        if not res:
            return None
        char = self.__clear_character(res)
        tasks = [self.__parse_field(key, value) for key, value in char.items()]
        for task in asyncio.as_completed(tasks):
            char.update(await task)
        return char

    async def get_total_count_characters(self):
        req = await send_request(self.PEOPLE_URL)
        return req.get("count", 0) + 1

    async def __parse_field(self, key, value):
        if isinstance(value, list):
            new_items = [await self.__parse_field(key, v) for v in value]
            return {key: self.__create_string_field(new_items)}
        elif check_is_link(value):
            res = await send_request(value)
            if not res:
                return None
            for k in res:
                if k in self.RES_REQUIRED_KEYS:
                    return {key: res[k]}
        return {key: value}

    def __clear_character(self, character):
        return {key: character[key] for key in character if key in self.REQUIRED_FIELDS}

    def __create_string_field(self, item: list | str):
        if isinstance(item, dict):
            return ", ".join(item.values())
        if isinstance(item, list):
            if len(item):
                return ", ".join([self.__create_string_field(value) for value in item])
            return None
        return str
