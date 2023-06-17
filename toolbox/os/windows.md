# Windows 系统装机清单

## 网络


### ClashX

科学上网

[Releases · Fndroid/clash_for_windows_pkg](https://github.com/Fndroid/clash_for_windows_pkg/releases)
+ 下载 arm64.exe 安装版


### Chrome

基本浏览器

[离线安装包下载](https://support.google.com/chrome/answer/95346?co=GENIE.Platform%3DDesktop&hl=zh-Hans#zippy=%2Cwindows)


## 软件

### chocolatey

一款Windows上的包管理软件， [安装方式](https://chocolatey.org/install)。

#### 基本操作

**查找帮助**

```powershell
choco -?
```

**查找软件**

[Chocolatey Software | Packages](https://community.chocolatey.org/packages) —— 下载包的地方

**更新软件**

```powershell
choco upgrade 软件包名称
```

**卸载软件**

```powershell
choco uninstall 软件包名称
```

**列出软件**

```powershell
choco list
```

#### 软件清单
使用以下命令安装必备软件
```powershell
// 安装Node：
// Hexo 要用
choco install nodejs-lts  

// 安装 Git
choco install git.install

// 安装VSCode
choco install vscode

// 安装7-zip：
choco install 7zip.install

// 安装 Python
choco install python

// 安装 Utools 我喜爱的启动器
choco install yuanliao-utools

//  安装 PDF 阅读器
choco install sumatrapdf
```

**参考**
1. [Chocolatey安装和使用 - 掘金](https://juejin.cn/post/6994715287178182693)
2. [使用说明](https://docs.chocolatey.org/en-us/choco/setup)

## 工作

### TeXLive

每年一个版本，越来越大的TeX系统

[清华镜像下载](https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/texlive2023-20230313.iso)

### Adobe 生产力

1. Acrobat
2. Ps
3. Pr

链接：https://pan.baidu.com/s/1Hibc2bUbidIN0pxk3HOIyg?pwd=e39f 
提取码：e39f 

### Inkscape

画矢量图软件

```powershelll
choco install inkscape
```
### Jabref


```powershell
choco install jabref
```