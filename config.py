import os


class Config:
    # Gemini配置
    GEMINI_API_KEY = "sk-TDVtL3zUsxjwAVRZlio68iqJNs32ygaAewxmG0f8bnBATgOF"

    # B站配置
    BILIBILI_ROOM_ID = "你的直播间ID"  # 在直播间URL中找到

    # VOICEVOX配置
    VOICEVOX_URL = "http://127.0.0.1:50021"
    VOICEVOX_SPEAKER_ID = 1  # 声源ID，在VOICEVOX中查看

    # VTube Studio配置
    VTS_WS_URL = "ws://127.0.0.1:8001"

    # 对话配置
    SYSTEM_PROMPT = """
    你是一个可爱的虚拟主播，名字叫「小灵」。性格活泼开朗，喜欢和观众互动。
    说话风格：使用可爱的语气词，比如「呢～」、「呀」、「哦！」。偶尔会卖萌。
    重要规则：
    1. 回复要简短，适合语音播放
    2. 每次只回复一条弹幕的内容
    3. 避免复杂的长句
    4. 保持积极正面的态度
    """

    # 性能配置
    MAX_HISTORY_LENGTH = 100  # 对话历史长度
    REPLY_COOLDOWN = 3  # 回复冷却时间(秒)