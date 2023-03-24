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

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(f"{config.chatglm_addr}/predict?user_msg={txt}&max_length={config.chatglm_model_leng}&top_p={config.chatglm_model_topp}&temperature={config.chatglm_model_temp}", json=history) as res:
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

request = Request()