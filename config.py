from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseSettings

class Config(BaseSettings):

    chatglm_addr: str = ""  #GLMAPI地址
    chatglm_poke: bool = True   #是否启用戳一戳提示
    chatglm_2pic: bool = False  #是否启用转图片

    class Config:
        extra = "ignore"

    async def _checkaddr(self, url):
        if url and url.startswith("http"):
            return True
        else:
            return False

config = Config(**get_driver().config.dict())
logger.debug(f"加载config完成" + str(config))