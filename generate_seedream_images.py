import json
import urllib.request
import urllib.error
import os
from pathlib import Path

API_KEY = "ark-0b872937-39b5-4070-9bfa-f1603014bc1a-cd549"
MODEL = "doubao-seedream-5-0-260128"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3/images/generations"
OUTPUT_DIR = Path(r"c:\Users\cococ\Desktop\内在生长\website\images")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

IMAGES = [
    {
        "filename": "self-love-treasure.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中央是一个温柔的人物侧身站立，面对一面复古圆镜，镜中映出一个微笑发光的自己；人物双手捧着一颗温暖发光的橙色钻石，钻石周围有细小光点。人物身后地面上散落着几块生锈的金属碎片和破铜烂铁，颜色灰暗无光泽。画面上方用温暖橙棕色粗体字写中文标题“自爱才是珍宝”，旁边有手写小标签“他人的爱≠可靠”“自己对自己的爱 排第一”。画面饱满但不拥挤，有真实纸面纹理，轻水彩笔触，温暖橙棕色为主，少量蓝灰辅助色，像一页温和的手绘绘本式课程笔记，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。方图构图。"
    },
    {
        "filename": "external-vs-internal.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面分为左右两个区域。左侧标题“向外求”用灰蓝色手写：一个人物焦虑地伸手向外抓取，周围有虚化的手、气球、爱心等象征外界认可，但人物身上有多条向外流失的橙色光带，像沙漏一样漏向画面外，脚下地面有裂缝。右侧标题“向内求”用温暖橙棕色手写：同一个人物闭目微笑，双手轻抱胸口，胸口发出温暖光芒，光芒化作植物根系向下扎根、向上生长成小花，周围有稳固的圆环。画面顶部有中文大标题“越外求越空，越内求越满”，中间用双向箭头连接两个区域。整体风格温暖手绘，纸面纹理，轻水彩马克笔质感，避免纯文字海报、避免细弱铅笔线、避免照片感和科技霓虹风。横图构图。"
    },
    {
        "filename": "self-care-toolkit.png",
        "prompt": "浅米色纸张背景，手绘手写风格的视觉知识笔记。画面中心是一只打开的帆布工具包，包盖翻开，里面整齐摆放着四样温暖的手绘物件：一面小圆镜（代表“看见并爱自己”）、一个橙色陶瓷存钱罐（代表“赚钱责任”）、一盆正在发芽的小绿植（代表“安全感与成长”）、一本摊开的笔记本上面写着“我可以”（代表“肯定与行动”）。每件物品旁边都有手写中文小标签。画面上方用温暖橙棕色粗体字写标题“向内求急救包”，下方有手写小字“缺爱→爱自己 / 缺钱→去赚钱 / 缺安全感→建秩序 / 缺力量→收能量”。画面四周有少量轻水彩斑点和纸胶带装饰，整体像一页温和的手绘绘本式课程笔记，真实纸面纹理，避免纯文字海报、避免只有线框箭头、避免铅笔线稿和照片感。竖图构图。"
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
