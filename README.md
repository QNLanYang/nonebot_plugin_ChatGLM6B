<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ChatGLM6B

_✨ ChatGPT连不上？不如看看本地部署的GLM吧 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/QNLanYang/nonebot_plugin_ChatGLM6B.svg" alt="license">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

如果你本地部署了ChatGLM-6B，那么你可以使用一些大佬用FastAPI实现的ChatGLM加上我这个~~烂怂~~插件来将它接入你的Bot，享受本地生成的速度。

## 📖 介绍

~~*首先本人技术很有限，插件都是照着别人的格式拼凑的，能用就行*~~



## 💿 安装

Clone本项目到你的Bot根目录的`./src/plugins/`目录下。


打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_ChatGLM6B"]



## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| CHATGLM_ADDR | 是 | 无 | 你的ChatGLM API的接口地址，例如`http://127.0.0.1:11451` |
| CHATGLM_POKE | 否 | True | 收到请求后是否戳一戳发送者 |
| CHATDLM_2PIC | 否 | False | 是否将收到的回答以图片形式发送 |

## 🎉 使用
使用 `@Bot + [Bot命令前缀(如果有)] + GLM|. + [想问的内容]`来与Bot对话 

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| GLM | 所有人 | 是 | 私聊/群聊 | 对话起始 |
| # | 所有人 | 是 | 私聊/群聊 | 对话起始 |
### 效果图
*还没*