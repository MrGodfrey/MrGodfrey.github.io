# 使用 docsify 建立个人知识库


docsify 的原理是直接在网页上渲染 MarkDown 文件，与传统的本地渲染文件，再上传 html 到服务器有本质的区别。

代价就是浏览器承担了更大的压力，但好处在于
1. 部署相当简单，本质上其实就是一个预先设定好的网页
2. 只需要维护一份 Markdown 文件 
3. 生成的是一本书而非时间流博客

## 安装

初次使用，建议遵循 docsify 官方网站 [快速开始](https://docsify.js.org/#/zh-cn/quickstart) 的步骤.

嫌麻烦不想装 `npm` 的人，可以用以下步骤, 当然 `python` 得装上.

1. 克隆我的 [仓库](https://github.com/MrGodfrey/MrGodfrey.github.io) 到本地
2. 仓库中的 `docs` 文件夹就是一个设置好的 docsify 项目

本地预览效果, 可以运行 `python localServe` 

## 使用技巧

### 多个知识库

可以在同一个项目中放很多个不同的 docsify 实例，从而实现一处仓库托管好几本书。

注意到此时在本地运行的server访问不到跨文件夹的东西。比如 `docs` 启动的 server 访问不到 `toolbox` 中的信息。

可以在根目录下直接运行server，就可以互相访问了.

### 切换主题

[docsify-themeable](https://jhildenbiddle.github.io/docsify-themeable/#/quick-start) 是个相当漂亮的主题, 2022年还在更新.


### 数学公式

使用 [upupming/docsify-katex: KaTeX support for docsify](https://github.com/upupming/docsify-katex) 即可
