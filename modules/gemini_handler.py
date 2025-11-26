import time
from collections import deque
from config import Config
import requests


class GeminiHandler:
    def __init__(self):
        self.api_key = Config.GEMINI_API_KEY
        self.api_url = "https://hiapi.online/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {Config.GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }

        # 先初始化 conversation_history，再调用 _initialize_history
        self.conversation_history = deque(maxlen=Config.MAX_HISTORY_LENGTH)
        self.last_reply_time = 0

        # 然后初始化历史记录
        self._initialize_history()

    def _initialize_history(self):
        """初始化对话历史"""
        system_message = {
            'role': 'system',
            'content': Config.SYSTEM_PROMPT
        }
        self.conversation_history.append(system_message)

    def generate_reply(self, user_message, username="观众"):
        """生成回复"""
        # 冷却检查
        current_time = time.time()
        if current_time - self.last_reply_time < Config.REPLY_COOLDOWN:
            return None

        # 添加用户消息到历史
        user_msg = {
            'role': 'user',
            'content': f"{username}说: {user_message}"
        }
        self.conversation_history.append(user_msg)

        try:
            # 构建请求数据
            payload = {
                "model": "gemini-2.5-pro-preview-06-05",  # 根据实际API调整
                "messages": list(self.conversation_history),
                "temperature": 1,
                "max_tokens": 20000
            }

            # 生成回复
            response = requests.post(self.api_url, headers=self.headers, json=payload, timeout=30)

            if response.status_code == 200:
                result = response.json()
                reply_text = result["choices"][0]["message"]["content"].strip()
            else:
                print(f"API请求失败: {response.status_code}, 响应: {response.text}")
                return "抱歉，我现在有点忙，稍后再聊～"

            # 添加助手回复到历史
            assistant_msg = {
                'role': 'assistant',
                'content': reply_text
            }
            self.conversation_history.append(assistant_msg)

            self.last_reply_time = current_time
            print(f"AI回复: {reply_text}")
            return reply_text

        except requests.exceptions.Timeout:
            print("API请求超时")
            return "思考时间有点长，让我再想想..."
        except Exception as e:
            print(f"Gemini API错误: {e}")
            return "嗯...让我想想该怎么回答呢～"

    def add_system_message(self, message):
        """添加系统消息"""
        system_msg = {'role': 'system', 'content': message}
        self.conversation_history.append(system_msg)