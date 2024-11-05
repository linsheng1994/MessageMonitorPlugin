from pkg.plugin.context import register, handler, BasePlugin, APIHost, EventContext
from pkg.plugin.events import *
import re

@register(
    name="MessageMonitor",
    description="监控QQ群消息并转发给指定用户",
    version="0.1",
    author="Assistant"
)
class MessageMonitorPlugin(BasePlugin):
    """QQ群消息监控插件"""
    
    def __init__(self, host: APIHost):
        super().__init__(host)
        from . import config
        self.cfg = config.Config()
        self.host.ap.logger.info(f"消息监控插件已加载, 监控群: {self.cfg.monitor_groups}")

    async def initialize(self):
        """异步初始化"""
        self.host.ap.logger.info("消息监控插件初始化完成")

    def check_keywords(self, text: str) -> bool:
        """检查文本是否包含关键词"""
        for kw in self.cfg.rules["keywords"]:
            if kw in text:
                self.host.ap.logger.debug(f"检测到关键词: {kw}")
                return True
        return False

    def check_regexp(self, text: str) -> bool:
        """检查文本是否匹配正则表达式"""
        return any(re.search(pattern, text) for pattern in self.cfg.rules["regexp"])

    def should_monitor_group(self, group_id: str) -> bool:
        """检查是否需要监控该群"""
        should_monitor = not self.cfg.monitor_groups or str(group_id) in self.cfg.monitor_groups
        self.host.ap.logger.debug(f"群 {group_id} {'在' if should_monitor else '不在'}监控列表中")
        return should_monitor

    @handler(GroupMessageReceived)
    @handler(GroupNormalMessageReceived)
    @handler(PersonMessageReceived)
    async def handle_message(self, ctx: EventContext):
        """处理消息"""
        try:
            # 判断是否是群消息
            if not hasattr(ctx.event, 'group_id'):
                return

            self.host.ap.logger.debug(f"收到消息: {ctx.event.text_message}")
            
            # 获取消息内容
            text_message = ctx.event.text_message
            group_id = str(ctx.event.group_id)
            sender_id = str(ctx.event.sender_id)
            
            # 检查是否需要监控此群
            if not self.should_monitor_group(group_id):
                return
                
            # 检查是否符合监控规则
            if not (self.check_keywords(text_message) or self.check_regexp(text_message)):
                return
                
            self.host.ap.logger.info(f"检测到关键词消息: {text_message}")
            
            # 构造转发消息
            forward_message = self.cfg.forward_template.format(
                group_name=f'群{group_id}',
                group_id=group_id,
                sender_name=f'用户{sender_id}',
                sender_id=sender_id,
                message=text_message
            )
            
            # 转发消息给目标用户
            for target_id in self.cfg.forward_targets:
                try:
                    await ctx.send_message(
                        target_type="person",
                        target_id=target_id,
                        message_chain=[forward_message]
                    )
                    self.host.ap.logger.info(f"已转发消息给 {target_id}")
                except Exception as e:
                    self.host.ap.logger.error(f"转发消息给 {target_id} 失败: {e}")
                    
        except Exception as e:
            self.host.ap.logger.error(f"处理消息时发生错误: {e}")
            import traceback
            self.host.ap.logger.error(traceback.format_exc())