# Ready to use 
Download this repository into your ROS workspace source folder. 
There is 2 important pythn scripts.

**esp_ros.py**: subscriber ROS node python script 
**coplay_cam_pub.py**: publisher python script

## CoPlay server address setting 
To use CoPlay, you need to set CoPlay server URL. Server ULR is following code. Both publisher and subscriber have this code.  

```
connections.update([
    #"ws://cobot.center:8286/pang/ws/pub?channel=instant&name=dGVzdA==&track=video",
    #"ws://cobot.center:8286/pang/ws/pub?channel=instant&name=dGVzdA==&track=colink",
    #"ws://cobot.center:8286/pang/ws/sub?channel=instant&name=dGVzdA==&track=metric"
    "ws://192.168.0.77:8276/pang/ws/pub?channel=cakjdd4k058s72qr0prg&track=colink&mode=bundle"
]
)
```
In this code, "channel=cakjdd4k058s72qr0prg" is channel. Publisher and subscriber should have same channel.

## Build your ROS package
After that build your ROS2 package using following code. 
```
# at your ROS workspace source folder
$ colcon build
$ source install/setup.bash
```

## How to run 
At first run subscriber script. Subscriber is ROS2 node. So you can run it as follwing.

```
$ ros2 run ros2 run esp_coplay esp_ros
```
And then, run publisher script as following.
```
$ python coplay_cam_pub.py
```

If you run both scripts collectly, you can see video from cam that has window name "receiver". 
