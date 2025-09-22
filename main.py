import os
import aiohttp
from astrbot.api.all import *

PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_spacequery')
SPACE_API_URL = "http://api.ovoc.cn/api/ckj.php?qq="
INFO_API_URL = "http://api.ovoc.cn/api/cxx.php?qq="
MUSIC_API_URL = "http://api.ovoc.cn/api/"

@register("space_query", "知鱼", "查询QQ空间、信息和音乐的插件", "1.0.0")
class SpaceQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
    
    async def _query_api(self, api_url: str, qq: str = ""):
        """通用API查询方法"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(api_url + qq) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        return f"查询失败，状态码：{response.status}"
        except Exception as e:
            self.context.logger.error(f"API查询失败: {str(e)}")
            return "查询时发生错误"
    
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """群聊消息处理器"""
        msg = event.message_str.strip()
        
        # 查空间指令
        if msg.startswith("查空间"):
            parts = msg.split()
            if len(parts) >= 2 and parts[1].isdigit():
                qq_number = parts[1]
                space_info = await self._query_api(SPACE_API_URL, qq_number)
                yield event.chain_result([Plain(text=space_info)])
            else:
                yield event.chain_result([Plain(text="请输入正确的QQ号，例如：查空间 123456")])
        
        # 查信息指令
        elif msg.startswith("查信息"):
            parts = msg.split()
            if len(parts) >= 2 and parts[1].isdigit():
                qq_number = parts[1]
                info_result = await self._query_api(INFO_API_URL, qq_number)
                yield event.chain_result([Plain(text=info_result)])
            else:
                yield event.chain_result([Plain(text="请输入正确的QQ号，例如：查信息 123456")])
        
        # 查音乐指令
        elif msg.startswith("查音乐"):
            parts = msg.split()
            if len(parts) >= 2:
                music_name = parts[1]
                # 这里需要确认音乐接口的具体格式，暂时使用通用格式
                music_result = await self._query_api(MUSIC_API_URL, music_name)
                yield event.chain_result([Plain(text=music_result)])
            else:
                yield event.chain_result([Plain(text="请输入音乐名称，例如：查音乐 周杰伦")])
