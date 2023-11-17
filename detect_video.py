import torch
from ultralytics import YOLO

if torch.cuda.is_available():
    torch.cuda.set_device(0)

from PIL import Image
import cv2
import numpy as np

model = YOLO("trained_model.pt")

corner = (320, 210)
size = (1280, 720)
bbox = (corner[0], corner[1], corner[0] + size[0], corner[1] + size[1])
# TODO: change video
video_path = "sample_video.mp4"
capture = cv2.VideoCapture(video_path)
current_frame = 0
interval_frames = 10
while True:
    if cv2.waitKey(55) & 0xFF == ord("q"):
        break
    ret, frame = capture.read()
    if not ret:
        break

    if current_frame % interval_frames == 0:
        results = model.predict(source=frame)
        for r in results:
            im = Image.fromarray(r.plot()[..., ::-1])
            im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            cv2.imshow("Brotato Vision (Press Q to stop)", im)
    current_frame += 1
capture.release()
cv2.destroyAllWindows()
