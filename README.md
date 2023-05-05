# 开发版中药关系抽取

## 介绍

🌍 [原始项目说明文档](README_cn.md)

💡 基于 [imClumsyPanda /langchain-ChatGLM](https://github.com/imClumsyPanda/langchain-ChatGLM) 项目开发，分支master。

## 功能

✅ 自动将从PubMed上爬取的包含摘要的XLSX文件转换为以PMID命名的TXT文件。

✅ 自动调用OpenAI提供的模型进行关系抽取，支持整个文件夹批量处理。

✅ 自动将抽取出的关系保存到XLSX文档或MYSQL数据库中。

![实现原理图](img/langchain+chatglm.png)

从文档处理角度来看，实现流程如下：

![实现原理图2](img/langchain+chatglm2.png)

🚩 本项目未涉及微调、训练过程，但可利用微调或训练对本项目效果进行优化。

🌐 [AutoDL 镜像](https://www.codewithgpu.com/i/imClumsyPanda/langchain-ChatGLM/langchain-ChatGLM)

📓 [ModelWhale 在线运行项目](https://www.heywhale.com/mw/project/643977aa446c45f4592a1e59)




## 开发部署

### 1. 安装环境

```shell
# 安装依赖
$ pip install -r requirements.txt
```

### 2. 设置模型默认参数

在开始执行 Web UI 或命令行交互前，请先检查 [configs/model_config.py](configs/model_config.py) 中的各项模型参数设计是否符合需求。

### 3. 执行脚本体验 Web UI 或命令行交互

> 注：鉴于环境部署过程中可能遇到问题，建议首先测试命令行脚本。建议命令行脚本测试可正常运行后再运行 Web UI。

执行 [cli_demo.py](cli_demo.py) 脚本体验**命令行交互**：
```shell
$ python cli_demo.py
```

或执行 [webui.py](webui.py) 脚本体验 **Web 交互**

```shell
$ python webui.py
```

或执行 [api.py](api.py) 利用 fastapi 部署 API
```shell
$ python api.py
```


注：如未将模型下载至本地，请执行前检查`$HOME/.cache/huggingface/`文件夹剩余空间，至少15G。

执行后效果如下图所示：
![webui](img/webui_0419.png)
Web UI 可以实现如下功能：

1. 运行前自动读取`configs/model_config.py`中`LLM`及`Embedding`模型枚举及默认模型设置运行模型，如需重新加载模型，可在 `模型配置` 标签页重新选择后点击 `重新加载模型` 进行模型加载；
2. 可手动调节保留对话历史长度、匹配知识库文段数量，可根据显存大小自行调节；
3. 具备模式选择功能，可选择 `LLM对话` 与 `知识库问答` 模式进行对话，支持流式对话；
4. 添加 `配置知识库` 功能，支持选择已有知识库或新建知识库，并可向知识库中**新增**上传文件/文件夹，使用文件上传组件选择好文件后点击 `上传文件并加载知识库`，会将所选上传文档数据加载至知识库中，并基于更新后知识库进行问答；
5. 后续版本中将会增加对知识库的修改或删除，及知识库中已导入文件的查看。

### 常见问题

参见 [常见问题](docs/FAQ.md)。

## Demo

以问题`chatglm-6b 的局限性具体体现在哪里，如何实现改进`为例：

未使用 langchain 接入本地文档时：

>ChatGLM-6B 是一个基于 GPT-3 的聊天机器人,它的局限性主要体现在以下几个方面:
>1. 语言模型的精度:GPT-3 是一种大型的语言模型,它的精度比较高,但是仍然有一些局限性。例如,它可能无法准确地理解某些方言、口音或者复杂的句子结构。
>2. 知识图谱的完整性:GPT-3 可以生成一些知识图谱,但是其完整性和准确性可能不够。例如,它可能无法准确地理解某些领域的专业知识和术语。
>3. 对话生成的连贯性:GPT-3 可以生成一些连贯的对话,但是其生成的对话可能不够自然。例如,它可能会生成一些虚假的、不连贯的对话或者误解用户的意图。
>
>为了改进 ChatGLM-6B,可以考虑以下几个方面:
>1. 提高语言模型的精度:可以通过增加训练数据、使用更好的语言模型架构、优化模型训练过程等方式来提高语言模型的精度。
>2. 增强知识图谱的完整性:可以通过增加知识图谱的维度、使用更好的知识图谱构建方法、优化知识图谱的匹配算法等方式来增强知识图谱的完整性。
>3. 提高对话生成的连贯性:可以通过增加对话生成模型的上下文信息、使用更好的上下文信息提取方法、优化对话生成模型的算法等方式来提高对话生成的连贯性。
>4. 引入更多的人类反馈:人类反馈可以帮助 ChatGLM-6B 更好地理解用户的意图和需求,从而提高对话生成的质量和准确性。可以通过引入更多的人类客服、使用人类反馈收集器等方式来引入更多的人类反馈。

使用 langchain 接入 ChatGLM-6B 项目的 README.md 文件后 ChatGLM 的回答：
>ChatGLM-6B 是一个基于深度学习的自然语言处理模型,它在回答问题方面表现出色。但是,它也有一些局限性,具体如下:
>1. 语言理解有限:ChatGLM-6B 只学习了中文自然语言,对于其他语言可能会存在理解上的局限性。
>2. 知识储备不足:ChatGLM-6B 的训练数据集只包含了中文语料,因此它可能无法回答一些非中文的问题或者某些特定领域的问题。
>3. 数据量有限:ChatGLM-6B 的训练数据集只有几百万条记录,因此它可能无法回答一些非常具体或者复杂的问题。
>
>为了改进 ChatGLM-6B,可以考虑以下几个方面:
>1. 学习更多的语言知识:可以学习其他语言的自然语言处理技术,扩大语言理解的范围。
>2. 扩大知识储备:可以收集更多的中文语料,或者使用其他语言的数据集来扩充知识储备。
>3. 增加数据量:可以使用更大的数据集来训练 ChatGLM-6B,提高模型的表现。
>4. 引入更多的评估指标:可以引入更多的评估指标来评估模型的表现,从而发现 ChatGLM-6B 存在的不足和局限性。
>5. 改进模型架构:可以改进 ChatGLM-6B 的模型架构,提高模型的性能和表现。例如,可以使用更大的神经网络或者改进的卷积神经网络结构。

## 路线图

- [ ] Langchain 应用
  - [x] 接入非结构化文档（已支持 md、pdf、docx、txt 文件格式）
  - [ ] 搜索引擎与本地网页接入
  - [ ] 结构化数据接入（如 csv、Excel、SQL 等）
  - [ ] 知识图谱/图数据库接入
  - [ ] Agent 实现
- [ ] 增加更多 LLM 模型支持
  - [x] [THUDM/chatglm-6b](https://huggingface.co/THUDM/chatglm-6b)
  - [x] [THUDM/chatglm-6b-int8](https://huggingface.co/THUDM/chatglm-6b-int8)
  - [x] [THUDM/chatglm-6b-int4](https://huggingface.co/THUDM/chatglm-6b-int4)
  - [x] [THUDM/chatglm-6b-int4-qe](https://huggingface.co/THUDM/chatglm-6b-int4-qe)
  - [x] [ClueAI/ChatYuan-large-v2](https://huggingface.co/ClueAI/ChatYuan-large-v2)
- [ ] 增加更多 Embedding 模型支持
  - [x] [nghuyong/ernie-3.0-nano-zh](https://huggingface.co/nghuyong/ernie-3.0-nano-zh)
  - [x] [nghuyong/ernie-3.0-base-zh](https://huggingface.co/nghuyong/ernie-3.0-base-zh)
  - [x] [shibing624/text2vec-base-chinese](https://huggingface.co/shibing624/text2vec-base-chinese)
  - [x] [GanymedeNil/text2vec-large-chinese](https://huggingface.co/GanymedeNil/text2vec-large-chinese)
- [ ] Web UI
  - [x] 利用 gradio 实现 Web UI DEMO
  - [x] 添加输出内容及错误提示
  - [x] 引用标注
  - [ ] 增加知识库管理
    - [x] 选择知识库开始问答
    - [x] 上传文件/文件夹至知识库
    - [ ] 删除知识库中文件
  - [ ] 利用 streamlit 实现 Web UI Demo
- [ ] 增加 API 支持
  - [x] 利用 fastapi 实现 API 部署方式
  - [ ] 实现调用 API 的 Web UI Demo

## 项目交流群
![二维码](img/qr_code_10.jpg)

🎉 langchain-ChatGLM 项目交流群，如果你也对本项目感兴趣，欢迎加入群聊参与讨论交流。
