#!/Library/Frameworks/Python.framework/Versions/3.14/bin/python3
# <swiftbar.hideAbout>true</swiftbar.hideAbout>
import json, math, os, sys
from pathlib import Path
from websockets.sync.client import connect

HOST = "YOUR_K1_IP"  # K1 IP address (printer screen or router)
DIAMETER_MM, DENSITY = 1.75, 1.27  # PETG
SPOOL_G = 1000
LEN_UNIT_MM = 1  # shortcut: usedMaterialLength assumed mm, verify on first real print
DATA = Path.home() / "Library/Application Support/k1-filament/data.json"


def grams(mm):
    return mm * LEN_UNIT_MM * math.pi * (DIAMETER_MM / 2) ** 2 / 1000 * DENSITY


def load():
    return json.loads(DATA.read_text()) if DATA.exists() else {"jobs": {}}


def save(d):
    tmp = DATA.with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    os.replace(tmp, DATA)  # atomic: a crash mid-write must not wipe the history


def poll(d):
    try:
        with connect(f"ws://{HOST}:9999", open_timeout=5) as ws:
            s = json.loads(ws.recv(timeout=5))
    except Exception:
        return False
    key = str(s.get("printStartTime") or s.get("printId") or "")
    used = float(s.get("usedMaterialLength") or 0)
    if key and used > 0:
        j = d["jobs"].setdefault(key, {"name": s.get("printFileName", ""), "mm": 0})
        j["mm"] = max(j["mm"], used)  # value may reset to 0 after the job ends
        save(d)
    return True


if __name__ == "__main__":
    if "--test" in sys.argv:
        assert abs(grams(1000) - 3.055) < 0.01, grams(1000)
        print("ok")
        sys.exit()
    d = load()
    if "reset" in sys.argv:
        d["jobs"] = {}
        save(d)
    online = poll(d)
    left = SPOOL_G - sum(grams(j["mm"]) for j in d["jobs"].values())
    print(f"🧵 {left:.0f}g")
    print("---")
    print("프린터 연결됨" if online else "프린터 연결 안 됨 (마지막 기록 기준)")
    for j in list(d["jobs"].values())[-5:][::-1]:
        print(f"{j['name'] or '(이름 없음)'}  {grams(j['mm']):.1f}g")
    print("---")
    print(f"새 스풀로 리셋 ({SPOOL_G}g) | bash='{os.path.abspath(__file__)}' param1=reset terminal=false refresh=true")
