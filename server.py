"""
轻量 HTTP 服务，将 realnamebaseinfo.py 的各功能暴露为 REST API
启动方式：python realname/server.py
访问地址：http://localhost:8888/realname_ui.html
"""

import sys
import os
import json
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler

# 确保能 import 同级模块
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from realnamebaseinfo import realname

# 全局单例，避免每次请求都重新登录
_client = None

def get_client():
    global _client
    if _client is None:
        print("初始化 realname 客户端并登录…")
        _client = realname()
    return _client


def handle_api(path: str, body: dict) -> dict:
    """根据路径分发到对应方法"""
    client = get_client()
    action = path.lstrip("/api/")

    if action == "getUserInfoByID":
        result = client.getUserInfoByID(body["user_id"])
        return {"success": True, "data": result}

    elif action == "getRealTelByHash":
        result = client.getRealTelByHash(body["user_id"])
        return {"success": True, "data": result}

    elif action == "GetRealNameinfo":
        result = client.GetRealNameinfo(body["user_id"])
        return {"success": True, "data": result}

    elif action == "GetRealidCardNumber":
        result = client.GetRealidCardNumber(body["idCardNumber"])
        return {"success": True, "data": result}

    elif action == "updateRealNameinfo":
        result = client.updateRealNameinfo(body["user_id"])
        return {"success": True, "data": result}

    elif action == "updateFaceInfo":
        result = client.updateFaceInfo(body["user_id"])
        return {"success": True, "data": result}

    elif action == "updateEnterpriseInfo":
        result = client.updateEnterpriseInfo(body["user_id"])
        return {"success": True, "data": result}

    elif action == "updateTwoElementRealNameinfo":
        result = client.updateTwoElementRealNameinfo(body["user_id"])
        return {"success": True, "data": result}

    else:
        return {"success": False, "error": f"未知接口：{action}"}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(f"[{self.address_string()}] {fmt % args}")

    def _send_json(self, code: int, data: dict):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, filepath: str, mime: str):
        with open(filepath, "rb") as f:
            body = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        base_dir = os.path.dirname(__file__)
        if self.path in ("/", "/realname_ui.html"):
            self._send_file(os.path.join(base_dir, "realname_ui.html"), "text/html; charset=utf-8")
        else:
            self._send_json(404, {"error": "Not Found"})

    def do_POST(self):
        if not self.path.startswith("/api/"):
            self._send_json(404, {"error": "Not Found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length)
        try:
            body = json.loads(raw) if raw else {}
        except Exception:
            self._send_json(400, {"success": False, "error": "请求体不是合法 JSON"})
            return

        try:
            result = handle_api(self.path, body)
            self._send_json(200, result)
        except Exception as e:
            tb = traceback.format_exc()
            print(tb)
            self._send_json(500, {"success": False, "error": str(e), "traceback": tb})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8888))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"✅ 服务已启动：http://localhost:{port}/realname_ui.html")
    print("   按 Ctrl+C 停止服务")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n服务已停止")
