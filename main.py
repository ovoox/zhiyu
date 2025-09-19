import aiohttp
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Video

@register("beauty-video-plugin", "美女视频", "一款获取美女视频的娱乐插件", "1.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "http://api.ovoc.cn/api/beautyvideo.php"
    
    async def initialize(self):
        """插件初始化"""
        logger.info("美女视频插件已加载")
    
    @filter.command("美女视频")
    async def beauty_video(self, event: AstrMessageEvent):
        """获取美女视频"""
        try:
            # 调用API获取视频
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url) as response:
                    if response.status == 200:
                        video_url = await response.text()
                        # 返回视频消息
                        yield event.result([Video(url=video_url)])
                    else:
                        yield event.plain_result("获取视频失败，请稍后再试")
        except Exception as e:
            logger.error(f"获取美女视频出错: {e}")
            yield event.plain_result("获取视频时发生错误")

    async def terminate(self):
        """插件销毁"""
        logger.info("美女视频插件已卸载")
