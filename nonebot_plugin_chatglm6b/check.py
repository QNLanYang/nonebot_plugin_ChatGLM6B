from nonebot.log import logger

import aiohttp

from .config import config

class Check:
    async def chk_server(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{config.chatglm_addr}/") as test:
                if (await test.json())["message"]!="Hello ChatGLM API!":
                    return False
                return True


check = Check()