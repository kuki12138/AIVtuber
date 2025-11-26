import time
import queue
import threading
from config import Config
from modules.bilibili_client import BilibiliDanmakuClient
from modules.gemini_handler import GeminiHandler
from modules.voicevox_tts import VoicevoxTTS
from modules.vtube_studio import VTubeStudioController


class AIVTuberSystem:
    def __init__(self):
        self.message_queue = queue.Queue()
        self.running = False

        # 初始化各个模块
        self.bilibili_client = BilibiliDanmakuClient(
            Config.BILIBILI_ROOM_ID,
            self.message_queue
        )
        self.gemini_handler = GeminiHandler()
        self.tts_engine = VoicevoxTTS()
        self.vts_controller = VTubeStudioController()

    def start(self):
        """启动AI VTuber系统"""
        print("启动AI VTuber系统...")
        self.running = True

        # 连接VTube Studio
        print("连接VTube Studio...")
        if not self.vts_controller.connect():
            print("警告: VTube Studio连接失败，将继续无模型运行")

        # 启动B站弹幕监听
        print("启动B站弹幕监听...")
        self.bilibili_client.start()

        # 启动消息处理循环
        self._message_loop()

    def _message_loop(self):
        """主消息处理循环"""
        while self.running:
            try:
                # 从队列获取消息（非阻塞）
                try:
                    message = self.message_queue.get(timeout=1)
                except queue.Empty:
                    continue

                # 处理弹幕消息
                if message['type'] == 'danmaku':
                    self._process_danmaku(message)

            except Exception as e:
                print(f"消息处理错误: {e}")
                time.sleep(1)

    def _process_danmaku(self, message):
        """处理弹幕消息"""
        user = message['user']
        text = message['text']

        # 生成AI回复
        reply_text = self.gemini_handler.generate_reply(text, user)

        if reply_text:
            # 触发开心表情
            self.vts_controller.trigger_expression("happy")

            # 语音合成和播放
            self.tts_engine.text_to_speech(reply_text)

            # 根据回复内容触发不同动作
            self._trigger_actions_based_on_reply(reply_text)

    def _trigger_actions_based_on_reply(self, reply_text):
        """根据回复内容触发动作"""
        # 简单的关键词匹配
        happy_keywords = ['开心', '高兴', '喜欢', '哈哈', '嘿嘿']
        sad_keywords = ['难过', '伤心', '抱歉', '对不起']

        if any(keyword in reply_text for keyword in happy_keywords):
            self.vts_controller.trigger_hotkey("action_wave")  # 挥手

        elif any(keyword in reply_text for keyword in sad_keywords):
            self.vts_controller.trigger_hotkey("action_sad")  # 悲伤动作

    def stop(self):
        """停止系统"""
        self.running = False
        print("AI VTuber系统已停止")


if __name__ == "__main__":
    vtuber_system = AIVTuberSystem()

    try:
        vtuber_system.start()
    except KeyboardInterrupt:
        print("\n收到停止信号...")
        vtuber_system.stop()