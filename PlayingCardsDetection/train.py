import os
from pathlib import Path
from ultralytics import YOLO

HERE = Path(__file__).parent
DATA_YAML = HERE / "data_config" / "playing_cards.yaml"

# Windows data loader workers re-import this file, so training must stay behind this guard
if __name__ == "__main__":
    os.chdir(HERE)  # the dataset path in the yaml is relative to the working directory
    model = YOLO("pretrained/yolov8s_playing_cards.pt")

    results = model.train(data=str(DATA_YAML), epochs=150, patience=40, imgsz=1280, batch=8, fliplr=0.0,
            project=str(HERE / "runs"), name="playing_cards", exist_ok=True)
    # best weights -> PlayingCardsDetection/runs/playing_cards/weights/best.pt
    print(results.results_dict)
