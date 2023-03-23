from . import getchat, utils

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
    if not await utils.config.check_addr(utils.config.chatglm_addr):
        logger.error("API地址未填写或格式错误！")
        raise ValueError("请检查API地址填写是否正确！")