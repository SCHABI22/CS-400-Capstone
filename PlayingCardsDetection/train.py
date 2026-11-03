from pathlib import Path
from ultralytics import YOLO

DATA_YAML = Path(__file__).parent / "data_config" / "playing_cards.yaml"
model = YOLO("yolov8n.pt")

results = model.train(data=str(DATA_YAML), epochs=50, imgsz=640, batch=16,
            project=str(Path(__file__).parent / "runs"), name="playing_cards", exist_ok=True)
# best weights -> PlayingCardsDetection/runs/playing_cards/weights/best.pt
print(results.results_dict)
