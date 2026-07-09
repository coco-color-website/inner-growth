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
        "filename": "core-point-1.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一面明亮的镜子，镜子里反射出一颗巨大发光的心，镜外有 several small gray broken hearts trying to reach the mirror but staying outside. 画面上方用温暖橙棕色粗体字写中文标题“任何人的爱都不会超过自己的”，旁边有手写小标签“别人的爱=破铜烂铁”“自己的爱=珍宝”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
    },
    {
        "filename": "core-point-2.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一颗巨大、完整、发光的爱心，旁边有几颗较小、颜色较淡的爱心。大爱心上有一个温柔的手写标签“自爱最真”。画面上方用温暖橙棕色粗体字写中文标题“自爱最真”，旁边有手写小标签“自己给自己的爱才是解药”“任何人的爱都不纯粹”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
    },
    {
        "filename": "core-point-3.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个人物站在自己肩上，双手稳稳托举着三样发光的东西：一颗心形（代表爱）、一个拥抱自己的手臂（代表被爱）、一枚金币（代表赚钱责任）。人物表情平静有力，周围有扎根的土壤和小植物。画面上方用温暖橙棕色粗体字写中文标题“把期待完完全全放在自己身上”，旁边有手写小标签“缺爱爱自己”“缺钱做事赚钱”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
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
