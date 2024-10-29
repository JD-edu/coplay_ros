import rclpy as rp
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor

from cv_bridge import CvBridge

from std_msgs.msg import String
from sensor_msgs.msg import Image

import cv2
import numpy as np
import websockets
import asyncio

class EspMsgSubscription(Node):
    def __init__(self):
        super().__init__('esp_msg_subscription')
        self.sub_msg = self.create_subscription(String, '/esp/msg', self.callback_msg, 10)

    def callback_msg(self, data):
        msg = data.data
        asyncio.run(self.send_msg(msg))

    async def send_msg(self, msg):
        url = ""
        async with websockets.connect(url) as ws:
            await ws.send(msg) 
            print(f"Sent: {msg}")

class EspImgPublisher(Node):
    def __init__(self):
        super().__init__('esp_img_publisher')
        self.pub_img = self.create_publisher(Image, '/esp/image', 10)
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.bridge = CvBridge()

    def timer_callback(self):
        asyncio.run(self.recive_image())

    async def recive_image(self):
        url = 'ws://192.168.0.77:8276/pang/ws/sub?channel=cakjdd4k058s72qr0prg&track=colink&mode=bundle'
        while True:
            try:
                async with websockets.connect(url) as ws:
                    while True:
                        img_binary_data = await ws.recv()
                        encoded_img = np.frombuffer(img_binary_data, dtype = np.uint8)
                        img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
                        cv2.imshow('receiver', img)
                        img_msg = self.bridge.cv2_to_imgmsg(img, encoding='bgr8')
                        self.pub_img.publish(img_msg)
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

            except Exception as e:
                print('closed. try connecting')
                await asyncio.sleep(1)

def main():
    rp.init()

    sub_msg = EspMsgSubscription()
    pub_img = EspImgPublisher()

    executor = MultiThreadedExecutor()

    executor.add_node(sub_msg)
    executor.add_node(pub_img)

    try:
        executor.spin()
    finally:
        executor.shutdown()
        sub_msg.destroy_node()
        pub_img.destroy_node()
        rp.shutdown()

if __name__ == "__main__":
    main()
