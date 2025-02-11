import network
import time
from logger import Logger
logger = Logger(filename="app.log", level="INFO")

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('Isaac_Desktop', 'zhou@jiahui')

while not wlan.isconnected():
    time.sleep(1)

Logger.info('Connected to WiFi:', wlan.ifconfig())

import urequests
import json

# Replace with your server IP address
url = "http://192.168.137.1:5000/test"

data = {
    "message": "Hello from ESP32!",  
    # Image
    "image": '',
    # Prompt
    "text": "Please describe the objects and their counts in the image. Use the format 'item: count' for each object, and put each item on a new line. For example:\napple: 5\nbanana: 3\norange: 2."
}

try:
    # Send POST request
    response = urequests.post(url, json=data, timeout=10)  # 设置超时为 10 秒
    if response.status_code == 200:
        result = response.json()
        print("Response from server:", result["response"])
    else:
        Logger.error("Request failed:", response.text)
except Exception as e:
    Logger.error("Request failed:", e)
