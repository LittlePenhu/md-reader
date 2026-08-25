# -*- coding: utf-8 -*-
"""MD 阅读器 —— pywebview 桌面应用入口。

用法:
    python app.py                # 打开窗口（自动恢复上次文件与阅读进度）
    python app.py 某文件.md      # 直接打开指定文件

依赖:
    pip install pywebview
"""
import base64
import json
import os
import sys
import time

import webview

APP_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_INDEX = os.path.join(APP_DIR, "web", "index.html")
STATE_DIR = os.path.join(os.environ.get("LOCALAPPDATA", APP_DIR), "MDReader")
STATE_FILE = os.path.join(STATE_DIR, "state.json")

MAX_MD_SIZE = 10 * 1024 * 1024    # 超过 10MB 的 md 拒绝渲染，避免界面卡死
MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 单张图片 base64 上限
MAX_PROGRESS = 200                 # 阅读进度最多记住的文件数（超出丢最旧的）

IMAGE_MIME = {
    ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg",
    ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp",
    ".svg": "image/svg+xml", ".ico": "image/x-icon", ".avif": "image/avif",
}


class Api:
    """通过 window.pywebview.api 暴露给前端的方法。"""

    def __init__(self, initial_file=None):
        self.initial_file = initial_file
        self.state = self._load_state()

    # ---------- 状态 ----------

    @staticmethod
    def _recent_path(item):
        """recent 条目归一化：新格式 {path, ts}，旧格式纯路径字符串。"""
        if isinstance(item, str):
            return {"path": item, "ts": None}
        if isinstance(item, dict) and isinstance(item.get("path"), str):
            ts = item.get("ts")
            return {"path": item["path"], "ts": ts if isinstance(ts, (int, float)) else None}
        return None

    def _load_state(self):
        try:
            with open(STATE_FILE, encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, dict):
                raise ValueError("state 损坏")
        except Exception:
            data = {}
        recent, seen = [], set()
        for item in data.get("recent", []):
            entry = self._recent_path(item)
            if entry and os.path.exists(entry["path"]) and entry["path"] not in seen:
                seen.add(entry["path"])
                recent.append(entry)
        last = data.get("last_file")
        if not (isinstance(last, str) and os.path.exists(last)):
            last = None
        progress = data.get("progress")
        if not isinstance(progress, dict):
            progress = {}
        return {"last_file": last, "recent": recent, "progress": progress}

    def _save_state(self):
        try:
            os.makedirs(STATE_DIR, exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.state, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print("保存状态失败:", e)

    def get_state(self):
        state = dict(self.state)
        if self.initial_file:
            state["initial_file"] = self.initial_file
            self.initial_file = None
        return state

    def register_open(self, path):
        if not path:
            return
        recent = [
            r for r in self.state.get("recent", [])
            if (r if isinstance(r, str) else r.get("path")) != path
        ]
        recent.insert(0, {"path": path, "ts": time.time()})
        self.state["recent"] = recent[:10]
        self.state["last_file"] = path
        self._save_state()

    def remove_recent(self, path):
        """从最近列表移除（文件已不存在时由前端调用）。"""
        self.state["recent"] = [
            r for r in self.state.get("recent", [])
            if (r if isinstance(r, str) else r.get("path")) != path
        ]
        self.state["progress"].pop(path, None)
        self._save_state()
        return self.state

    def save_progress(self, path, ratio):
        """记录阅读进度（0~1 的滚动比例）。"""
        if not path or not isinstance(ratio, (int, float)):
            return
        progress = self.state.setdefault("progress", {})
        if progress.get(path) == round(float(ratio), 4):
            return
        progress[path] = round(float(ratio), 4)
        while len(progress) > MAX_PROGRESS:
            progress.pop(next(iter(progress)))
        self._save_state()

    def clear_state(self):
        self.state = {"last_file": None, "recent": [], "progress": {}}
        self._save_state()
        return self.state

    # ---------- 文件 ----------

    def open_file(self):
        """弹出系统文件对话框，返回 read_file 结果或 None。"""
        try:
            result = webview.windows[0].create_file_dialog(
                webview.OPEN_DIALOG,
                file_types=("Markdown 文件 (*.md;*.markdown;*.mdown)", "文本文件 (*.txt)", "所有文件 (*.*)"),
            )
        except Exception as e:
            return {"error": "无法打开文件对话框: %s" % e}
        if not result:
            return None
        return self.read_file(result[0])

    def read_file(self, path):
        """读取文件，自动探测编码。返回 {path, name, content, mtime} 或 {error}。"""
        try:
            if os.path.getsize(path) > MAX_MD_SIZE:
                return {"error": "文件太大（%.1f MB），超过 %d MB 上限" % (
                    os.path.getsize(path) / 1048576, MAX_MD_SIZE // 1048576)}
            with open(path, "rb") as f:
                raw = f.read()
        except Exception as e:
            return {"error": "读取失败: %s" % e}

        if raw[:2] in (b"\xff\xfe", b"\xfe\xff"):
            # UTF-16 BOM：gb18030 几乎不会解码失败，必须先拦下，否则"成功"出乱码
            content = raw.decode("utf-16", errors="replace")
        else:
            for enc in ("utf-8-sig", "utf-8", "gb18030"):
                try:
                    content = raw.decode(enc)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                content = raw.decode("utf-8", errors="replace")

        try:
            mtime = os.path.getmtime(path)
        except OSError:
            mtime = None
        return {
            "path": path,
            "name": os.path.basename(path),
            "content": content,
            "mtime": mtime,
        }

    def stat_file(self, path):
        """供前端检测文件是否被外部修改。"""
        try:
            return {"mtime": os.path.getmtime(path)}
        except OSError:
            return {"error": "文件不存在"}

    def read_image(self, path):
        """读取本地图片返回 data URL，作为 file:// 直载失败时的兜底。"""
        try:
            path = os.path.normpath(path)
            ext = os.path.splitext(path)[1].lower()
            mime = IMAGE_MIME.get(ext, "application/octet-stream")
            with open(path, "rb") as f:
                raw = f.read(MAX_IMAGE_SIZE + 1)
            if len(raw) > MAX_IMAGE_SIZE:
                return {"error": "图片过大（超过 20 MB）"}
            return {"data": "data:%s;base64,%s" % (mime, base64.b64encode(raw).decode("ascii"))}
        except Exception as e:
            return {"error": "图片读取失败: %s" % e}


def main():
    initial = sys.argv[1] if len(sys.argv) > 1 else None
    api = Api(initial_file=initial)
    webview.create_window(
        "MD 阅读器",
        WEB_INDEX,
        js_api=api,
        width=1200,
        height=820,
        min_size=(880, 600),
        text_select=True,
    )
    # private_mode=False + 持久 storage_path：否则 WebView2 隐私模式下
    # localStorage 重启即清空，外观设置（风格/深浅色/字号/页宽）无法记忆
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
    except OSError:
        pass
    webview.start(
        private_mode=False,
        storage_path=os.path.join(STATE_DIR, "webview"),
    )


if __name__ == "__main__":
    main()
