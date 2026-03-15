import requests
import json


def get_meta_url():
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    meta_url = []
    for i in data.keys():
        response = requests.get(
            f"https://prts.wiki/api.php?action=query&prop=imageinfo&iiprop=url&format=json&titles=File:头像_{i}.png"
        )
        if response.status_code == 200:
            meta_url.append(response.json())
            print(f"{i} 获取成功")
        else:
            print(f"{i} 获取失败，状态码: {response.status_code}")
    with open("meta_url.json", "w", encoding="utf-8") as f:
        json.dump(meta_url, f, ensure_ascii=False, indent=4)


def save_images():
    with open("meta_url.json", "r", encoding="utf-8") as f:
        meta_url = json.load(f)
    for item in meta_url:
        name = next(iter(item["query"]["pages"].values()))["title"].replace("文件:头像 ", "").replace(".png", "")
        download_image_url = next(iter(item["query"]["pages"].values()))["imageinfo"][0]["url"]
        print(name)
        print(download_image_url)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
            "Referer": "https://prts.wiki/",
        }
        try: 
            response = requests.get(download_image_url, headers=headers, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            with open(f"images/{name}.png", "wb") as f:
                f.write(response.content)
            print(f"✅ {name} 保存成功！")
        except Exception as e:
            print(f"❌{name} 下载失败: {e}")


def main():
    # get_meta_url()
    save_images()


if __name__ == "__main__":
    main()
