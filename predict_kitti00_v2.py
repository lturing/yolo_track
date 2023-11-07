from torchyolo import YoloHub

config_path = './torchyolo/configs/default_config.yaml'
#model_type = 'yolov5'
model_path = '/home/spurs/x/yolov8/yolov5x6.pt'
#model_path = '/home/spurs/x/yolov8/detector_yolov5s.pt'
#model_path = '/home/spurs/x/yolov8/yolov8x.pt'
#model_path = '/home/spurs/x/yolov8/yolo-object-detection-kitti/yolov8n-kitti/train/weights/best.pt'


#model_type = 'yolov7'
#model_path = '/home/spurs/x/yolov8/yolov7-e6e.pt'

if 'yolov5' in model_path:
    model_type = 'yolov5'
elif 'yolov7' in model_path:
    model_type = 'yolov7'
elif 'yolov8' in model_path:
    model_type = 'yolov8'
else:
    assert False, "error"

tracker_type = 'BYTETRACK'
tracker_config_path = './torchyolo/configs/tracker/byte_track.yaml'

source = '/home/spurs/dataset/kitti_rgb_00/image_2'
source = '/home/spurs/dataset/kitti_raw/2011_10_03/2011_10_03_drive_0047_sync/image_02/data'
#source = '/home/spurs/dataset/kitti_raw/2011_09_29/2011_09_29_drive_0071_sync/image_02/data'

print(f"model path: {model_path}, model type: {model_type}")
model = YoloHub(
    config_path=config_path,
    model_type=model_type,
    model_path=model_path,
)

result = model.tracker_predict(
        source=source,
        tracker_type=tracker_type,
        tracker_config_path=tracker_config_path)



