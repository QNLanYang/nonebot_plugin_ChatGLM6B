from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseSettings
import json, os
from pathlib import Path
import aiofiles

jsonpath = Path("data/chatglm/history.json").resolve()


class Config(BaseSettings):

    chatglm_addr: str = ""  #GLMAPI地址
    chatglm_poke: bool = True   #是否启用戳一戳提示
    chatglm_2pic: bool = False  #是否启用转图片
    chatglm_wide: int = 400 #转图片时用的图片宽度
    chatglm_rply: bool = False  #是否启用回复模式，关闭则为艾特
    chatglm_mmry: int = 10  #支持记录的对话回合数

    class Config:
        extra = "ignore"

    async def check_addr(self, url):    #检查API地址格式
        if url and url.startswith("http"):
            return True
        else:
            return False
    
    async def __init_json(self):    #初始化历史记录
        if not jsonpath.exists():
            jsonpath.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(jsonpath, "w") as f:
                await f.write("{}")
        else:
            async with aiofiles.open(jsonpath, "r") as f:
                data = await f.read()
            if data is None:
                os.remove(jsonpath)

    async def load_history(self):    #读取历史记录
        await self.__init_json()
        async with aiofiles.open(jsonpath, "r") as f:
            jsonraw = await f.read()
            data = json.loads(jsonraw)
            log = list(data)
            return log
    
    async def save_history(self,log):    #保存对话记录 
        log = await self.check_length(log)
        async with aiofiles.open(jsonpath, "w") as f:
            jsonnew = json.dumps(log)
            await f.write(jsonnew)
    
    async def check_length(self,log):    #将最久远的对话记录删除掉
        if (x := len(log) - config.chatglm_mmry) > 0:
            log = log[x:]
        return list(log)
       
    async def clr_history(self): #清除历史对话
        os.remove(jsonpath)
        return True

config = Config(**get_driver().config.dict())
logger.debug(f"加载config完成" + str(config))