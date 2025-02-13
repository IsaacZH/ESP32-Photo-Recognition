from flask import Flask, request, jsonify
import os
import datetime

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
    
    return response

if __name__ == '__main__':
    app.run(host='192.168.137.1', port=5000)