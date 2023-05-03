# nonebot-adapter-minecraft

NoneBot2 与 MineCraft Server互通的适配器

## 使用

前往还未装修的 [Wiki](https://github.com/17TheWord/nonebot-adapter-spigot/wiki)

## 服务端支持

- 原版（读取日志并正则匹配）
- Spigot（插件）
- Forge（读取日志并正则匹配、Mod）
- Fabric（读取日志并正则匹配）

## Rcon支持

对于非插件端采用 `WebSocket` + `Rcon` 方式与服务端通信，需要在服务端开启 `Rcon` 功能

## 其他

- [17TheWord/nonebot-plugin-mcqq](https://github.com/17TheWord/nonebot-plugin-mcqq) 使用插件与MineCraft Server通信，较为完善
- [17TheWord/nonebot-plugin-mcping](https://github.com/17TheWord/nonebot-plugin-mcqq) 获取 MineCraft Server Motd 信息并返回图片

# 特别感谢

- [@yanyongyu](https://github.com/yanyongyu) ：首先感谢万能的DDL。
- [@SK-415](https://github.com/SK-415) ：感谢SK佬给予许多优秀的建议和耐心的解答。
- [@zhz-红石头](https://github.com/zhzhongshi) ：感谢红石头在代码上的帮助
- [NoneBot2](https://github.com/nonebot/nonebot2) ：插件使用的开发框架。
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp) ：稳定完善的 CQHTTP 实现。

## 贡献与支持

觉得好用可以给这个项目点个 `Star` 或者去 [爱发电](https://afdian.net/a/17TheWord) 投喂我。

有意见或者建议也欢迎提交 [Issues](https://github.com/17TheWord/nonebot-adapter-minecraft/issues)
和 [Pull requests](https://github.com/17TheWord/nonebot-adapter-minecraft/pulls) 。

## 许可证

本项目使用 [GNU AGPLv3](https://choosealicense.com/licenses/agpl-3.0/) 作为开源许可证。
