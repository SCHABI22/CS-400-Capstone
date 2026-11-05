from pathlib import Path
from ultralytics import YOLO

WEIGHTS = Path(__file__).parent / "runs" / "playing_cards" / "weights" / "best.pt"
_model = None

def loadModel():
    global _model
    if _model is None:
        if not WEIGHTS.exists():
            raise FileNotFoundError(f"Weight file not found: {WEIGHTS}")
        _model = YOLO(str(WEIGHTS))
    return _model

def detectCardsLabeled(image, confidence=0.5):
    result = loadModel()(image, conf=confidence, verbose=False)[0]
    cards = []
    for classId in result.boxes.cls.tolist():
        name = result.names[int(classId)]
        if name not in cards:
            cards.append(name)
    return cards, result.plot()

def detectCards(image, confidence=0.5):
    return detectCardsLabeled(image, confidence)[0]