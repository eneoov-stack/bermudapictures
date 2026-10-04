#!/usr/bin/env python3
"""버뮤다픽쳐스 홈페이지 데이터 — 채널 재생목록과 공개 영상 목록을 읽기 전용으로 가져온다 (2026-10-04).
tools/youtube-upload.py 의 youtube() 인증(token.json, readonly 범위)을 그대로 쓴다. 쓰기 호출은 없다.
usage: python fetch_channel.py  -> ../data/channel.json
"""
import importlib.util
import json
from pathlib import Path

ROOT = Path(r"F:/seedance-prompt-builder")   # tools/youtube-upload.py 가 있는 작업 저장소 (기계마다 다르면 고친다). 지금 빌드에는 쓰지 않는다
spec = importlib.util.spec_from_file_location("ytu", ROOT / "tools" / "youtube-upload.py")
ytu = importlib.util.module_from_spec(spec); spec.loader.exec_module(ytu)
OUT = Path(__file__).resolve().parents[1] / "data" / "channel.json"


def pages(call, **kw):
    token = None
    while True:
        res = call(pageToken=token, **kw).execute() if token else call(**kw).execute()
        yield from res.get("items", [])
        token = res.get("nextPageToken")
        if not token:
            return


def main():
    yt = ytu.youtube()
    ch = yt.channels().list(part="snippet,statistics,contentDetails", id=ytu.EXPECTED_CHANNEL_ID).execute()["items"][0]
    playlists = [{"id": p["id"], "title": p["snippet"]["title"], "count": p["contentDetails"]["itemCount"],
                  "privacy": p["status"]["privacyStatus"]}
                 for p in pages(yt.playlists().list, part="snippet,contentDetails,status", channelId=ch["id"], maxResults=50)]
    for p in playlists:
        p["video_ids"] = [i["contentDetails"]["videoId"]
                          for i in pages(yt.playlistItems().list, part="contentDetails", playlistId=p["id"], maxResults=50)]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    all_ids = [i["contentDetails"]["videoId"] for i in pages(yt.playlistItems().list, part="contentDetails", playlistId=uploads, maxResults=50)]
    videos = {}
    for k in range(0, len(all_ids), 50):
        for v in yt.videos().list(part="snippet,status,statistics,contentDetails", id=",".join(all_ids[k:k + 50])).execute()["items"]:
            if v["status"]["privacyStatus"] != "public":
                continue   # 비공개·예약·일부공개는 사이트에 싣지 않는다
            videos[v["id"]] = {"title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"],
                               "views": int(v["statistics"].get("viewCount", 0)), "duration": v["contentDetails"]["duration"],
                               "thumb": f"https://i.ytimg.com/vi/{v['id']}/hqdefault.jpg"}
    data = {"channel": {"id": ch["id"], "title": ch["snippet"]["title"], "handle": ch["snippet"].get("customUrl"),
                        "subscribers": int(ch["statistics"].get("subscriberCount", 0)),
                        "videos": int(ch["statistics"].get("videoCount", 0))},
            "playlists": playlists, "videos": videos}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"ok {len(playlists)} playlists, {len(videos)} public videos -> {OUT}")


if __name__ == "__main__":
    main()
