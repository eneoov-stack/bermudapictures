#!/usr/bin/env python3
"""작업 카드용 장면 고르기 (2026-10-04). 크레딧 0.
1) sheets: 영상마다 장면 12장을 고르게 뽑아 번호 붙인 확인 시트를 만든다 (사람·클로드가 보고 고른다).
2) pick:   고른 번호의 장면을 1280px webp로 site/assets/works/<id>.webp 에 쓴다.
영상은 yt-dlp로 받은 720p 화면 파일(소리 없음)이고 스크래치에 둔다. 다 쓰면 휴지통으로 보낸다.
usage: [FRAMES=24] python pick_frames.py sheets <영상폴더>
       python pick_frames.py pick <영상폴더> <id>=<번호|@초> [...]
"""
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[2] / "assets" / "works"   # 저장소 뿌리/assets/works
import os
N = int(os.environ.get("FRAMES", 12))   # 확인 시트 장면 수. 촘촘히 볼 때 FRAMES=24
FONT = ImageFont.truetype(r"C:\Windows\Fonts\malgunbd.ttf", 28)


def duration(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True)
    return float(r.stdout.strip())


def times(f):
    d = duration(f)
    return [d * (0.06 + 0.88 * k / (N - 1)) for k in range(N)]   # 앞뒤 6%는 뺀다(로고·타이틀 자리)


def grab(f, t, w):
    r = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", str(f), "-frames:v", "1", "-vf", f"scale={w}:-2",
                        "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True)
    from io import BytesIO
    return Image.open(BytesIO(r.stdout)).convert("RGB")


def sheets(folder):
    vids = sorted(folder.glob("*.mp4"))
    out = folder / "sheets"; out.mkdir(exist_ok=True)
    for v in vids:
        tiles = [grab(v, t, 320) for t in times(v)]
        rows = (N + 3) // 4
        sheet = Image.new("RGB", (4 * 320, rows * 180 + 40), (20, 20, 20))
        d = ImageDraw.Draw(sheet)
        d.text((8, 4), v.stem, font=FONT, fill=(255, 182, 0))
        ts = times(v)
        for k, im in enumerate(tiles):
            x, y = (k % 4) * 320, 40 + (k // 4) * 180
            sheet.paste(im.resize((320, 180)), (x, y))
            d.rectangle((x, y, x + 120, y + 30), fill=(0, 0, 0))
            d.text((x + 4, y), f"{k} {ts[k]:.0f}s", font=FONT, fill=(255, 255, 255))   # 번호와 초 — pick에 @초로 넘길 수 있다
        sheet.save(out / f"{v.stem}.jpg", quality=80)
        print("sheet", v.stem)


def pick(folder, picks):
    OUT.mkdir(parents=True, exist_ok=True)
    for p in picks:
        vid, k = p.rsplit("=", 1)
        f = folder / f"{vid}.mp4"
        t = float(k[1:]) if k.startswith("@") else times(f)[int(k)]   # <id>=@초 로 정확한 시각을 줄 수 있다
        im = grab(f, t, 1280)
        im.save(OUT / f"{vid}.webp", quality=82, method=6)
        print("pick", vid, k)


if __name__ == "__main__":
    cmd, folder = sys.argv[1], Path(sys.argv[2])
    sheets(folder) if cmd == "sheets" else pick(folder, sys.argv[3:])
