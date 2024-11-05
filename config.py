class Config:
    # 监控的QQ群列表，为空则监控所有群
    monitor_groups = ["84324747"]
    
    # 接收转发消息的QQ号列表
    forward_targets = ["757834215"]
    
    # 监控规则
    rules = {
        # 关键词匹配规则
        "keywords": [
            "苹果"
        ],
        
        # 正则表达式规则（这里可以留空，因为我们只需要关键词匹配）
        "regexp": []
    }
    
    # 是否转发包含图片的消息
    forward_images = True
    
    # 转发消息的格式
    forward_template = """
⚠️监控提醒
群：{group_name}
发送者：{sender_name}
消息内容：
{message}
    """.strip()