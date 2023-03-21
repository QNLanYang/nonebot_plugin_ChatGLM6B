from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import MessageEvent, Message, MessageSegment, Bot
from nonebot.params import CommandArg

import requests

from .config import config

if config.chatglm_2pic:
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import md_to_pic

#以上为import部分，以下为实现部分

chatglm = on_command("GLM", aliases={"#"}, priority=99, block=False, rule=to_me())

@chatglm.handle()
async def chat(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    #获取剔除前缀的用户输入纯文本
    txt = msg.extract_plain_text()

    #若没有输入则结束
    if txt == "" or txt is None:
        await chatglm.finish("你想问什么呢？", at_sender=True)
    
    #若响应成功则戳一戳用户
    await chatglm.send(Message(f'[CQ:poke,qq={event.user_id}]'))

    #检查地址是否填写
    if not await config._checkaddr(config.chatglm_addr):
        await chatglm.finish("请检查API地址是否填写正确，以'http(s)://'开头", at_sender=True)

    history = []

    #调用API
    try:
        res = requests.post(f"{config.chatglm_addr}/predict?user_msg={txt}", json=history)

    #排查错误
    except Exception as error:
        logger.error(error)
        await chatglm.finish(str(error), at_sender=True)
    
    if res.status_code != 200:
        await chatglm.finish(f"与API服务器沟通时出现问题，错误{res.status_code}", at_sender=True)
    
    #得到正确回复
    resp, history = res.json()["response"], res.json()["history"]

    #转图片
    if config.chatglm_2pic:
        if resp.count("```") % 2 != 0:
            resp += "\n```"
        img = await md_to_pic(resp, width=400)
        resp = MessageSegment.image(img)

    #返回生成的文本
    ans = MessageSegment.reply(event.message_id) + resp
    await chatglm.finish(ans)