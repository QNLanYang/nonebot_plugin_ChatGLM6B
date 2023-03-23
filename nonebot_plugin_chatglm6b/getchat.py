from nonebot import on_command, require
from nonebot.rule import to_me
from nonebot.log import logger
from nonebot.adapters.onebot.v11 import (MessageEvent, PrivateMessageEvent,
                        GroupMessageEvent , Message, MessageSegment, Bot)
from nonebot.params import CommandArg

import httpx

from .utils import config, record

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
    
    #若响应成功则戳一戳用户
    await chatglm.send(Message(f'[CQ:poke,qq={event.user_id}]'))

    #读取历史对话记录
    if config.chatglm_mmry:
        uid = get_recpath(event)
        history = await record.load_history(uid)
    else:
        history = []

    res = ""
    #调用API
    try:
        #res = requests.post(f"{config.chatglm_addr}/predict?user_msg={txt}", json=history)
        async with httpx.AsyncClient(timeout=httpx.Timeout(15.0)) as client:
            res = await client.post(f"{config.chatglm_addr}/predict?user_msg={txt}", json=history)
            res.raise_for_status()

    #排查错误
    
    except httpx.ConnectTimeout:
        logger.error("连接服务器失败，请检查服务器状态\n" + res)
        await chatglm.finish("服务好像没有开启呢，问问我的主人吧！", at_sender=True)

    except httpx.NetworkError:
        logger.error("出错了，请检查网络状态\n" + res)
        await chatglm.finish("ChatGLM被玩坏了，这绝对不是ChatGLM的问题，绝对不是。", at_sender=True)

    except httpx.TimeoutException:
        logger.error("请求超时。\n" + res)
        await chatglm.finish("可恶，这个AI没反应了，要不炖了吧？", at_sender=True)

    except httpx.InvalidURL:
        logger.error("API服务器地址格式有误")
        await chatglm.finish("配置有误，请反馈给我的主人。", at_sender=True)

    except Exception as e:
        logger.error("error:" + str(e) + "\nresponse:" + res)
        await chatglm.finish(f"请求时出现未知错误：{str(e)}", at_sender=True)
    
    #得到正确回复
    resp, history = res.json()["response"], res.json()["history"]

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