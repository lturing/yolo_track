import cv2
from ultralytics import YOLO
import glob 
from collections import defaultdict
import numpy as np

# Load the YOLOv8 model
#model = YOLO('/home/spurs/x/yolov8/yolov8n.pt')

#model = YOLO('/home/spurs/x/yolov8/yolov8x.pt')
#model = YOLO('/home/spurs/x/yolov8/yolov8x-oiv7.pt')

model= YOLO('/home/spurs/x/yolov8/yolo-object-detection-kitti/yolov8n-kitti/train/weights/best.pt')

#model = YOLO('/home/spurs/x/yolov8/yolov5x-seg.pt')

# /home/spurs/dataset/kitti_rgb_00/image_2

#images = glob.glob("/home/spurs/dataset/kitti_00/image_0/*.png")
images = glob.glob("/home/spurs/dataset/kitti_rgb_00/image_2/*.png")
#images = glob.glob("/home/spurs/dataset/kitti_raw/2011_10_03/2011_10_03_drive_0047_sync/image_02/data/*.png")
# /home/spurs/dataset/kitti_rgb_00/image_2

images.sort()

print(len(images), images[0])

track_history = defaultdict(lambda: [])

for path in images:
    img = cv2.imread(path)
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #results = model(img)
    results = model.track(img, persist=True, tracker="bytetrack.yaml", imgsz=1280) # botsort.yaml
    annotated_frame = results[0].plot()
    if results[0].boxes.id != None: 
        track_ids = results[0].boxes.id.int().cpu().tolist()
        boxes = results[0].boxes.xywh.cpu()

    for box, track_id in zip(boxes, track_ids):
        x, y, w, h = box
        track = track_history[track_id]
        track.append((float(x), float(y)))  # x, y center point
        if len(track) > 30:  # retain 90 tracks for 90 frames
            track.pop(0)

        points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2))
        cv2.polylines(annotated_frame, [points], isClosed=False, color=(0, 0, 255), thickness=3)

    cv2.imshow("YOLOv8 Tracking", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


