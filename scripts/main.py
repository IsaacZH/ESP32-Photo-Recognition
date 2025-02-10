import os
import json
import logging
from flask import Flask, request, jsonify
from openai import OpenAI

app = Flask(__name__)

# 设置 API 密钥
MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
if not MOONSHOT_API_KEY:
    raise ValueError("No API key found in environment variables")

client = OpenAI(
    api_key=MOONSHOT_API_KEY,
    base_url="https://api.moonshot.cn/v1",
)

@app.route('/test', methods=['POST'])
def upload():
    # 获取请求中的 JSON 数据
    data = request.get_json()
    
    # 获取图像和提示词
    image_base64 = data.get("image","No message received")
    text_prompt = data.get("text","No text received")
    # 输入前100个image_base64字符和text_prompt
    logging.info("image_base64: %s", image_base64[:100])
    logging.info("text_prompt: %s", text_prompt)
    
    # 调用 OpenAI API 进行图像识别
    completion = client.chat.completions.create(
        model="moonshot-v1-8k-vision-preview",
        messages=[
            {"role": "system", "content": "你是 Kimi。"},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",  # 使用图像 URL
                        "image_url": image_base64,
                    },
                    {
                        "type": "text",
                        "text": text_prompt,  # 提示词
                    },
                ],
            },
        ],
    )
    
    # 返回识别结果
    response = completion.choices[0].message.content
    print(response)
    return jsonify({"response": response})

if __name__ == '__main__':
    # 启动 Flask 服务器，监听 5000 端口
    app.run(host='192.168.137.1', port=5000)
