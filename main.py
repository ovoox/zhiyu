import os
import aiohttp
from astrbot.api.all import *

PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_spacequery')
SPACE_API_URL = "http://api.ovoc.cn/api/ckj.php?qq="

@register("space_query", "知鱼", "查询QQ空间信息的插件", "1.0.0")
class SpaceQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    async def _query_space_info(self, qq: str):
        """查询QQ空间信息"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(SPACE_API_URL + qq) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return f"查询失败，状态码：{response.status}"
        except Exception as e:
            self.context.logger.error(f"查询QQ空间信息失败: {str(e)}")
            return "查询QQ空间信息时发生错误"
    
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """群聊消息处理器"""
        msg = event.message_str.strip()
        msg_id = str(event.message_obj.message_id)
        
        if msg.startswith("查空间"):
            parts = msg.split()
            if len(parts) >= 2 and parts[1].isdigit():
                qq_number = parts[1]
                space_info = await self._query_space_info(qq_number)
                chain = [
                    Reply(id=msg_id),
                    Plain(text=space_info)
                ]
                yield event.chain_result(chain)
            else:
                chain = [
                    Reply(id=msg_id),
                    Plain(text="请输入正确的QQ号，例如：查空间 123456")
                ]
                yield event.chain_result(chain)
