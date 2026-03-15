import torch
import easyocr

print(f"PyTorch 版本: {torch.__version__}")
print(f"CUDA 是否可用: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"正在使用的显卡: {torch.cuda.get_device_name(0)}")
    # 初始化一个 GPU 模式的 Reader 看看
    reader = easyocr.Reader(['ch_sim', 'en'], gpu=True)
    print("EasyOCR 已成功加载 GPU 权重！")
else:
    print("依然无法检测到 GPU，请确认安装命令中是否带有 --index-url")