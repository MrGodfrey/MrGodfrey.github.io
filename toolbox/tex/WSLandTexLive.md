# WSL 上安装 TexLive

TeX 在 Linux 系统中编译的速度大大快于 Windows 系统，为此，可以在Windows中配置 WSL 系统。并在该系统中安装 TeXLive。

## 安装

### 下载镜像

[清华镜像下载](https://mirrors.tuna.tsinghua.edu.cn/CTAN/systems/texlive/Images/texlive2023-20230313.iso)

右键单击好的 `iso` 文件，选择装载。记住出现的盘符，我的是 `E:`

### 在WSL中安装

我的 WSL 是 `Ubuntu` 系统。

使用如下命令安装 TeXLive.
```bash
sudo mkdir /mnt/img
sudo mount -t drvfs E: /mnt/img
sudo mnt/img/install-tl
```

注意在安装时可以按 `O` 选择将 create symlinks to standard directories, 自动创建符号链接。

若是错过这一步，也可以用TeXLive自带的包管理器 `tlmgr` 自动将路径添加到默认目录中
```bash
sudo /usr/local/texlive/2020/bin/x86_64-linux/tlmgr path add
```

!> 使用 `xelatex` 引擎需要[配置字体](#字体配置). 

## 配置

### Git

我的论文是存在Github中的，为了在Ubuntu中修改，需要克隆下来

首先生成 SSH 密钥
```bash
ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

打开公钥文件 `~/.ssh/id_rsa.pub` 并复制文件内容

在Github的 Settings “SSH and GPG keys” “New SSH key”， 添加刚才的公钥即可

### 代理

可以使用 Clash 直接配置代理，打开 allow lan 开关后，会直接看到 WSL 系统的ip地址 `${hostip}`

在WSL中运行 
```bash
export https_proxy="http://${hostip}:7890";
export http_proxy="http://${hostip}:7890";
```
将 `${hostip}` 替换为ip地址

测试
```bash
curl google.com
```
正常返回即可

### 字体配置

?> 注意到如果用的是 `xelatex` 引擎，那么会报错，此时就需要配置字体运行库.

需要使用 Windows 系统的字体，可以采用如下方式

首先更新 `apt-get`
```bash
sudo apt-get update
```

安装 `fontconfig`
```bash
sudo apt install fontconfig
```

在 `/etc/fonts/` 新建一个文件 `local.conf`， 添加以下内容：
```xml
<?xml version="1.0"?>
<!DOCTYPE fontconfig SYSTEM "fonts.dtd">
<fontconfig>
    <dir>/mnt/c/Windows/Fonts</dir>
</fontconfig>
```

然后使用 `fc-cache -fv` 刷新一下字体缓存，就可以使用 Windows 中的字体了。

### TexStudio

由于 TeXLive 装在了 WSL 中， 在 Windows 的bash中调用命令为 `wsl pdflatex`.

在 TexStudio 的设置中配置 pdflatex 引擎命令为
```bash
wsl pdflatex %
```
余下相同

### Jabref

这款软件直接在Ubuntu目录中打开对应的库文件是可以的，但是没有办法保存。为此只能采取曲线救国的手段。

新建一个 bash 脚本 `copyThingsToWindows.sh`, 使用 rsync 将 WSL 中的文件传到 Windows，再传回来。

```sh
#!/bin/bash

if [ "$1" == "a" ]; then
    # 执行第一条命令
    rsync -a --delete  /home/name/Github/papers/bibtex  /mnt/c/githubLinux
elif [ "$1" == "b" ]; then
    # 执行第二条命令
    rsync -a  /mnt/c/githubLinux/bibtex/ /home/name/Github/papers/bibtex  
else
    # 参数无效
    echo "无效的参数"
fi
```

使用命令 `chmod +x copyThingsToWindows.sh` 将其变为可执行文件.

在终端中输入 `./copyThingsToWindows.sh a` 将文件同步到 Windows 中，参数为 `b` 则是拉回到 WSL. 

这样就可以在 Jabref 中打开 Windows 的库了。当然，这样做的代价就是不能用查找源文件的功能了。

## 问题

目前发现的问题是，对于较复杂的层级结构，需要大量的时间来建立缓存，在此之前整个 vscode 是被阻塞掉的，也即没办法操作。这个bug最近被修复了

## 参考阅读

1. [在WSL中安装LaTeX - 知乎](https://zhuanlan.zhihu.com/p/202865739)