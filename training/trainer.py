import torch
from ultralytics import YOLO

if torch.cuda.is_available():
    torch.cuda.set_device(0)

from pathlib import Path
import os
import argparse

if __name__ == "__main__": 
    py_dir = Path(__file__).resolve().parent
    project_dir = py_dir.parent

    parser = argparse.ArgumentParser(description="Fine tune YOLO")

    parser.add_argument("--pre_trained", type=str, default="yolov8m.pt", help="Path / name of pre-trained model")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    args = parser.parse_args()
    
    pre_trained = args.pre_trained
    n_epochs = args.epochs

    # load pre-trained
    model = YOLO(pre_trained)

    # Train
    config_path = os.path.join(str(py_dir), "config.yaml")
    model.train(data=config_path, epochs=n_epochs)

    # Save
    model.save(os.path.join(str(project_dir), "new_trained_model.pt"))
