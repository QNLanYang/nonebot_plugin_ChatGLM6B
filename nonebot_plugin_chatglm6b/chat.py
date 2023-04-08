from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (MessageEvent,
                            Message, MessageSegment, Bot)
from nonebot.params import CommandArg, _shell_command_argv
from collections import deque
import asyncio

from .save import record
from .request import request
from .config import config

chat_queue: deque = deque([])

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
    if config.chatglm_poke:
        await chatglm.send(Message(f'[CQ:poke,qq={event.user_id}]'))

    #检查服务器状态 (暂时弃用)
#    if config.chatglm_api == "6b-api":
#        if not await request.chk_server():
#            logger.error("连接服务器失败，请检查服务器状态。")
#            await chatglm.finish("服务器好像没有开启呢，问问我的主人吧！")

    #简易的消息队列控制，一定程度上防止群友们一股脑问问题问爆显存
    chat_queue.append(event)
    while True:

        if chat_queue[0] is event:    
        #读取历史对话记录
            if config.chatglm_mmry:
                history, jsonpath = await record.load_history(event)
            else:
                history = []

            #调用API
            try:
                resp, history = await request.get_resp(txt, history)

            #排查错误
            except Exception as e:
                logger.exception("对话失败", stack_info=True)
                message = f"唔……出状况了。\n"
                for i in e.args:
                    message += str(i)
                await chatglm.finish(message, at_sender=True)
            
            finally:
                chat_queue.popleft()

            #保存历史对话
            if config.chatglm_mmry:
                await record.save_history(history, jsonpath)

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

        else:
            await asyncio.sleep(1)

@clr_log.handle()   #清除历史功能
async def clear_history(event: MessageEvent):
    if await record.clr_history(event):
        await clr_log.finish("你的历史对话已清除。", at_sender=True)
