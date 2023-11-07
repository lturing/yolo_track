import cv2
import numpy as np


class Colors:
    # Ultralytics color palette https://ultralytics.com/
    def __init__(self):
        # hex = matplotlib.colors.TABLEAU_COLORS.values()
        hexs = (
            "FF3838",
            "FF9D97",
            "FF701F",
            "FFB21D",
            "CFD231",
            "48F90A",
            "92CC17",
            "3DDB86",
            "1A9334",
            "00D4BB",
            "2C99A8",
            "00C2FF",
            "344593",
            "6473FF",
            "0018EC",
            "8438FF",
            "520085",
            "CB38FF",
            "FF95C8",
            "FF37C7",
        )
        self.palette = [self.hex2rgb(f"#{c}") for c in hexs]
        self.n = len(self.palette)

    def __call__(self, i, bgr=False):
        c = self.palette[int(i) % self.n]
        return (c[2], c[1], c[0]) if bgr else c

    @staticmethod
    def hex2rgb(h):  # rgb order (PIL)
        return tuple(int(h[1 + i : 1 + i + 2], 16) for i in (0, 2, 4))


def video_vis(
    object_id,
    label,
    frame,
    bbox,
) -> np.ndarray:
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    MIN_FONT_SCALE = 0.7
    color = Colors()(object_id + 12)
    txt_color = (0, 0, 0) if np.mean(color) > 0.5 else (255, 255, 255)
    txt_color = (255, 255, 255)
    font_scale = max(MIN_FONT_SCALE, 0.3 * (w + h) / 600)

    thickness = 2
    font_scale = thickness / 3
    font_thickness = max(thickness -1, 1)
    
    txt_size = cv2.getTextSize(label, 0, font_scale, font_thickness)[0]
    cv2.rectangle(frame, (x, y), (w, h), color, thickness, lineType=cv2.LINE_AA)  # object box
    cv2.rectangle(frame, (x, y - txt_size[1]), (x + txt_size[0], y), color, -1, lineType=cv2.LINE_AA)  # object label box
    cv2.putText(
        frame,
        label,
        (x, y - 2),
        0,
        font_scale,
        txt_color,
        font_thickness,
        cv2.LINE_AA,
    )
    return frame
