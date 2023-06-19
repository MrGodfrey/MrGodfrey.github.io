
# 国内可用的 ChatGPT 部署方法

总所周知， ChatGPT 在中国是用不了的。
与其小心谨慎地采用各种奇淫巧计，还要担心被封号，不如直接用 ChatGPT 的 Api, 以及各类替代。


## 前期准备

1. 申请一个Github帐号：[Github](https://github.com/)
2. 申请一个API2D帐号并充值： [API2D](https://api2d.com/reg/email)（充值需要信用卡）


?> 用我的推荐链接充值有点数优惠：[https://api2d.com/r/198143](https://api2d.com/r/198143)

## 部署网页版


[Yidadaa/ChatGPT-Next-Web](https://github.com/Yidadaa/ChatGPT-Next-Web#keep-updated) 还在频繁的开发， 那么如何升级新的版本呢？

遵循指南 [keep-updated](https://github.com/Yidadaa/ChatGPT-Next-Web#keep-updated), 需要执行以下步骤

1. 重新 fork [Yidadaa/ChatGPT-Next-Web](https://github.com/Yidadaa/ChatGPT-Next-Web#keep-updated)
2. 在 vercel 中新建项目， 选择第一步中的仓库
3. 配置环境变量
   1. 新建 `BASE_URL` 环境变量, 值为 `openai.api2d.net`
   2. 新建 `OPENAI_API_KEY` 环境变量，值为 `API2D中的 Forward Key` 
   3. 新建 `CODE` 环境变量，值为 `自己设置的密码`
4. 点击 `Deploy`， 等待五分钟左右即可

安装好后， 访问 Vercel 提供的链接，在登录页面中填入你自己设定的 CODE 即可.

为了将来无缝的升级这一应用，最好自己申请一个可访问的域名。

!> 任何知道你 CODE 和 Vercel 应用网址的人都能使用你的 ChatGPT。 CODE 要设置的比较复杂，不能是123，否则会有别人偷跑你的流量


**参考**
1. [ChatGPT-Next-Web/vercel-cn.md at main · Yidadaa/ChatGPT-Next-Web · GitHub](https://github.com/Yidadaa/ChatGPT-Next-Web/blob/main/docs/vercel-cn.md) —— vercel 部署帮助
2. [【API2D】配置和使用 ChatGPT Next Web_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1zT411p7dg/?vd_source=4d55e615e34201407bdaaa9275aa62bc)


## 其他插件


### 浏览器插件 - chatGPTBox

[josStorer/chatGPTBox: Integrating ChatGPT into your browser deeply, everything you need is here](https://github.com/josStorer/chatGPTBox)

chatGPTBox	[📼 教程链接](https://www.bilibili.com/video/BV1bo4y1h7Hb) 浏览器插件可将 ChatGPT 深度集成到浏览器，适配各种搜索引擎和常用站点

中文简介 - [chatGPTBox/README_ZH.md at master · josStorer/chatGPTBox](https://github.com/josStorer/chatGPTBox/blob/master/README_ZH.md)

#### 小技巧

1.  在任何页面随时呼出聊天对话框 (Ctrl+B)
2. 通过右键菜单总结任意页面 (Alt+B)
3. 框选工具与右键菜单, 执行各种你的需求, 如翻译, 总结, 润色, 情感分析, 段落划分, 代码解释, 问询

### ChatGPT for VSCode

[ChatGPT: write and improve code using AI - Visual Studio Marketplace](https://marketplace.visualstudio.com/items?itemName=timkmecl.chatgpt)

#### 小技巧

1. 在设置中填入自己的prompt, 可以重构他的命令, 比如我把Refactor换成了自己定义的英文润色



**参考**

1. [GitHub - easychen/openai-gpt-dev-notes-for-cn-developer: 如何快速开发一个OpenAI/GPT应用：国内开发者笔记](https://github.com/easychen/openai-gpt-dev-notes-for-cn-developer)
2. API2D 官网： [API2D](https://api2d.com/reg/email)
3. [Dashboard – Vercel](https://vercel.com/dashboard)

