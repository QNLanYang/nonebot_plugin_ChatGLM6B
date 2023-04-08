<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-ChatGLM6B

_✨ ChatGPT 连不上？不如看看本地部署的 GLM 吧 ✨_

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/QNLanYang/nonebot_plugin_ChatGLM6B.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-chatglm6b">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-chatglm6b.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

如果你本地部署了 ChatGLM-6B，那么你可以使用一些大佬用 FastAPI 实现的 ChatGLM 加上我这个~~烂怂~~插件来将它接入你的 Bot，享受本地生成的速度。

## 📖 介绍

~~_首先本人技术很有限，插件都是照着别人的格式拼凑的，能用就行_~~

✨ 感谢 跨平台异步 Python 机器人框架 **[Nonebot](https://nb2.baka.icu/)** ✨

✨ 感谢 **[THUDM](https://github.com/THUDM)** 开源的 **[Chat GLM-6B](https://huggingface.co/THUDM/chatglm-6b)** ✨

✨ 感谢 **[imClumsyPand](https://github.com/imClumsyPanda)** 使用 FastAPI 实现的 **[ChatGLM-6B-API](https://github.com/imClumsyPanda/ChatGLM-6B-API)** ✨

✨ 感谢 **[A-kirami](https://github.com/A-kirami)** 制作的 Nonebot 插件 **[README 模板](https://github.com/A-kirami/nonebot-plugin-template)** ✨

#### 注意事项

本插件需要你有部署好的 ChatGLM-6B 并且成功运行 ChatGLM-6B-API
关于本地部署的细节请点击上方相关链接自行查询（或者我可以考虑 B 站出个教程 ~~如果给我点 star 的话~~）

### 最新消息

**v0.1.4** --> **v0.1.5**

✨ 感谢 **[KirbyScarlet](https://github.com/KirbyScarlet)** 的初次贡献 **[添加队列防止堵塞](https://github.com/QNLanYang/nonebot_plugin_ChatGLM6B/pull/19)** ✨

- 优化了 保存的历史记录文件的格式，加入换行使其更易读也更容易编辑；

**v0.1.3** --> **v0.1.4**

官方仓库 API 更新，本插件同步更新：

- 新增了 对官方新版 API 的适配，现在使用官方 API 也可以传入模型参数了；

## 💿 安装

<details>
<summary>使用 nb-cli 安装（推荐）</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-chatglm6b

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-chatglm6b

</details>

<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-chatglm6b

</details>

<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-chatglm6b

</details>

<details>
<summary>conda</summary>

    conda install nonebot-plugin-chatglm6b

</details>

<details>
<summary>然后，不要忘了下一步是……</summary>
打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_chatglm6b"]

</details>
</details>

<details>
<summary>手动安装</summary>
下载最新版本Release或main分支源码，将插件文件夹存放至Bot根目录的`./src/plugins/`目录中
（如果需要使用转图片功能则**必须**安装 *nonebot_plugin_hemlrender*）
（记得检查Bot根目录的`pyproject.toml`中`[tool.nonebot]` 部分有`plugin_dirs = ["src/plugins"]`
</details>

## ⚙️ 配置

不要忘记在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|    配置项    |  必填  |  类型  | 默认值  | 说明                                                          |
| :----------: | :----: | :----: | :-----: | :------------------------------------------------------------ |
| CHATGLM_ADDR | **是** | `str`  |   无    | 你的 ChatGLM API 的接口地址，_例如`http://127.0.0.1:11451`_   |
| CHATGLM_API  | **是** | `str`  |   无    | 你使用的 API 是谁提供的，_详情看表格下方的注释_               |
| CHATGLM_POKE |   否   | `bool` | `True`  | 收到请求后是否戳一戳发送者                                    |
| CHATGLM_2PIC |   否   | `bool` | `False` | 是否将收到的回答以图片形式发送                                |
| CHATGLM_WIDE |   否   | `int`  |  `400`  | 转图片时的图片宽度 _（单位：像素）_                           |
| CHATGLM_MMRY |   否   | `int`  |  `10`   | 对话时机器人所能记住的最大对话轮数，_设为`0`则每次都为新对话_ |
| CHATGLM_PBLC |   否   | `bool` | `False` | 在群聊中是否启用公共对话，_即群员共用对话历史_                |
| CHATGLM_RPLY |   否   | `bool` | `False` | 机器人返回内容时是否回复对应消息                              |

ℹ️**关于 CHATGLM_API**：_（大小写敏感）_

如果你使用的是 ChatGLM-6B 官方仓库里的 **[API.py](https://github.com/THUDM/ChatGLM-6B/blob/main/api.py)**，请在配置项填入 `official`

如果你使用的是 本项目致谢的 **[ChatGLM-6B-API](https://github.com/imClumsyPanda/ChatGLM-6B-API)**，请在配置项填入 `6b-api`

### 🔧 模型微调相关配置

|       配置项       | 必填 |  类型   | 默认值 | 说明                                                    |
| :----------------: | :--: | :-----: | :----: | :------------------------------------------------------ |
| CHATGLM_MODEL_LENG |  否  |  `int`  | `2048` | 模型的`max_length`参数，决定了模型接受输入的 token 上限 |
| CHATGLM_MODEL_TEMP |  否  | `float` | `0.95` | 模型的`temperature`参数，决定了模型输出对话的随机程度   |
| CHATGLM_MODEL_TOPP |  否  | `float` | `0.7`  | 模型的`top_P`参数，决定了模型输出与输入内容的相关性     |

**⚠ 注意**：所有配置项均还未设置取值范围检查，错误的设置可能带来严重的后果

## 🎉 使用

使用 `@Bot + [Bot命令前缀(如果有)] + GLM|# + [想问的内容]`来与 Bot 对话

### 指令表

|           指令           |  权限  | 需要@ |   范围    |     说明     |
| :----------------------: | :----: | :---: | :-------: | :----------: |
|       `GLM` \| `#`       | 所有人 |  是   | 私聊/群聊 |   对话起始   |
| `clrlog` \| `清除上下文` | 所有人 |  是   | 私聊/群聊 | 清除对话记录 |

## 🖼️ 效果图

![插件效果图](https://raw.githubusercontent.com/QNLanYang/nonebot_plugin_ChatGLM6B/main/.data/%E5%AF%B9%E8%AF%9D%E5%8F%8A%E8%AE%B0%E5%BF%86.png "对话和记忆")

~~效果图懒得改了，这是以前的，意思就是有记忆了~~

## ✅ 代办

- [x] ~~加入记忆保存上下文~~
- [x] ~~区分每个用户的对话历史，并加入可选参数选择群聊对话为私有或公开~~
- [x] ~~加入对更多 API 的支持——_官方 API:做好了_~~
- [ ] 加入对更多 API 的支持 _webui:不太好弄_
- [ ] 为配置项加入取值范围检查避免错误
- [ ] 将模型微调参数改为随时可调 _（通过命令或消息后附带参数）_
- [ ] 加入预设机器人人格
- [ ] 加入更多管理员指令

## 🌸 致谢

- [@A-kirami](https://github.com/A-kirami)，本项目使用了 README[模板](https://github.com/A-kirami/nonebot-plugin-template)，有修改
- [nonebot2](https://github.com/nonebot/nonebot2)，一切的基础
- [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)，可以跑在消费级显卡上的大语言模型
- [ChatGLM-6B-API](https://github.com/imClumsyPanda/ChatGLM-6B-API)，本项目的灵感来源，提供了与 GLM6B 交流的 API
- [nonebot-plugin-novelai](https://github.com/sena-nana/nonebot-plugin-novelai)，学习的对象，配置项导入的部分来源于此
- [nonebot-plugin-ChatGLM](https://github.com/DaoMingze/zhukebot/tree/main/zhukebot/plugins/chatglm)，与本项目相似，但是本地部署的版本，从中学习优化代码结构（或新功能？）~~开抄！~~
