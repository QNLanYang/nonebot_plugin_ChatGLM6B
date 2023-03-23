from nonebot.log import logger
import json, os
from pathlib import Path
import aiofiles

from .config import config

class Record:
    
    def __get_path(self,uid): #生成保存路径
        jsonpath = Path(f"data/chatglm/history_{uid}.json").resolve()
        return jsonpath

    async def __init_json(self,uid):    #初始化历史记录
        jsonpath = self.__get_path(uid)
        if not jsonpath.exists():   #不存在则创建
            jsonpath.parent.mkdir(parents=True, exist_ok=True)
            async with aiofiles.open(jsonpath, "w", encoding="utf-8") as f:
                await f.write("{}")
        else:   #删除空记录
            async with aiofiles.open(jsonpath, "r", encoding="utf-8") as f:
                data = await f.read()
            if data is None:
                os.remove(jsonpath)
                await self.__init_json(uid)

    async def load_history(self,uid):    #读取历史记录
        jsonpath = self.__get_path(uid)
        await self.__init_json(uid)
        async with aiofiles.open(jsonpath, "r", encoding="utf-8") as f:
            jsonraw = await f.read()
            data = json.loads(jsonraw)
            log = list(data)
            logger.debug("Dialogue history loaded Successfully!")
            return log
    
    async def save_history(self,log,uid):    #保存对话记录 
        jsonpath = self.__get_path(uid)
        log = await self.check_length(log)
        async with aiofiles.open(jsonpath, "w", encoding="utf-8") as f:
            jsonnew = json.dumps(log)
            await f.write(jsonnew)
            logger.debug("Dialogue history saved Successfully.")
    
    async def check_length(self,log):    #将最久远的对话记录删除掉
        if (x := len(log) - config.chatglm_mmry) > 0:
            log = log[x:]
            logger.debug("History longer than config, delleting earliest.")
        return list(log)
       
    async def clr_history(self,uid): #清除历史对话
        jsonpath = self.__get_path(uid)
        os.remove(jsonpath)
        logger.debug("History delleted Successfully!")
        return True

record = Record()