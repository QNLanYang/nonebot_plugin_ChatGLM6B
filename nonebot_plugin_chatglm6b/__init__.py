from . import getchat, utils

from nonebot.plugin import PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="ChatGLM-6B",
    description="调用本地 ChatGLM API 进行聊天",
    usage="@机器人 +【命令前缀（如果有）】+ GLM|. +【内容】"
)

