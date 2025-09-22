import aiohttp
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.message_components import Comp

@register("beauty-video-plugin", "美女视频", "一款获取美女视频的娱乐插件", "1.0")
class BeautyVideoPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.api_url = "http://api.ovoc.cn/api/beautyvideo.php"
        self.session = aiohttp.ClientSession()
    
    async def initialize(self):
        """插件初始化"""
        logger.info("美女视频插件已加载")
    
    @filter.command("美女视频")
    async def beauty_video(self, event: AstrMessageEvent):
        """获取美女视频"""
        try:
            # 调用API获取视频URL
            async with self.session.get(self.api_url) as resp:
                if resp.status != 200:
                    return event.reply("视频获取失败，请稍后再试")
                
                video_url = (await resp.text()).strip()
                
                # 验证URL格式
                if not (video_url.startswith("http://") or video_url.startswith("https://")):
                    return event.reply("获取的视频链接无效")
                
                # 创建视频消息组件
                video = Comp.Video.fromURL(url=video_url)
                
                # 回复视频消息
                return event.reply(video)
                
        except aiohttp.ClientError as e:
            logger.error(f"网络请求错误: {e}")
            return event.reply("网络请求失败，请检查网络连接")
        except Exception as e:
            logger.error(f"获取视频出错: {e}")
            return event.reply("获取视频时发生错误")
    
    async def terminate(self):
        """插件销毁"""
        await self.session.close()
        logger.info("美女视频插件已卸载")
