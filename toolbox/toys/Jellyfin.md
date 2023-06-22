# Jellyfin 家庭影音系统

[官方网站](https://jellyfin.org/)

## 安装

服务器端使用 choco 安装

```bash
choco install jellyfin
```

小米电视可采用如下步骤

1. 在Windows中新建一个用户账户 `user`，设置密码 `pw`
2. 新建一个文件夹 `share` ，在属性中将其设置为共享
3. 在 [jellyfin/jellyfin-androidtv: Android TV Client for Jellyfin](https://github.com/jellyfin/jellyfin-androidtv) 中下载客户端, 放入 `share`
4. 在小米电视高清播放器中输入本机 ip, 选择 smb 协议，输入账号 `user` 和密码  `pw`
5. 进入  `share` 安装客户端
6. 登录即可

注意到 Jellyfin 默认需要 `8096` 端口，可以在其他设备上访问 `<localIP>:8096`, 测试防火墙是否暴露了该端口。若无法连接，则在防火墙的高级设置中的入站规则和出站规则中添加端口 `8096`.

**参考**
1. [小米电视安装jellyfinTV客户端APP_哔哩哔哩_bilibili](https://www.bilibili.com/video/BV1fG4y1s7UT/?spm_id_from=333.788&vd_source=4d55e615e34201407bdaaa9275aa62bc)
2. [Windows 10/ 11 下安全并正确地使用 SMB 共享_软件应用_什么值得买](https://post.smzdm.com/p/akxwkxqk/)
3. [解决window系统电脑某个端口下的程序无法被局域网内的电脑访问的问题。_局域网无法访问某端口_cjy_is_me的博客-CSDN博客](https://blog.csdn.net/cuijiying/article/details/104993550)

## 管理

可以用 [tinyMediaManager](https://www.tinymediamanager.org/) 来管理电影源文件，以及刮削各类元数据

### 字幕

可以用 [首页 - 射手网(伪) - assrt.net - 字幕下载，字幕组，中文字幕，美剧字幕，英剧字幕，双语字幕，新番字幕](https://assrt.net/) 来下载中文字幕。

查看 Jellyfin 的[支持的字幕](https://jellyfin.org/docs/general/clients/codec-support#wikipedias-subtitle-codec-tables) 以及 [字幕设置](https://jellyfin.org/docs/general/server/media/external-files/)

格式为 `film.中文.default.srt`.

