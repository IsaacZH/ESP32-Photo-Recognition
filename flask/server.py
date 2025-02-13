from flask import Flask, request, jsonify
import os
import datetime
from openai import OpenAI
import base64

MOONSHOT_API_KEY = os.environ.get("MOONSHOT_API_KEY")
if not MOONSHOT_API_KEY:
    raise ValueError("No API key found in environment variables")


client = OpenAI(
    api_key=MOONSHOT_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    if request.content_type != 'image/jpeg':
        return 'Content-Type not supported!', 415
    
    # 获取请求的二进制数据
    data = request.data
    
    # 返回响应
    response = jsonify({"response": "Data received successfully!"})
    
    # 在返回响应后打印数据并保存到本地文件
    # 将数据转换为十六进制字符串
    hex_data = data.hex()
    print("Received data (hex):", hex_data[:200])
    
    # 确保 images 文件夹存在
    if not os.path.exists('images'):
        os.makedirs('images')
    
    # 使用当前时间戳作为文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    file_path = os.path.join('images', f"received_image_{timestamp}.jpg")
    
    # 将数据保存为 JPEG 文件
    with open(file_path, "wb") as f:
        f.write(data)
    # convert to base64

    image_url = f"data:image/{os.path.splitext(file_path)[1]};base64,{base64.b64encode(data).decode('utf-8')}"

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
     
    return response

if __name__ == '__main__':
    app.run(host='192.168.137.1', port=5000)