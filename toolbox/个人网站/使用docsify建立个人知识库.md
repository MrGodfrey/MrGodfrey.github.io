# 使用 docsify 建立个人知识库


docsify 的原理是直接在网页上渲染 MarkDown 文件，与传统的本地渲染文件，再上传 html 到服务器有本质的区别。

代价就是浏览器承担了更大的压力，但好处在于
1. 部署相当简单 
2. 只需要维护一份 Markdown 文件 
3. 生成的是一本书而非时间流博客

## 安装

遵循官网[快速开始](https://docsify.js.org/#/zh-cn/quickstart)的步骤即可。

## 使用技巧

### 多个知识库

可以在同一个项目中放很多个不同的 docsify 实例，从而实现一处仓库托管好几本书。


## 数学公式

使用 [upupming/docsify-katex: KaTeX support for docsify](https://github.com/upupming/docsify-katex) 即可