## yolo + track
目标检测支持yolov5、yolov6、yolov7、yolov8，跟踪支持byteTrack等

```
git clone https://github.com/lturing/yolo_track

cd yolo_track
1. 修改predict_kitti00_v2.py中的model_path、source，其中model_path为预训练模型参数的路径，source为图片路径
2. 根据图片分辨率修改torchyolo/configs/default_config.yaml中的IMAGE_SIZE(图片高度和宽度的最大值)
3. 根据数据的帧率修改 
    https://github.com/lturing/yolo_track/blob/main/torchyolo/modelhub/yolov5.py#L94
    https://github.com/lturing/yolo_track/blob/main/torchyolo/modelhub/yolov7.py#L89
    https://github.com/lturing/yolo_track/blob/main/torchyolo/modelhub/yolov8.py#L93
    等处的fps，fps将影响保存视频的帧率

# 下载yolo的预训练参数
- [yolov5](https://github.com/ultralytics/yolov5/releases)
- [yolov6](https://github.com/meituan/YOLOv6/releases)
- [yolov7](https://github.com/WongKinYiu/yolov7/releases)
- [yolov8](https://github.com/ultralytics/ultralytics)

# kitti数据下载参考 https://zhuanlan.zhihu.com/p/664386718

运行
python predict_kitti00_v2.py
# 结果会保存在当前目录下的output.mp4

```

## demo 
- [b站](https://www.bilibili.com/video/BV1zg4y1X7s6)


## 感谢
- [torchyolo](https://github.com/kadirnar/torchyolo)



