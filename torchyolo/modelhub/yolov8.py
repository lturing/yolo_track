import cv2
import torch
from tqdm import tqdm

from torchyolo.tracker.tracker_zoo import load_tracker
from torchyolo.utils.dataset import LoadData, create_video_writer
from torchyolo.utils.load_config import load_parameters
from torchyolo.utils.object_vis import video_vis
from collections import defaultdict
import numpy as np

class Yolov8DetectionModel:
    def __init__(
        self,
        config_path: str,
        model_path: str = "yolov8s.pt",
    ):

        self.model_path = model_path
        self.load_config(config_path)
        self.load_model()

    def load_config(self, config_path: str):
        self.config_path = config_path
        self.output_path, self.conf, self.iou, self.image_size, self.device, self.save, self.show = load_parameters(
            self.config_path
        )

    def load_model(self):
        try:
            from ultralytics import YOLO

            model = YOLO(self.model_path)
            model.conf = self.conf
            model.iou = self.iou
            self.model = model

        except ImportError:
            raise ImportError('Please run "pip install ultralytics" ' "to install YOLOv8 first for YOLOv8 inference.")

    def predict(self, source: str):
        dataset = LoadData(source)
        video_writer = create_video_writer(video_path=source, output_path=self.output_path)

        for img_src, img_path, vid_cap in tqdm(dataset):
            results = self.model.predict(img_src, imgsz=self.image_size)
            for image_id, prediction in enumerate(results[0].boxes.cpu().numpy()):
                bbox, category_id, score = (
                    prediction.xyxy,
                    prediction.cls,
                    prediction.conf,
                )
                category_name = self.model.model.names[int(category_id)]
                label = f"{category_name} {float(score):.2f}"

                if self.save or self.show:
                    frame = video_vis(
                        bbox=bbox[0],
                        label=label,
                        frame=img_src,
                        object_id=int(category_id),
                    )
                if self.save:
                    if source.endswith(".mp4"):
                        video_writer.write(frame)
                    else:
                        cv2.imwrite("output.jpg", frame)

    def tracker_predict(
        self,
        source: str = None,
        tracker_type: str = None,
        tracker_weight_path: str = None,
        tracker_config_path: str = None,
    ):
        if tracker_type == "STRONGSORT":
            tracker_module = load_tracker(
                config_path=self.config_path,
                tracker_type=tracker_type,
                tracker_weight_path=tracker_weight_path,
                tracker_config_path=tracker_config_path,
            )

        else:
            tracker_module = load_tracker(
                config_path=self.config_path,
                tracker_type=tracker_type,
                tracker_config_path=tracker_config_path,
            )

        tracker_outputs = [None]
        dataset = LoadData(source)
        video_writer = create_video_writer(video_path=source, output_path=self.output_path, fps=10)
        track_history = defaultdict(lambda: [])
        cnt = 0

        for img_src, img_path, vid_cap in tqdm(dataset):
            results = self.model.predict(img_src, imgsz=self.image_size)
            for image_id, prediction in enumerate(results):
                boxes = prediction[:].boxes.xyxy
                score = prediction[:].boxes.conf
                category_id = prediction[:].boxes.cls
                dets = torch.cat((boxes, score.unsqueeze(1), category_id.unsqueeze(1)), dim=1)
                tracker_outputs[image_id] = tracker_module.update(dets.cpu(), img_src)
                for output in tracker_outputs[image_id]:
                    bbox, track_id, category_id, score = (
                        output[:4],
                        int(output[4]),
                        output[5],
                        output[6],
                    )
                    category_name = self.model.model.names[int(category_id)]
                    label = f"Id:{track_id} {category_name} {float(score):.2f}"

                    img_src = video_vis(
                            bbox=bbox,
                            label=label,
                            frame=img_src,
                            object_id=int(category_id),
                        )

                    track = track_history[track_id]
                    x, y, w, h = bbox[0], bbox[1], bbox[2], bbox[3]
                    track.append(((x+w)/2, (y+h)/2))  # x, y center point
                    if len(track) > 30:  # retain 90 tracks for 90 frames
                        track.pop(0)

                    points = np.hstack(track).astype(np.int32).reshape((-1, 1, 2)) 
                    cv2.polylines(img_src, [points], isClosed=False, color=(0, 0, 255), thickness=2)

                cv2.imshow("output", img_src)
                cv2.waitKey(1)
                #cv2.imwrite(os.path.join(des, str(cnt) + '.png'), img_src)
                cnt += 1
                video_writer.write(img_src)
                
        video_writer.release()
        cv2.destroyAllWindows()
