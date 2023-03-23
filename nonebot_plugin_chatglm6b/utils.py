from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseSettings
import json, os
from pathlib import Path
import aiofiles

class Config(BaseSettings):

    chatglm_addr: str = ""  #GLMAPI地址
    chatglm_poke: bool = True   #是否启用戳一戳提示
    chatglm_2pic: bool = False  #是否启用转图片
    chatglm_wide: int = 400 > 100 #转图片时用的图片宽度（单位：像素）
    chatglm_rply: bool = False  #是否启用回复模式，关闭则为艾特
    chatglm_mmry: int = 10  #支持记录的对话回合数
    chatglm_pblc: bool = False  #群聊中是否启用公共对话，即开启后所有群员共用同一段记录

    class Config:
        extra = "ignore"

    async def check_addr(self,url):    #检查API地址格式
        if url and url.startswith("http"):
            return True
        else:
            return False

config = Config(**get_driver().config.dict())
logger.debug(f"加载config完成" + str(config))

class Record:
    
    def __get_path(self,uid): #生成保存路径
        jsonpath = Path(f"data/chatglm/history_{uid}.json").resolve()
        return jsonpath

    async def __init_json(self,uid):    #初始化历史记录
        jsonpath = self.__get_path(uid)
        if not jsonpath.exists():
            jsonpath.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(jsonpath, "w") as f:
                await f.write("{}")
        else:
            async with aiofiles.open(jsonpath, "r") as f:
                data = await f.read()
            if data is None:
                os.remove(jsonpath)
                await self.__init_json(uid)

    async def load_history(self,uid):    #读取历史记录
        jsonpath = self.__get_path(uid)
        await self.__init_json(uid)
        async with aiofiles.open(jsonpath, "r") as f:
            jsonraw = await f.read()
            data = json.loads(jsonraw)
            log = list(data)
            return log
    
    async def save_history(self,log,uid):    #保存对话记录 
        jsonpath = self.__get_path(uid)
        log = await self.check_length(log)
        async with aiofiles.open(jsonpath, "w") as f:
            jsonnew = json.dumps(log)
            await f.write(jsonnew)
    
    async def check_length(self,log):    #将最久远的对话记录删除掉
        if (x := len(log) - config.chatglm_mmry) > 0:
            log = log[x:]
        return list(log)
       
    async def clr_history(self,uid): #清除历史对话
        jsonpath = self.__get_path(uid)
        os.remove(jsonpath)
        return True

record = Record