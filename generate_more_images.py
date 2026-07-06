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
        "filename": "energy-flow.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中心是一个温暖发光的心形容器，心形底部原本有一道小裂缝，金色硬币正从裂缝中流失；旁边是同一个人用双手修补好心形裂缝后，心形容器装满金色光芒，硬币围绕光芒旋转不再流失。画面上方用温暖橙棕色粗体字写中文标题“钱和爱都顺着内心流动”，旁边有手写小标签“内心有缺口 → 钱和爱会流走”“修补自爱 → 留住丰盛”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
    },
    {
        "filename": "only-inward.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个坚定的人物站在稳固的山顶平地上，双手握着一个船舵/方向盘，脚下是厚实的大地，身后是升起的太阳和稳固的山峦。人物表情平静自信，周围有细小的光点。画面上方用温暖橙棕色粗体字写中文标题“向内求是唯一可行的路”，旁边有手写小标签“可控”“可积累”“稳稳的”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
    },
    {
        "filename": "stop-external.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面左侧是一个人站在灰暗的迷宫/迷雾中，手伸向虚化的手和气球；右侧是同一个人已经走出迷雾，斩断了一条锁链，迈步走向明亮的开阔道路，道路尽头有温暖的阳光。画面上方用温暖橙棕色粗体字写中文标题“停止外求，开始自由”，旁边有手写小标签“外求=原地打转”“喊停=出路”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
    },
    {
        "filename": "early-inward.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面是一条向远方延伸的开阔道路，道路尽头是温暖的朝阳/金色光芒，一个轻盈的人物正在道路上奔跑，身后拖出一道金色光带。道路两旁有成长中的小植物和花朵。画面上方用温暖橙棕色粗体字写中文标题“越早向内求，越早开挂”，旁边有手写小标签“停止消耗”“专注耕耘”“人生正循环”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。横图构图。"
    },
    {
        "filename": "sos-kit.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中心是一个打开的急救箱/急救包，里面整齐摆放着手绘物品：一个红色暂停按钮、一个创可贴、一面小镜子、一本写着“我可以”的笔记本、一盆小绿植。急救箱旁边有一只温柔的手正做出“停止”手势。画面上方用温暖橙棕色粗体字写中文标题“一招走出内耗急救包”，下方有手写小字“觉察→喊停→转向”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
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
        print(f"Generating {item['filename']}...")
        try:
            result = generate_image(item["prompt"])
            print(json.dumps(result, ensure_ascii=False, indent=2)[:500])

            url = result.get("data", [{}])[0].get("url")
            if not url:
                print(f"No URL returned for {item['filename']}")
                continue

            dest = OUTPUT_DIR / item["filename"]
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
