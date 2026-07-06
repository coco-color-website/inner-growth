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
        "filename": "update5-hero.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个人物站在分岔路口，左侧是灰暗迷雾中伸向外的无数只手，右侧是明亮温暖的内在花园，人物正转身走向内在花园，花园里有发光的爱心、金币、小植物。画面上方用温暖橙棕色粗体字写中文标题“本自具足向内求”，旁边有手写小标签“停止外求”“回到自己”“丰盛自来”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
    },
    {
        "filename": "update5-theory.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个温柔的天平，天平一侧是沉重的西瓜、创可贴、糖果等外物，另一侧是轻盈发光的镜子、爱心、小药瓶。天平向发光的一侧倾斜。画面上方用温暖橙棕色粗体字写中文标题“西瓜芝麻 · 创可贴 · 天秤 · 糖与解药”，旁边有手写小标签“外物压秤”“内里轻盈”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
    },
    {
        "filename": "update5-selflove.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一只手捧着一颗发光的爱心，爱心比周围灰蒙蒙、破损的小心心更大更亮。旁边有一个小标签写着“他人的爱=破铜烂铁”“自己的爱=珍宝”。画面上方用温暖橙棕色粗体字写中文标题“自己对自己的爱才是珍宝”，画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
    },
    {
        "filename": "update5-method.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个打开的帆布工具包，里面整齐摆放着手绘物品：一面镜子、一个存钱罐、一本写着“我可以”的笔记本、一盆扎根很深的小绿植、一个写着“做事”的小锤子。旁边有手写小标签“缺爱爱自己”“缺钱做事赚钱”。画面上方用温暖橙棕色粗体字写中文标题“向内扎根爱自己方法论”，画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
    },
    {
        "filename": "update5-abundance.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一条向远方延伸的金色道路，道路尽头是温暖的朝阳，一个轻盈的人物正在道路上奔跑，身后有金色光带。道路两旁是茂盛的植物和飞舞的金币、爱心光点。画面上方用温暖橙棕色粗体字写中文标题“越早向内求，越早开挂”，旁边有手写小标签“人生正循环”“丰盛幸福”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
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
