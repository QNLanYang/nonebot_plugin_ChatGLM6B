from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (MessageEvent, PrivateMessageEvent,
                        GroupMessageEvent , Message, MessageSegment, Bot)
from nonebot.params import CommandArg

import aiohttp

from .save import record
from .check import check
from .config import config

if config.chatglm_2pic:
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import md_to_pic

#以上为import部分，以下为实现部分

chatglm = on_command("GLM", aliases={"#"}, priority=99, block=False, rule=to_me())

clr_log = on_command("清除上下文", aliases={"clrlog"}, priority=99, block=False, rule=to_me())

@chatglm.handle()
async def chat(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    #获取剔除前缀的用户输入纯文本
    txt = msg.extract_plain_text()

    #若没有输入则结束
    if txt == "" or txt is None:
        await chatglm.finish("你想问什么呢？", at_sender=True)

    #检查服务器状态
    if not await check.chk_server():
        logger.error("连接服务器失败，请检查服务器状态。")
        await chatglm.finish("服务器好像没有开启呢，问问我的主人吧！")
    
    #若响应成功则戳一戳用户
    await chatglm.send(Message(f'[CQ:poke,qq={event.user_id}]'))

    #读取历史对话记录
    if config.chatglm_mmry:
        uid = get_recpath(event)
        history = await record.load_history(uid)
    else:
        history = []

    #调用API
    try:
        resp, history = await get_resp(txt, history)

    #排查错误
    except Exception as e:
        logger.exception("对话失败")
        message = f"啊哦~"
        for i in e.args:
            message += str(i)
        await chatglm.finish(message, at_sender=True)

    #else:
    #得到正确回复
    #    resp, history = res.json()["response"], res.json()["history"]

    #保存历史对话
    if config.chatglm_mmry:
        await record.save_history(history,uid)

    #转图片
    if config.chatglm_2pic:
        if resp.count("```") % 2 != 0:
            resp += "\n```"
        img = await md_to_pic(resp, width=400)
        resp = MessageSegment.image(img)

    #返回生成的文本
    if config.chatglm_rply:
        ans = MessageSegment.reply(event.message_id) + resp
        await chatglm.finish(ans)
    else:
        await chatglm.finish(resp, at_sender=True)

@clr_log.handle()   #清除历史功能
async def clear_history(event=MessageEvent):
    uid = get_recpath(event)
    if await record.clr_history(uid):
        await clr_log.finish("历史对话已清除。")

def get_recpath(event):   #生成对应对话记录文件名
    if isinstance(event, GroupMessageEvent):
        uid = event.get_session_id()
        if config.chatglm_pblc:
            uid = uid.replace(f"{event.user_id}", "Public")
    else:
        uid = "Private_" + f"{event.user_id}"
    # if groupmessage get_session_id returns 'Group_{group_id}_{user_id}'
    return uid

async def get_resp(txt, history):
    #res = requests.post(f"{config.chatglm_addr}/predict?user_msg={txt}", json=history)
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{config.chatglm_addr}/predict?user_msg={txt}", json=history) as res:
                if res.status not in [200, 201]:
                    logger.error(await res.text())
                    raise RuntimeError(f"与服务器沟通时发生{res.status}错误")
                resp, history = (await res.json())["response"], (await res.json())["history"]
                return resp, history

    except aiohttp.ServerTimeoutError:  #响应超时
        logger.error("请求超时。\n" + res)
        raise RuntimeError(f"可恶，这个AI没反应了，要不炖了吧？")

    except aiohttp.InvalidURL:  #地址错误
        logger.error("API服务器地址格式有误")
        raise RuntimeError(f"配置有误，请反馈给我的主人。")

    except Exception as e:  #其他情况
        logger.error("error:" + str(e) + "\nresponse:" + await res.text())
        raise RuntimeError(f"请求时出现未知错误：{str(e)}")