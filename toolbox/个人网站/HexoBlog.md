
# 使用 Hexo 构建个人博客

Demo: [https://mrgodfrey.github.io/](https://mrgodfrey.github.io/) 


## 基本部署

我目前采用的是分成几个仓库的构造方法。
1. 主页是参考 [PhosphorW/hexo-theme-academia](https://github.com/PhosphorW/hexo-theme-academia) 主题生成的主页，直接写的 `index.html` 
2.  `thinking` 和 `toolbox` 是我利用 [docsify](/个人网站/使用docsify建立个人知识库.md) 写的，同样保存在 `mrgodfrey.github.io` 的仓库中
3. `blog` 是我利用 `Hexo` 生成的个人博客，源文件是保存在私有仓库中


### 本地部署

安装的流程可参考[文档 | Hexo](https://hexo.io/zh-cn/docs/)
 
在本地安装好后，需要利用 [One-Command Deployment | Hexo](https://hexo.io/docs/one-command-deployment#Git) 中的 `hexo-deployer-git` 方法部署到服务器中

1. 在 `hexo` 项目目录下运行安装 hexo-deployer-git

```shell
 npm install hexo-deployer-git --save
```

2. 在 `_config.yml` 中配置

```yml
  deploy:
    type: git
    repo: https://github.com/MrGodfrey/blog.git
    branch: gh-pages
```

> 这里将推送的分支设置为 `gh-pages`, 参考了 [issue](https://github.com/hexojs/hexo/issues/1081) 中的设置方法。此举的目的是为了之后使用 Github 自动部署网页.
>
> 为什么不直接用 `master` 呢？ 因为 `master` 分支中有不少内容是不需要被部署的，是 Hexo 运行依赖的东西。

3. 用 `hexo clean && hexo deploy` 将本地发布的内容推送到  `gh-pages` 分支

### Github 设置

1. 在 Github 存放 Hexo 文件的仓库, 我的是 `blog` 中， 点击 `setting->Pages`, 选择 `Deploy from a branch`.

> 不选择 Action 是因为我暂时还想在本地编译我的 Hexo 站点， 而非直接交给 Github 编译

2. 选择 Branch 为 `gh-pages` , 目录就是 `/(root)`, 即可

**参考**

1. [Configuring a publishing source for your GitHub Pages site - GitHub Docs](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## 问题
 
### 使用GitHub管理Hexo源文件时在子目录下找不到 Hexo

原因: 之前按照说明, 只是安装了Hexo的驱动程序. 从Github上同步下来Hexo 源文件后, 需要在目录中运行 `npm install`才能在当前目录装上 `hexo`

> npm install是一个命令，用于安装Node.js项目依赖的所有模块。它会在项目目录下查找package.json文件，读取其中的依赖项，并自动下载和安装这些依赖项。通过npm install命令，可以方便地管理项目的依赖项，保证项目的正常运行。



