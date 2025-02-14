import os
import base64
import time  # 新增导入 time 模块
from openai import OpenAI

MOONSHOT_API_KEY = os.environ.get("MOONSHOT_API_KEY")
if not MOONSHOT_API_KEY:
    raise ValueError("No API key found in environment variables")
client = OpenAI(
    api_key=MOONSHOT_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)
 
# 在这里，你需要将 kimi.png 文件替换为你想让 Kimi 识别的图片的地址
image_path = "../images/received_image_20250213211758.jpg"

with open(image_path, "rb") as f:
    image_data = f.read()
 
# 我们使用标准库 base64.b64encode 函数将图片编码成 base64 格式的 image_url
image_url = f"data:image/{os.path.splitext(image_path)[1]};base64,{base64.b64encode(image_data).decode('utf-8')}"
 
start_time = time.time()  # 记录开始时间

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

end_time = time.time()  # 记录结束时间
elapsed_time = (end_time - start_time) * 1000  # 计算耗时，单位为毫秒

response_text = completion.choices[0].message.content 
print(response_text)
print(f"request take: {elapsed_time:.2f} ms")  # 输出请求耗时