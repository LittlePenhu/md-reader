# -*- coding: utf-8 -*-
"""生成二次元风格应用图标（3 个候选，PNG 预览 + ICO）。"""
import os
from PIL import Image, ImageDraw

SIZE = 512
OUT = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUT, exist_ok=True)


def new_canvas():
    return Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))


def round_bg(d, cx, cy, r, outer, inner):
    """同心圆模拟渐变背景。"""
    steps = 8
    for i in range(steps):
        rr = r - i * (r // steps)
        alpha = 255 - i * 18
        color = outer if i == 0 else inner
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (alpha,))


def face(d, cx, cy, w, h, skin=(255, 232, 214)):
    d.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=skin + (255,))


def big_eye(d, cx, cy, w, h, color=(59, 43, 46)):
    d.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=color + (255,))
    d.ellipse([cx - w // 2 + 6, cy - h // 2 + 6, cx + w // 2 - 6, cy + h // 2 - 6], fill=color + (255,))
    d.ellipse([cx - w // 5, cy - h // 3, cx + w // 5, cy - h // 9], fill=(255, 255, 255, 255))          # 上高光
    d.ellipse([cx - w // 2 + 10, cy + h // 6, cx - w // 2 + 24, cy + h // 6 + 18], fill=(255, 255, 255, 255))  # 下小高光
    d.ellipse([cx - w // 2 + 16, cy - h // 2 + 30, cx - w // 2 + 30, cy - h // 2 + 44], fill=(255, 255, 255, 235))  # 眼角反光


def blush(d, cx, cy, r, color=(255, 150, 175, 110)):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)


def smile(d, x1, y1, x2, y2, color=(170, 90, 90), width=6):
    d.arc([x1, y1, x2, y2], start=15, end=165, fill=color + (255,), width=width)


def brow(d, x1, y1, x2, y2, color=(150, 110, 100), width=7):
    d.arc([min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2)], start=200, end=340, fill=color + (255,), width=width)


# ---------------- A：粉发猫耳少女 ----------------
def icon_a():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    round_bg(d, 256, 256, 242, (255, 176, 214), (255, 214, 235))
    # 猫耳（先画在头发下）
    for sx in (-1, 1):
        d.polygon([(256 + sx * 95, 175), (256 + sx * 40, 45), (256 + sx * 170, 95)], fill=(255, 148, 191, 255))
        d.polygon([(256 + sx * 100, 150), (256 + sx * 70, 80), (256 + sx * 145, 105)], fill=(255, 205, 225, 255))
    # 头发（后发 + 头顶）
    d.ellipse([76, 78, 436, 330], fill=(255, 148, 191, 255))
    d.ellipse([86, 120, 426, 430], fill=(255, 128, 181, 255))   # 侧发轮廓
    # 脸
    face(d, 256, 308, 252, 268)
    # 刘海
    d.ellipse([86, 96, 426, 268], fill=(255, 148, 191, 255))
    for dx in (-90, 0, 90):
        d.ellipse([256 + dx - 52, 200, 256 + dx + 52, 322], fill=(255, 148, 191, 255))
    # 呆毛
    d.arc([230, 30, 282, 110], start=200, end=330, fill=(255, 148, 191, 255), width=16)
    # 眼睛
    big_eye(d, 198, 322, 78, 100)
    big_eye(d, 314, 322, 78, 100)
    brow(d, 150, 262, 238, 272)
    brow(d, 274, 272, 362, 262)
    blush(d, 158, 392, 27)
    blush(d, 354, 392, 27)
    smile(d, 238, 388, 274, 416)
    return img


# ---------------- B：蓝发双马尾 ----------------
def icon_b():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    round_bg(d, 256, 256, 242, (122, 168, 255), (214, 232, 255))
    # 双马尾
    for sx in (-1, 1):
        d.ellipse([256 + sx * 250 - 70, 150, 256 + sx * 250 + 70, 360], fill=(110, 156, 242, 255))
        d.ellipse([256 + sx * 250 - 40, 190, 256 + sx * 250 + 40, 330], fill=(160, 196, 255, 255))
    # 头顶发
    d.ellipse([70, 70, 442, 330], fill=(110, 156, 242, 255))
    d.ellipse([80, 110, 432, 430], fill=(95, 140, 230, 255))
    # 脸
    face(d, 256, 308, 252, 268)
    # 刘海
    d.ellipse([80, 92, 432, 270], fill=(110, 156, 242, 255))
    for dx in (-80, 15, 105):
        d.ellipse([256 + dx - 50, 205, 256 + dx + 50, 325], fill=(110, 156, 242, 255))
    # 眼睛（金黄瞳）
    big_eye(d, 198, 322, 78, 100, color=(58, 52, 66))
    d.ellipse([166, 296, 230, 352], fill=(255, 201, 60, 255))   # 金瞳
    big_eye(d, 314, 322, 78, 100, color=(58, 52, 66))
    d.ellipse([282, 296, 346, 352], fill=(255, 201, 60, 255))
    brow(d, 150, 262, 238, 272)
    brow(d, 274, 272, 362, 262)
    blush(d, 158, 392, 27, (255, 160, 175, 110))
    blush(d, 354, 392, 27, (255, 160, 175, 110))
    smile(d, 238, 388, 274, 416)
    return img


# ---------------- C：金发元气笑脸 ----------------
def icon_c():
    img = new_canvas()
    d = ImageDraw.Draw(img)
    round_bg(d, 256, 256, 242, (255, 204, 92), (255, 240, 200))
    # 头发
    d.ellipse([66, 66, 446, 340], fill=(255, 196, 74, 255))
    d.ellipse([76, 110, 436, 430], fill=(240, 178, 60, 255))
    # 脸
    face(d, 256, 308, 252, 268)
    # 刘海（微微不对称更俏皮）
    d.ellipse([76, 90, 436, 272], fill=(255, 196, 74, 255))
    for dx in (-85, 5, 95):
        d.ellipse([256 + dx - 52, 202, 256 + dx + 52, 326], fill=(255, 196, 74, 255))
    d.ellipse([180, 180, 240, 300], fill=(255, 196, 74, 255))   # 侧刘海
    # 蝴蝶结
    d.polygon([(256, 60), (210, 20), (215, 70)], fill=(255, 90, 120, 255))
    d.polygon([(256, 60), (302, 20), (297, 70)], fill=(255, 90, 120, 255))
    d.ellipse([246, 48, 266, 72], fill=(255, 140, 160, 255))
    # 眼睛（绿瞳，笑得弯弯的）
    big_eye(d, 198, 322, 76, 96)
    d.ellipse([168, 298, 228, 350], fill=(87, 180, 100, 255))
    big_eye(d, 314, 322, 76, 96)
    d.ellipse([284, 298, 344, 350], fill=(87, 180, 100, 255))
    brow(d, 152, 260, 240, 270, (200, 140, 40))
    brow(d, 272, 270, 360, 260, (200, 140, 40))
    blush(d, 156, 392, 28)
    blush(d, 356, 392, 28)
    d.arc([226, 382, 286, 420], start=20, end=160, fill=(170, 90, 90, 255), width=7)  # 大笑
    return img


def save_all(name, img):
    img.save(os.path.join(OUT, name + ".png"))
    img.save(os.path.join(OUT, name + ".ico"),
             sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    print("已生成", name)


if __name__ == "__main__":
    save_all("A_粉发猫耳", icon_a())
    save_all("B_蓝发双马尾", icon_b())
    save_all("C_金发元气", icon_c())
