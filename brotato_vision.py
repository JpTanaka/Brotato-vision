import torch
from ultralytics import YOLO

if torch.cuda.is_available():
    torch.cuda.set_device(0)

from PIL import Image, ImageGrab
import time
import cv2
import numpy as np
import pywinctl as pwc
import argparse
from pathlib import Path
from typing import Union

class Detector():
    def __init__(self, model_path : str):
        self.model = YOLO(model_path)
    
    def _draw_prediction(self, source : Union[str, np.ndarray]):
        results = self.model.predict(source=source)
        for r in results:
            im = Image.fromarray(r.plot()[..., ::-1])
            im = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)
            cv2.imshow("Brotato Vision (Press Q to stop)", im)
    
    def _press_Q(self, timer : int) -> bool:
        return cv2.waitKey(timer) & 0xFF == ord("q") 
    
    
    def detect_from_game(self) -> None:
        # Find a window with game's name as substring
        game_window_title = "Brotato"
        game_window = pwc.getWindowsWithTitle("Brotato")
        if not game_window:
            print(f"Error: Unable to find the game window with title '{game_window_title}'")
            exit()

        # Get the game window's bounding box
        bbox = (
            game_window[0].left,
            game_window[0].top,
            game_window[0].left + game_window[0].width,
            game_window[0].top + game_window[0].height
        )

        while True:
            # check if user pressed Q 
            if self._press_Q(55): break
            
            # print screen at window location
            screenshot = ImageGrab.grab(bbox)
            
            self._draw_prediction(screenshot)
            time.sleep(0.05)

    def detect_from_video(self, video_path : str) -> None:
        capture = cv2.VideoCapture(video_path)
        current_frame = 0
        interval_frames = 10
        while True:
            # check if user pressed Q
            if self._press_Q(55): break
            
            # check if end of video was reached
            ret, frame = capture.read()
            if not ret: break
            
            # print at interval_frames rate 
            if current_frame % interval_frames == 0:
                self._draw_prediction(frame)

            current_frame += 1
        capture.release()

    def detect_from_image(self, image_path : str) -> None:
        self._draw_prediction(image_path)

        # wait until user press Q
        self._press_Q(0)
    

def check_file_path(path):
    path = Path(path)
    if not path.is_file():
        raise argparse.ArgumentTypeError(f"File not found: {path}")
    return str(path)

if __name__ == "__main__":
    # project_dir = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(description="Brotato-Vision: YOLO fine-tuned to detect objets in Brotato")

    parser.add_argument("--image", type=check_file_path, help="Path to image")
    parser.add_argument("--video", type=check_file_path, help="Path to video")
    parser.add_argument("--game", action="store_true", default=None, help="Run YOLO on game window")
    parser.add_argument("--model_path", type=check_file_path, default="trained_model.pt", help="Path to model")
    args = parser.parse_args()

    # default to --game if no option is provided
    if not any([args.image, args.video, args.game]):
        print("No option provided, running script in --game mode")
        args.game = True

    # only one mode can be selected
    if sum(bool(arg) for arg in [args.image, args.video, args.game]) != 1:
        parser.error("Exactly one of --image, --video, or --game must be specified.")
    
    brotato_vision = Detector(args.model_path)
    
    if args.game:
        brotato_vision.detect_from_game()
    elif args.video:
        brotato_vision.detect_from_video(args.video)
    elif args.image:
        brotato_vision.detect_from_image(args.image)

    cv2.destroyAllWindows()