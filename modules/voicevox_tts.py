import requests
import json
import pygame
import tempfile
import os
import threading
from config import Config


class VoicevoxTTS:
    def __init__(self):
        pygame.mixer.init()
        self.is_playing = False

    def text_to_speech(self, text, speaker_id=None):
        """文本转语音"""
        if speaker_id is None:
            speaker_id = Config.VOICEVOX_SPEAKER_ID

        try:
            # 步骤1: 生成音频查询
            query_params = {
                'text': text,
                'speaker': speaker_id
            }

            query_response = requests.post(
                f"{Config.VOICEVOX_URL}/audio_query",
                params=query_params
            )
            query_data = query_response.json()

            # 步骤2: 合成语音
            synthesis_params = {
                'speaker': speaker_id
            }

            synthesis_response = requests.post(
                f"{Config.VOICEVOX_URL}/synthesis",
                params=synthesis_params,
                data=json.dumps(query_data),
                headers={'Content-Type': 'application/json'}
            )

            # 保存临时音频文件
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
                f.write(synthesis_response.content)
                temp_file = f.name

            # 在新线程中播放音频
            thread = threading.Thread(target=self._play_audio, args=(temp_file,))
            thread.daemon = True
            thread.start()

            return temp_file

        except Exception as e:
            print(f"VOICEVOX TTS错误: {e}")
            return None

    def _play_audio(self, audio_file):
        """播放音频文件"""
        self.is_playing = True
        try:
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()

            # 等待播放完成
            while pygame.mixer.music.get_busy():
                pygame.time.wait(100)

        finally:
            self.is_playing = False
            # 清理临时文件
            try:
                os.unlink(audio_file)
            except:
                pass