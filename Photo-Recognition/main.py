import network
import time
from logger import Logger
logger = Logger(filename="app.log", level="INFO", min_level="INFO")

def parse_response(response_text):    
    """
    解析服务器响应文本，将其转换为字典格式。

    参数：
    response_text (str): 服务器响应的文本。

    返回：
    dict: 包含项目及其计数的字典。
    """
    item_count = {}
    lines = response_text.strip().split("\n")
    
    for line in lines:
        if ":" not in line:
            continue
        item, count = line.split(":").strip()
        item_count[item] = int(count)
    
    return item_count



logger.debug("Starting the application...")

###########################################################
#################      连接到WI-FI       ##################
###########################################################

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Isaac_Desktop', 'zhou@jiahui')

logger.info('Connecting to WiFi...')
while not wlan.isconnected():
    time.sleep(1)

logger.info('Connected to WiFi:', wlan.ifconfig())

import urequests
import json

###########################################################
#################       服务器请求        ##################
###########################################################
url = "http://192.168.137.1:5000/test"

data = {
    "message": "Hello from ESP32!",  
    # 图像
    "image": 'data:image/.jpg;base64,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',
    # 提示词
    "text": "Please describe the objects and their counts in the image. Use the format 'item: count' for each object, and put each item on a new line. For example:\napple: 5\nbanana: 3\norange: 2."
}

try:
    # 发送 POST 请求
    response = urequests.post(url, json=data, timeout=10)  # 设置超时为 10 秒
    if response.status_code == 200:
        result = response.json()
        response_text = result["response"]
        logger.info("Response from server:", response_text)
        # Parse data
        parsed_data = parse_response(response_text)
        logger.info(parsed_data)
    else:
        logger.error("Request failed:", response.text)
except Exception as e:
    logger.error("Request failed:", e)

logger.debug("Shutting down the application...")
