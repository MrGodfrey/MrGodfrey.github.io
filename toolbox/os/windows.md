# Windows 系统装机清单

## 网络

### ClashX

科学上网

[Releases · Fndroid/clash_for_windows_pkg](https://github.com/Fndroid/clash_for_windows_pkg/releases)
+ 下载免安装版，解压即可使用

### Chrome

浏览器

[离线安装包下载](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=zh-Hans#zippy=%2Cwindows)


## 软件

### VSCode

官网下载相当慢，不知为何。

### Git

安装好后需要[设置用户名和邮箱](https://docs.github.com/zh/get-started/getting-started-with-git/setting-your-username-in-git)

```shell
git config --global user.name "Mona Lisa"
git config --global user.email "Email"
```

!> 为了避免繁琐的密码，可以保留自己的ssh文件，路径在 `C:\Users\<username>\.ssh`, 复制到新电脑中的相应位置即可


### chocolatey

一款Windows上的包管理软件， [安装方式](https://chocolatey.org/install)。

#### 基本操作

**查找帮助**

```shell
choco -?
```

**查找软件**

[Chocolatey Software | Packages](https://community.chocolatey.org/packages) —— 下载包的地方

**安装软件**

```shell
choco install 软件名1 软件名2 -y
```

`-y` 是同意所有的脚本


**更新软件**

```shell
choco upgrade 软件包名称
```

**卸载软件**

```shell
choco uninstall 软件包名称
```

**列出软件**

```shell
choco list
```

#### 软件清单
使用以下命令安装必备软件
```shell
// 安装Node：
// Hexo 要用
choco install nodejs-lts  

// 安装 Python
choco install python

//  安装 PDF 阅读器
choco install sumatrapdf
```

**参考**
1. [Chocolatey安装和使用 - 掘金](https://juejin.cn/post/6994715287178182693)
2. [使用说明](https://docs.chocolatey.org/en-us/choco/setup)

## 工作

### utools

[uTools官网 - 新一代效率工具平台](https://www.u.tools/)

快速启动器，相当好用。

### TeXLive

每年一个版本，越来越大的TeX系统。虽然体量大，但是能保证TeX的可编译性。一般我们只需要保证自己的文件能被编译出来。

[清华镜像下载](https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/texlive2023-20230313.iso)

### Adobe 生产力

1. Acrobat
2. Ps
3. Pr

链接：https://pan.baidu.com/s/1Hibc2bUbidIN0pxk3HOIyg?pwd=e39f 
提取码：e39f 

### Inkscape

画矢量图软件

```shell
choco install inkscape
```
### Jabref

bibtex 库文件管理软件

```shell
choco install jabref
```

### Pandoc

文档格式转化界的瑞士军刀

```shell
choco install pandoc
```