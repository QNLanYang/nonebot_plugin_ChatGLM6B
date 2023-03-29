from nonebot.log import logger

import aiohttp

from .config import config

class Request:
    #检查服务器连通性
    async def chk_server(self):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{config.chatglm_addr}/") as test:
                    if (await test.json())["message"]!="Hello ChatGLM API!":
                        return False
                    return True
        except aiohttp.ClientConnectorError:
            logger.exception("无法连接至服务器", stack_info=True)
            return False

    #发送请求
    async def get_resp(self, txt, history):

        if config.chatglm_api == "6b-api":  #使用我推荐的API
            url = (f"{config.chatglm_addr}/predict?"+
                    f"user_msg={txt}"+
                    f"&max_length={config.chatglm_model_leng}"+
                    f"&top_p={config.chatglm_model_topp}"+
                    f"&temperature={config.chatglm_model_temp}")
            json = history

        elif config.chatglm_api == "official":  #使用官方API
            url = f"{config.chatglm_addr}/"
            json = {"prompt": txt, "history": history,
                    "max_length": config.chatglm_model_leng,
                    "temperature": config.chatglm_model_temp,
                    "top_p": config.chatglm_model_topp}
        
        else:   #没有匹配的API
            raise ValueError("请选择正确的API配置！")

        res: aiohttp.ClientResponse = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json = json) as res:
                    if res.status != 200:   #HTTP error
                        logger.error(await res.text())
                        raise RuntimeError(f"与服务器沟通时发生{res.status}错误")
                    resp, history = (await res.json())["response"], (await res.json())["history"]
                    if not resp:    #确保有返回内容
                        raise RuntimeError("Response from ChatGLM server is None.\n\
                            Maybe you've reached the max_length limit?")
                    return resp, history

        except aiohttp.ClientConnectorError:  #响应超时
            logger.error("请求超时。\n")
            raise RuntimeError(f"可恶，这个AI没反应了，要不炖了吧？")

        except aiohttp.InvalidURL:  #地址错误
            logger.error("API服务器地址格式有误")
            raise RuntimeError(f"配置有误，请反馈给我的主人。")

        except Exception as e:  #其他情况
            logger.error("error:" + str(e) + "\nresponse:" + await res.text())
            raise RuntimeError(f"请求时出现错误：{str(e)}")

request = Request()