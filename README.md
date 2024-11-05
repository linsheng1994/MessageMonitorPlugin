# MessageMonitorPlugin

QQ群消息监控转发插件，支持关键词监控和消息转发。

## 功能

- 监控指定QQ群或所有群的消息
- 支持关键词匹配
- 支持正则表达式匹配
- 将匹配的消息转发给指定QQ用户

## 安装
bash
!plugin get https://github.com/你的用户名/MessageMonitorPlugin.git


## 配置

编辑 `config.py`:

1. 设置监控的群号：
python
monitor_groups = ["群号1", "群号2"] # 为空则监控所有群


2. 设置接收转发消息的QQ号：
python
forward_targets = ["QQ号1", "QQ号2"]


3. 设置关键词：

python
rules = {
"keywords": ["关键词1", "关键词2"],
"regexp": [] # 正则表达式规则
}


## 使用

1. 安装插件后重启 QChatGPT
2. 使用 `!plugin list` 确认插件已加载
3. 使用 `!plugin on MessageMonitor` 启用插件
