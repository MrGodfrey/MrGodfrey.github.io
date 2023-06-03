# ctex 套件

国内的很多期刊 需要用ctex套件才能编译， 涉及到的问题包括
1. 模板文件打开乱码
2. 缺失 `sty` 文件

[CTEX](https://ctex.org/about/) 是一款古老的套件， 已经中断开发了将近十年， 最近又在开发了。
一般从师兄师姐， 或者从国内期刊上下载的 tex 模板， 打开中文是乱码的话， 就是用的 ctex 套件。

## 安装

从 [下载中心 – CTEX](https://ctex.org/ctex/download/) 下载所谓的**过时版本**。

!> 注意要下载 Full 的版本， 这个版本可以将所有的宏包文件都安装上。

直接运行安装程序，默认安装即可。

!> 最好只安装到 `C` 盘。

## 测试

安装完成后需要重启电脑。

打开 WinEdt 软件， 打开之前是乱码的文件， 看能否编译。

一般编译的方法是 texify， 或者 pdfLatex 等， 只要能编译出 pdf 文件即可。

## 配置 TeXStudio

因为 ctex 套件会覆盖系统的 PATH 变量， 导致 TeXStudio 默认的编译引擎会指向 ctex 套件的位置。 
此时需要手动指定 TeXStudio 的编译引擎。

1. 在 TeXStudio 的 `设置-> 命令-> LaTeX` 中选择右边第一个按钮， 选择程序。
2. 在弹出的选中程序对话框中进入如下路径 `C:\texlive\2021\bin\win32`， 点击对话框底部的打开
3. 对 PdfLatex， XeLatex， 和 Lualatex 都如此设置即可

配置之后， 在 WinEdt 中编译老旧的文件， 在TeXStudio中正常编译新的文件即可。