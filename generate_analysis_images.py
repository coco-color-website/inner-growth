import json
import urllib.request
import urllib.error
import os
from pathlib import Path

API_KEY = "ark-7841e7bb-c9a3-4a70-9171-65ae63428f7d-3a8ef"
MODEL = "doubao-seedream-5-0-260128"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
OUTPUT_DIR = Path(r"c:\Users\cococ\Desktop\内在生长\website\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES = [
    {
        "filename": "analysis-og-cover.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记封面。画面中央是一个温柔发光的心形容器，心形底部有道小裂缝正在被一双手温柔修补，周围有镜子、小绿植、笔记本、存钱罐等象征自爱的小物件。画面整体温暖柔和，橙棕色为主，少量蓝灰辅助色。上方留白用于放置标题，不要有大字标题，像一页温和的手绘绘本式课程封面，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图，比例 1200:630。"
    },
    {
        "filename": "analysis-hero.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个人盘腿坐在一片发光的内在花园里，双手抱膝，周围有心形光点、小植物、镜子、存钱罐、笔记本。人物表情平静满足。画面上方留白，不要写标题。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记。横图构图。"
    }
]

def generate_image(prompt: str) -> str:
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "sequential_image_generation": "disabled",
        "response_format": "url",
        "size": "2K",
        "stream": False,
        "watermark": True
    }

    req = urllib.request.Request(
        BASE_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        return json.loads(resp.read().decode("utf-8"))

def download_image(url: str, dest: Path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as resp:
        with open(dest, "wb") as f:
            f.write(resp.read())

def main():
    for item in IMAGES:
        dest = OUTPUT_DIR / item["filename"]
        if dest.exists():
            print(f"Skipping {item['filename']}, already exists.")
            continue
        print(f"Generating {item['filename']}...")
        try:
            result = generate_image(item["prompt"])
            print(json.dumps(result, ensure_ascii=False, indent=2)[:500])

            url = result.get("data", [{}])[0].get("url")
            if not url:
                print(f"No URL returned for {item['filename']}")
                continue

            print(f"Downloading to {dest}...")
            download_image(url, dest)
            print(f"Saved {dest}\n")
        except urllib.error.HTTPError as e:
            print(f"HTTP Error for {item['filename']}: {e.code}")
            print(e.read().decode("utf-8"))
        except Exception as e:
            print(f"Error for {item['filename']}: {e}")

if __name__ == "__main__":
    main()
