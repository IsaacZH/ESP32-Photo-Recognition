import os
import base64
from PIL import Image
 
from openai import OpenAI

MOONSHOT_API_KEY = os.environ.get("MOONSHOT_API_KEY")
if not MOONSHOT_API_KEY:
    raise ValueError("No API key found in environment variables")


client = OpenAI(
    api_key=MOONSHOT_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)
 
# 在这里，你需要将 kimi.png 文件替换为你想让 Kimi 识别的图片的地址
image_path = "spacex.jpg"

# 打开图像并降低分辨率
with Image.open(image_path) as img:
    img = img.convert("L")  # 转换为灰度图
    img = img.resize((img.width // 6, img.height // 6))
    img.save("resized_" + image_path)
    image_path = "resized_" + image_path
    
with open(image_path, "rb") as f:
    image_data = f.read()
 
# 我们使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
image_url = f"data:image/{os.path.splitext(image_path)[1]};base64,{base64.b64encode(image_data).decode('utf-8')}"
 
# print(image_url) 

# 将 image_url 保存到本地的 image_url.txt 文件中
with open("image_url.txt", "w") as file:
    file.write(image_url)

completion = client.chat.completions.create(
    model="moonshot-v1-8k-vision-preview",
    messages=[
        {"role": "system", "content": "你是 Kimi。"},
        {
            "role": "user",
            # 注意这里，content 由原来的 str 类型变更为一个 list，这个 list 中包含多个部分的内容，图片（image_url）是一个部分（part），
            # 文字（text）是一个部分（part）
            "content": [
                {
                    "type": "image_url", # <-- 使用 image_url 类型来上传图片，内容为使用 base64 编码过的图片内容
                    "image_url": {
                        "url": image_url,
                    },
                },
                {
                    "type": "text",
                    "text": "Please describe the objects and their counts in the image. Use the format 'item: count' for each object, and put each item on a new line. For example:\napple: 5\nbanana: 3\norange: 2."
                },
            ],
        },
    ],
)

response_text = completion.choices[0].message.content 
print(response_text)

def parse_response(response_text):
    item_count = {}
    lines = response_text.strip().split("\n")
    
    for line in lines:
        item, count = line.split(": ")
        item_count[item] = int(count)
    
    return item_count

# Parse data
parsed_data = parse_response(response_text)
print(parsed_data)