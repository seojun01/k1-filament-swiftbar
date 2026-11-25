# k1-filament-swiftbar

Creality K1의 필라멘트 잔량을 맥 메뉴바(`🧵 703g`)에 표시하는 SwiftBar 플러그인.

- K1 웹 UI 웹소켓(`ws://<K1 IP>:9999`)에서 `usedMaterialLength`(mm)를 30초마다 읽어 출력별 사용량을 누적하고, 1000g에서 뺀 값을 보여줍니다.
- 기본값은 PETG 1.75mm (밀도 1.27 g/cm³). 다른 소재는 `DENSITY`를 바꾸세요.
- 메뉴의 "새 스풀로 리셋"을 누르면 기록이 지워지고 1000g로 돌아갑니다.

## 설치
1. `brew install swiftbar` 후 `pip install websockets`
2. `k1_filament.30s.py`의 `HOST`를 K1 IP로 바꾸고, 첫 줄 shebang을 `websockets`가 설치된 실제 파이썬 경로로 맞춥니다 (SwiftBar는 pyenv shim을 못 씁니다).
3. SwiftBar 플러그인 폴더에 복사 후 `chmod +x`.

기록은 `~/Library/Application Support/k1-filament/data.json`에 저장됩니다.

## 한계
- 맥이 잠든 동안 출력하면 그 구간은 기록되지 않습니다.
- 출력 도중 중단/재시작된 작업은 마지막으로 읽은 값까지만 반영됩니다.
- 자체 점검: `python3 k1_filament.30s.py --test`
