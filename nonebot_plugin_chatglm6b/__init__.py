from . import chat, request, save, config

from nonebot import get_driver
from nonebot.log import logger
from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ChatGLM-6B",
    description="调用本地 ChatGLM API 进行聊天",
    usage="@机器人 +【命令前缀（如果有）】+ GLM|. +【内容】"
)

driver = get_driver()

@driver.on_startup
async def startup():
    if not await config.config.check_addr(config.config.chatglm_addr):
        if not await request.request.chk_server():
            logger.error("API地址未填写或格式错误！")
            raise ValueError("请检查API地址填写是否正确！")
    logger.debug("API Address comfirmed")