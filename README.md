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

✨感谢 跨平台异步Python机器人框架 **[Nonebot](https://nb2.baka.icu/)** ✨

✨感谢 **[THUDM](https://github.com/THUDM)** 开源的 **[Chat GLM-6B](https://huggingface.co/THUDM/chatglm-6b)** ✨

✨感谢 **[imClumsyPand](https://github.com/imClumsyPanda)** 使用FastAPI实现的 **[ChatGLM-6B-API](https://github.com/imClumsyPanda/ChatGLM-6B-API)** ✨

#### 注意事项

本插件需要你有部署好的 ChatGLM-6B 并且成功运行 ChatGLM-6B-API
关于本地部署的细节请点击上方相关链接自行查询



## 💿 安装

<details>
<summary>使用 nb-cli 安装（推荐）</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-example

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-example

</details>
打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_chatglm6b"]

</details>

<details>
<summary>手动安装</summary>
下载最新版本Release，将文件夹存放至Bot根目录的`./src/plugins/`目录中
</details>


## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 类型 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|------|
| CHATGLM_ADDR | 是 | str | 无 | 你的ChatGLM API的接口地址，例如`http://127.0.0.1:11451` |
| CHATGLM_POKE | 否 | bool | True | 收到请求后是否戳一戳发送者 |
| CHATGLM_2PIC | 否 | bool | False | 是否将收到的回答以图片形式发送 |
| CHATGLM_WIDE | 否 | int | 400 | 转图片时的图片宽度 |
| CHATGLM_MMRY | 否 | int | 10 | 对话时机器人所能记住的最大对话轮数，设为0则每次都为新对话 |



## 🎉 使用

使用 `@Bot + [Bot命令前缀(如果有)] + GLM|# + [想问的内容]`来与Bot对话 

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| GLM\|# | 所有人 | 是 | 私聊/群聊 | 对话起始 |
| clrlog\|清除上下文 | 所有人 | 是 | 私聊/群聊 | 清除对话记录 |


## ✅ 代办

- [x]  加入记忆保存上下文
- [ ]  区分每个用户的对话历史，并加入可选参数选择群聊对话为私有或公开
