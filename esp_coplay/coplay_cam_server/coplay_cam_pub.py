import websockets
import asyncio
import cv2
import time
from datetime import datetime

connections = set()
connections.update([
    #"ws://cobot.center:8286/pang/ws/pub?channel=instant&name=dGVzdA==&track=video",
    #"ws://cobot.center:8286/pang/ws/pub?channel=instant&name=dGVzdA==&track=colink",
    #"ws://cobot.center:8286/pang/ws/sub?channel=instant&name=dGVzdA==&track=metric"
    "ws://192.168.0.77:8276/pang/ws/pub?channel=cakjdd4k058s72qr0prg&track=colink&mode=bundle"
]
)


async def websockets_handler(uri):
    async with websockets.connect(uri, ping_interval=None) as ws:
        print("Connected to", uri)
        track = uri.split("&mode=", 1)[1]
        if track == "bundle":
            frame_data = cv2.VideoCapture(0)
            #frame_data.set(3, 320)
            #frame_data.set(4, 240)
            while True:
                await asyncio.sleep(0.016)
                try:
                    _, image = frame_data.read()
                    #cv2.imshow('sender',image)
                    binary_image = cv2.imencode(".JPEG", image)[1].tobytes()
                    await ws.send(binary_image)
                    #if cv2.waitKey(1) & 0xFF == ord('q'):
                    #    break
                except:
                    print("cv error")
        elif track == "colink":
            while True:
                await asyncio.sleep(1)
                colink_data = datetime.now()
                await ws.send("source: &track=" + track + ", data: " + str(colink_data))
        elif track == "metric":
            while True:
                await asyncio.sleep(0.016)
                metric_data = await ws.recv()
                print(metric_data)


async def connect_websocket():
    tasks = [websockets_handler(uri) for uri in connections]
    await asyncio.gather(*tasks)


def main():
    asyncio.run(connect_websocket())


if __name__ == '__main__':
    main()
