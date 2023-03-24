from nonebot import get_driver
from nonebot.log import logger
from pydantic import BaseSettings

class Config(BaseSettings):

    chatglm_addr: str = ""  #GLMAPI地址
    chatglm_poke: bool = False  #是否启用戳一戳提示
    chatglm_2pic: bool = False  #是否启用转图片
    chatglm_wide: int = 400 #转图片时用的图片宽度（单位：像素）
    chatglm_rply: bool = False  #是否启用回复模式，关闭则为艾特
    chatglm_mmry: int = 10  #支持记录的对话回合数
    chatglm_pblc: bool = False  #群聊中是否启用公共对话，即开启后所有群员共用同一段记录

    chatglm_model_leng: int = 2048  #设置模型的max-length，注意历史对话记录也占用token数
    chatglm_model_temp: float = 0.95    #设置模型的temperature，取值0-1，越高回复越多样
    chatglm_model_topp: float = 0.7 #设置模型的top-P，取值0-1，越高话题越相关

    class Config:
        extra = "ignore"

    async def check_addr(self,url):    #检查API地址格式
        if url and url.startswith("http"):
            return True
        return False

config = Config(**get_driver().config.dict())
logger.debug(f"加载config完成" + str(config))