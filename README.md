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
关于本地部署的细节请点击上方相关链接自行查询（或者我可以考虑B站出个教程 ~~如果给我点star的话~~）

### 最新消息

**v0.1.0** --> **v0.1.1**
一次小的更新，主要内容有：

- 修复了	清除对话记录无反应的问题；
- 修复了	配置项 *CHATGLM_WIDE* 失效的问题；
- 修复了	部分配置项未配置时默认值出错的问题；
- 新增了	对服务器返回消息但内容为空的异常处理；
  *可能是由于输入内容长度（含历史记录）超出模型设置*
- 针对上一条情况新增了配置项以微调模型参数；
  		*需要同步更新 [ChatGLM-6B-API](https://github.com/imClumsyPanda/ChatGLM-6B-API) 以支持模型微调*
    	*（上述更新还包含显存释放以及模型重复载入的bug，强烈建议更新）*


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
（记得检查Bot根目录的`pyproject.toml`中`[tool.nonebot]` 部分有`plugin_dirs = ["src/plugins"]`
</details>

## ⚙️ 配置

不要忘记在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|    配置项    | 必填 |  类型  | 默认值  | 说明                                                        |
| :----------: | :--: | :----: | :-----: | :---------------------------------------------------------- |
| CHATGLM_ADDR |  是  | `str`  |   无    | 你的 ChatGLM API 的接口地址，例如`http://127.0.0.1:11451`   |
| CHATGLM_POKE |  否  | `bool` | `True`  | 收到请求后是否戳一戳发送者                                  |
| CHATGLM_2PIC |  否  | `bool` | `False` | 是否将收到的回答以图片形式发送                              |
| CHATGLM_WIDE |  否  | `int`  |  `400`  | 转图片时的图片宽度（单位：像素）                            |
| CHATGLM_MMRY |  否  | `int`  |  `10`   | 对话时机器人所能记住的最大对话轮数，设为`0`则每次都为新对话 |
| CHATGLM_PBLC |  否  | `bool` | `False` | 在群聊中是否启用公共对话，即群员共用对话历史                |
| CHATGLM_RPLY |  否  | `bool` | `False` | 机器人返回内容时是否回复对应消息                            |

### 模型微调相关配置

|       配置项       | 必填 | 类型  | 默认值 | 说明                                                  |
| :----------------: | :--: | :---: | :----: | :---------------------------------------------------- |
| CHATGLM_MODEL_LENG |  否  | `int` |  2048  | 模型的`max_length`参数，决定了模型接受输入的token上限 |
| CHATGLM_MODEL_TEMP |  否  | float |  0.95  | 模型的`temperature`参数，决定了模型输出对话的随机程度 |
| CHATGLM_MODEL_TOPP |  否  | float |  0.7   | 模型的`top_P`参数，决定了模型输出与输入内容的相关性   |


## 🎉 使用

使用 `@Bot + [Bot命令前缀(如果有)] + GLM|# + [想问的内容]`来与 Bot 对话

### 指令表

|        指令        |  权限  | 需要@ |   范围    |     说明     |
| :----------------: | :----: | :---: | :-------: | :----------: |
|       GLM\|#       | 所有人 |  是   | 私聊/群聊 |   对话起始   |
| clrlog\|清除上下文 | 所有人 |  是   | 私聊/群聊 | 清除对话记录 |

## 🖼️ 效果图

![插件效果图](https://raw.githubusercontent.com/QNLanYang/nonebot_plugin_ChatGLM6B/main/.data/%E5%AF%B9%E8%AF%9D%E5%8F%8A%E8%AE%B0%E5%BF%86.png "对话和记忆")

~~效果图懒得改了，这是以前的，意思就是有记忆了~~

## ✅ 代办

- [x] ~~加入记忆保存上下文~~
- [x] ~~区分每个用户的对话历史，并加入可选参数选择群聊对话为私有或公开~~
- [ ] 将模型微调参数改为随时可调（通过命令以及消息后附带参数）
- [ ] 加入预设机器人人格
- [ ] 加入更多管理员指令

## 🌸 致谢

- [@A-kirami](https://github.com/A-kirami)，本项目使用了 README[模板](https://github.com/A-kirami/nonebot-plugin-template)，有修改
- [nonebot2](https://github.com/nonebot/nonebot2)，一切的基础
- [ChatGLM-6B](https://github.com/THUDM/ChatGLM-6B)，可以跑在消费级显卡上的大语言模型
- [ChatGLM-6B-API](https://github.com/imClumsyPanda/ChatGLM-6B-API)，提供了与GLM6B交流的API
- [nonebot-plugin-novelai](https://github.com/sena-nana/nonebot-plugin-novelai)，学习的对象，配置项导入的部分来源于此
- [nonebot-plugin-ChatGLM](https://github.com/DaoMingze/zhukebot/tree/main/zhukebot/plugins/chatglm)，与本项目相似，但是本地部署的版本，从中学习优化代码结构（或新功能？）~~开抄！~~
