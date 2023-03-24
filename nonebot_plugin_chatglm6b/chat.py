from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (MessageEvent,
                            Message, MessageSegment, Bot)
from nonebot.params import CommandArg, _shell_command_argv

from .save import record
from .request import request
from .config import config

if config.chatglm_2pic:
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import md_to_pic

#以上为import部分，以下为实现部分

chatglm = on_command("GLM", aliases={"#"}, priority=99,
                    block=False, rule=to_me())

clr_log = on_command("清除上下文", aliases={"clrlog"}, priority=99,
                    block=False, rule=to_me())

@chatglm.handle()
async def chat(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    #获取剔除前缀的用户输入纯文本
    txt = msg.extract_plain_text()

    #若没有输入则结束
    if txt == "" or txt is None:
        await chatglm.finish("你想问什么呢？", at_sender=True)
    
    #若响应成功则戳一戳用户
    await chatglm.send(Message(f'[CQ:poke,qq={event.user_id}]'))

    #检查服务器状态
    if not await request.chk_server():
        logger.error("连接服务器失败，请检查服务器状态。")
        await chatglm.finish("服务器好像没有开启呢，问问我的主人吧！")

    #读取历史对话记录
    if config.chatglm_mmry:
        history, jsonpath = await record.load_history(event)
    else:
        history = []

    #调用API
    try:
        resp, history = await request.get_resp(txt, history)
        if resp == None:
            raise RuntimeError("Response from ChatGLM server is None.\n\
                            Maybe you've reached the max_length limit?")

    #排查错误
    except Exception as e:
        logger.exception("对话失败", stack_info=True)
        message = f"啊哦~ 出现了以下错误呢……\n"
        for i in e.args:
            message += str(i)
        await chatglm.finish(message, at_sender=True)

    #保存历史对话
    if config.chatglm_mmry:
        await record.save_history(history,jsonpath)

    #转图片
    if config.chatglm_2pic:
        if resp.count("```") % 2 != 0:
            resp += "\n```"
        img = await md_to_pic(resp, width=config.chatglm_wide)
        resp = MessageSegment.image(img)

    #返回生成的文本
    if config.chatglm_rply:
        ans = MessageSegment.reply(event.message_id) + resp
        await chatglm.finish(ans)
    else:
        await chatglm.finish(resp, at_sender=True)

@clr_log.handle()   #清除历史功能
async def clear_history(event: MessageEvent):
    if await record.clr_history(event):
        await clr_log.finish("历史对话已清除。")
