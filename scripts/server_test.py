from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/test', methods=['POST'])
def test():
    # 获取请求的 JSON 数据
    data = request.get_json()
    message = data.get("message", "No message received")
    print(f"Received from ESP32: {message}")
    
    # 返回响应
    return jsonify({"response": f"Message '{message}' received successfully!"})

if __name__ == '__main__':
    # 替换为你的实际 IP 地址，确保 Flask 监听在该 IP 上
    app.run(host='192.168.137.1', port=5000)


