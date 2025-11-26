import websocket
import json
import threading
import time


class VTubeStudioController:
    def __init__(self):
        self.ws = None
        self.connected = False
        self.token = None

    def connect(self):
        """连接到VTube Studio"""
        try:
            self.ws = websocket.WebSocketApp("ws://127.0.0.1:8001",
                                             on_message=self.on_message,
                                             on_error=self.on_error,
                                             on_close=self.on_close)
            self.ws.on_open = self.on_open

            # 在新线程中运行WebSocket
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()

            # 等待连接建立
            time.sleep(2)
            return self.connected

        except Exception as e:
            print(f"VTube Studio连接失败: {e}")
            return False

    def on_open(self, ws):
        """WebSocket连接打开"""
        print("连接到VTube Studio")
        self.authenticate()

    def on_message(self, ws, message):
        """处理来自VTube Studio的消息"""
        data = json.loads(message)
        print(f"VTS消息: {data}")

        if data.get('messageType') == 'APIError':
            print(f"VTS API错误: {data}")

    def on_error(self, ws, error):
        print(f"VTS WebSocket错误: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("VTube Studio连接关闭")
        self.connected = False

    def authenticate(self):
        """认证到VTube Studio API"""
        auth_request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": "AuthRequest1",
            "messageType": "AuthenticationTokenRequest",
            "data": {
                "pluginName": "AI VTuber",
                "pluginDeveloper": "YourName"
            }
        }

        self.ws.send(json.dumps(auth_request))

    def trigger_hotkey(self, hotkey_id):
        """触发热键（用于表情和动作）"""
        if not self.connected:
            return

        request = {
            "apiName": "VTubeStudioPublicAPI",
            "apiVersion": "1.0",
            "requestID": f"Hotkey_{hotkey_id}",
            "messageType": "HotkeyTriggerRequest",
            "data": {
                "hotkeyID": hotkey_id
            }
        }

        self.ws.send(json.dumps(request))

    def trigger_expression(self, expression_file):
        """触发表情（通过模拟热键）"""
        # 这里需要先在VTube Studio中设置好表情热键
        # 根据expression_file名称映射到对应的热键ID
        expression_map = {
            "happy": "expression_happy_id",
            "sad": "expression_sad_id",
            "angry": "expression_angry_id"
        }

        hotkey_id = expression_map.get(expression_file)
        if hotkey_id:
            self.trigger_hotkey(hotkey_id)