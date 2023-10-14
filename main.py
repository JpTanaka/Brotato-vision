from ultralytics import YOLO
from PIL import Image

model = YOLO("yolov8m.pt")


results = model.train(data="config.yaml", epochs=10)
path = model.export(format="onnx")

results = model("images/video_1/frame_8.jpg")

for r in results:
    print(r)
    im_array = r.plot()
    im = Image.fromarray(im_array[..., ::-1])
    im.show()
    im.save("results.jpg")
