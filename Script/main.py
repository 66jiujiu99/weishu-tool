import cv2
import numpy as np
import pyautogui
import easyocr
import time
import json
import os
import re
from pynput import mouse
from pynput import keyboard

"""
ROI selection completed.:{'干员名称': (5, 140, 207, 47), '特质分类': (60, 566, 382, 43), '特质描述': (21, 613, 444, 78), '盟约': (20, 751, 114, 290), '阶位': (264, 127, 70, 50)}
"""

reader = easyocr.Reader(
    ["ch_sim", "en"], gpu=True
)  # 这里直接初始化了 GPU 模式的 Reader，确保后续 OCR 识别能使用 GPU 加速
ROI_CONFIG = {
    "干员": (5, 165, 192, 46),
    "阶位": (248, 153, 63, 50),
    "分类": (55, 565, 315, 31),
    "描述": (14, 600, 403, 99),
    "盟约": (25, 724, 90, 306),
}  # {"键名" : (x, y, w, h)}


def get_tags(description):
    # 定义特质标签的正则表达式
    tag_pattern = r"<([^>]+)>"
    # 使用正则表达式提取特质标签
    tags = re.findall(tag_pattern, description)
    return tags


def select_rois():
    print("Selecting ROIs...")
    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    while True:
        cv2.namedWindow("Select ROI", cv2.WINDOW_GUI_EXPANDED)
        roi = cv2.selectROI("Select ROI", img, False)
        if roi == (0, 0, 0, 0):
            break
        key_name = input("键名: ")
        if not key_name:
            print("键名不能为空!")
            continue
        ROI_CONFIG[key_name] = roi
        print(f"已记录 {key_name}: {roi}")
    cv2.destroyAllWindows()
    print(f"ROI selection completed.:{ROI_CONFIG}")


def ocr_and_save():
    print("\n[!] 正在识别区域...")
    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    cv2.imwrite("full_screenshot.png", cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR))
    raw_text_map = {}
    for key, (x, y, w, h) in ROI_CONFIG.items():
        # 裁剪出目标区域
        crop = screen_np[y : y + h, x : x + w]
        # cv2.imwrite(f"{key}.png", crop)
        # OCR识别
        text_list = reader.readtext(crop, detail=0)
        raw_text_map[key] = " ".join(text_list)
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    new_row = {
        "盟约": raw_text_map["盟约"].strip().split(),
        "特质": {
            "分类": raw_text_map["分类"],
            "tag": get_tags(raw_text_map["描述"]),
            "描述": raw_text_map["描述"],
        },
        "阶位": raw_text_map["阶位"],
    }
    print(f"\n[!] 识别结果 {raw_text_map['干员']}:\n{new_row}")
    data[raw_text_map["干员"]] = new_row
    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_mengye():
    print("\n[!] 正在识别区域...")
    screenshot = pyautogui.screenshot()
    screen_np = np.array(screenshot)
    cv2.imwrite("full_screenshot.png", cv2.cvtColor(screen_np, cv2.COLOR_RGB2BGR))
    raw_text_map = {}
    for key, (x, y, w, h) in ROI_CONFIG.items():
        # 裁剪出目标区域
        crop = screen_np[y : y + h, x : x + w]
        # cv2.imwrite(f"{key}.png", crop)
        # OCR识别
        text_list = reader.readtext(crop, detail=0)
        raw_text_map[key] = " ".join(text_list)
    with open("data_盟约.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    new_row = {
        "激活需要人数": raw_text_map["激活需要人数"],
        "描述": raw_text_map["描述"]
    }
    print(f"\n[!] 识别结果 {raw_text_map['盟约']}:\n{new_row}")
    data[raw_text_map["盟约"]] = new_row
    with open("data_盟约.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)    

def on_press(key):
    try:
        # 监听 Enter 键 (Key.enter)
        if key == keyboard.Key.enter:
            get_mengye()
        # 额外加一个退出键，比如 ESC
        if key == keyboard.Key.esc:
            print("退出程序...")
            return False
    except Exception as e:
        print(f"错误: {e}")


def main():
    op = input("是否需要重新选择ROI? (y/n): ").strip().lower()
    if op == "y":
        time.sleep(2)
        select_rois()
        if not ROI_CONFIG:
            print("未配置任何区域，程序退出。")
            exit(1)

    print("\n--- 脚本已启动 ---")
    print("操作方式：enter 键启动，esc 键退出。")

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()


"""
{
'干员': '凛御银灰',
'阶位': '5阶',
'分类': '持续叠加', 
'描述': '<战斗开始时>使身前一格{谢拉格]  干员获得 特质 "范围内1名敌人进入冻结时。有700概 率使巳激活的[谢拉格]  层 数+1', 
'盟约': '谢拉格 迅捷'
}

"""
