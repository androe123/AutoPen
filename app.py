from pathlib import Path
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


def get_app_data_dir():
    appdata = os.environ.get("APPDATA") or os.path.expanduser("~")
    cfg_dir = os.path.join(appdata, "АвтоРучка")
    os.makedirs(cfg_dir, exist_ok=True)
    return cfg_dir


class DesktopApi:
    def load_settings(self):
        path = os.path.join(get_app_data_dir(), "settings.json")
        if not os.path.exists(path):
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def save_settings(self, payload):
        path = os.path.join(get_app_data_dir(), "settings.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def load_photos(self):
        path = os.path.join(get_app_data_dir(), "photos.json")
        if not os.path.exists(path):
            return []
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []

    def save_photos(self, photos_list):
        path = os.path.join(get_app_data_dir(), "photos.json")
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(photos_list, f, ensure_ascii=False)
            return True
        except Exception:
            return False


ONE_DAY_SEC = 24 * 60 * 60


def watch_updates(window):
    while True:
        time.sleep(ONE_DAY_SEC)
        try:
            window.evaluate_js("if (typeof checkForCodeUpdates === 'function') checkForCodeUpdates(false)")
        except Exception:
            pass


if __name__ == "__main__":
    html_path = Path(get_base_dir()) / "index.html"
    api = DesktopApi()
    window = webview.create_window(
        "АвтоРучка",
        url=html_path.as_uri(),
        width=1280,
        height=820,
        min_size=(900, 600),
        js_api=api,
        background_color="#0c0e1a",
    )
    t = threading.Thread(target=watch_updates, args=(window,), daemon=True)
    t.start()
    webview.start(debug=False)
