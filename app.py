import json
import os
import sys
import threading
import time
import webview


def get_base_dir():
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def get_settings_path():
    appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    cfg_dir = os.path.join(appdata, "АвтоРучка")
    os.makedirs(cfg_dir, exist_ok=True)
    return os.path.join(cfg_dir, "settings.json")


class DesktopApi:
    def load_settings(self):
        path = get_settings_path()
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def save_settings(self, payload):
        path = get_settings_path()
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False


def watch_html(window, html_path):
    last_mtime = os.path.getmtime(html_path)
    while True:
        time.sleep(1.5)
        try:
            mtime = os.path.getmtime(html_path)
            if mtime != last_mtime:
                last_mtime = mtime
                window.evaluate_js("checkForCodeUpdates()")
        except OSError:
            pass


if __name__ == "__main__":
    html_path = os.path.join(get_base_dir(), "index.html")
    api = DesktopApi()
    window = webview.create_window(
        "АвтоРучка",
        url=f"file:///{html_path.replace(os.sep, '/')}",
        width=1280,
        height=820,
        min_size=(900, 600),
        js_api=api,
    )
    t = threading.Thread(target=watch_html, args=(window, html_path), daemon=True)
    t.start()
    webview.start()