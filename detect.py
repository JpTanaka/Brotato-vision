import torch
from ultralytics import YOLO

if torch.cuda.is_available(): 
    torch.cuda.set_device(0)

from PIL import Image, ImageGrab
import matplotlib.pyplot as plt
import os
import time
import cv2
import numpy as np

model = YOLO("runs/detect/train/weights/best.pt")

corner = (320, 210)
size = (1280, 720)
bbox = (corner[0], corner[1], corner[0] + size[0], corner[1] + size[1])

while True:
    screenshot = ImageGrab.grab(bbox)

    results = model.predict(source = screenshot)
    for r in results:
        im = Image.fromarray(r.plot()[..., ::-1])
        im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
        cv2.imshow("brotato", im)
        cv2.waitKey(1)
    time.sleep(0.05)
cv2.destroyAllWindows()