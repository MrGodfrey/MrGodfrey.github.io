
# 使用 Hexo 构建个人博客

Demo: [https://mrgodfrey.github.io/](https://mrgodfrey.github.io/) 


## 基本部署

可参考[文档 | Hexo](https://hexo.io/zh-cn/docs/)


## 使用 GitHub action 部署

假设Hexo仓库在 `hexo`文件夹下
### 私有仓库准备

1. 删除 hexo 文件夹下theme中的 `.git` 文件
2.  `git init` 在Hexo 目录下新建空仓库
3. 在 Github 中新建一个私有仓库 `remote-hexo`，遵循指引将本地内容上传

### 新建 Github Page

1. 在 Github 中新建 `<username>.Github.io`仓库

### 创建 Github Action 脚本

1. 在 hexo 文件夹下新建 `.github/workflows/pages.yml`  文件，输入以下内容


```yaml
name: Pages #脚本名称

on: push ＃在push这个操作发生的时候执行脚本，也可以指定分支，默认master

jobs:
  pages:
    runs-on: ubuntu-latest #虚拟环境
    steps:
      - uses: actions/checkout@v2 #uses指令就是用的其它的现成的脚本
      - name: Use Node.js 12.x ＃name只是提供一个名称
        uses: actions/setup-node@v1
        with:                     ＃可以用with提供参数信息
          node-version: '12.x'
      - name: Cache NPM dependencies
        uses: actions/cache@v2
        with:
          path: node_modules
          key: ${{ runner.OS }}-npm-cache
          restore-keys: |
            ${{ runner.OS }}-npm-cache
      - name: Install Dependencies
        run: npm install

      ＃上面的操作都是为了准备环境


      - name: Build ＃生成
        run: npm run build ＃这里需要保证你博客根目录下的package.json文件中有这个脚本，没有的话添加一下"build": "hexo generate"
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3　＃这是一个自动化部署到github pages的脚本
        with:
          personal_token: ${{ secrets.HEXO_DEPLOY }} ＃HEXO_DEPLOY这个名称跟源文件仓库中设置的要对应
          external_repository: <username>/<username>.github.io  ＃添加部署的目标仓库，也就是github.io对应的仓库，由＂用户名／仓库名＂的方式指定
          publish_dir: ./public ＃需要发布的文件目录，hexo generate生成的就是./public
          publish_branch: master  # deploying branch 部署的分支，对应我们的external_repository
```

1. 在Github用户设置中生成名为 `HEXO_DEPLOY`的密钥，具体位置在 `头像->Settings->Developer settings->Personal access tokens->Generate new token` 
   1. 需要打开 `repo`和 `workflow`权限.
   2. 这里生成的密钥要记录下来，第3步中复制过去
2. 在 `remote-hexo`中 `Settings->Secrets->New repository secret` 添加名为 `HEXO_DEPLOY`的密钥， 内容为第2步中复制的

> 每次 `git push`之后就可以自动更新到 GitHub Page 中了


**参考**

1. [用github actions自动化布署hexo博客-从私有仓库到公共仓库](https://www.fewth.com/%E7%94%A8github-actions%E8%87%AA%E5%8A%A8%E5%8C%96%E5%B8%83%E7%BD%B2hexo%E5%8D%9A%E5%AE%A2-%E4%BB%8E%E7%A7%81%E6%9C%89%E4%BB%93%E5%BA%93%E5%88%B0%E5%85%AC%E5%85%B1%E4%BB%93%E5%BA%93/)
2. [在 GitHub Pages 上部署 Hexo](https://hexo.io/zh-cn/docs/github-pages#%E4%B8%80%E9%94%AE%E9%83%A8%E7%BD%B2)

## 问题
 
### 使用GitHub管理Hexo源文件时在子目录下找不到 Hexo

原因: 之前按照说明, 只是安装了Hexo的驱动程序. 从Github上同步下来Hexo 源文件后, 需要在目录中运行 `npm install`才能在当前目录装上 `hexo`


>npm install是一个命令，用于安装Node.js项目依赖的所有模块。它会在项目目录下查找package.json文件，读取其中的依赖项，并自动下载和安装这些依赖项。通过npm install命令，可以方便地管理项目的依赖项，保证项目的正常运行。



