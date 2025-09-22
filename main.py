import os
import aiohttp
import time
from astrbot.api.all import *

PLUGIN_DIR = os.path.join('data', 'plugins', 'astrbot_plugin_spacequery')
SPACE_API_URL = "http://api.ovoc.cn/api/ckj.php?qq="
INFO_API_URL = "http://api.ovoc.cn/api/cxx.php?qq="
MUSIC_API_URL = "http://api.ovoc.cn/api/cyy.php?qq="
COOLDOWN_TIME = 5  # 冷却时间5秒

@register("space_query", "知鱼", "查询QQ空间、信息和音乐的插件", "1.0.0")
class SpaceQueryPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.last_query_time = 0  # 记录上次查询时间
    
    async def _query_api(self, api_url: str, qq: str = ""):
        """通用API查询方法"""
        try:
            current_time = time.time()
            if current_time - self.last_query_time < COOLDOWN_TIME:
                remaining = COOLDOWN_TIME - (current_time - self.last_query_time)
                return f"查询过于频繁，请等待 {remaining:.1f} 秒后再试"
            
            self.last_query_time = current_time
            
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
        
        # 查询菜单指令
        if msg == "查询菜单":
            menu = """可用查询指令：
查空间 [QQ号] - 查询QQ空间信息
查信息 [QQ号] - 查询QQ基本信息
查音乐 [QQ号] - 查询QQ音乐信息
注意：每次查询后有5秒冷却时间"""
            yield event.chain_result([Plain(text=menu)])
            return
        
        # 查空间指令
        elif msg.startswith("查空间"):
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
            if len(parts) >= 2 and parts[1].isdigit():
                qq_number = parts[1]
                music_result = await self._query_api(MUSIC_API_URL, qq_number)
                yield event.chain_result([Plain(text=music_result)])
            else:
                yield event.chain_result([Plain(text="请输入正确的QQ号，例如：查音乐 123456")])
