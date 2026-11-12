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
    result = loadModel()(image, conf=confidence, imgsz=1280, verbose=False)[0]
    midpoint = image.shape[1] // 2
    playerCards = []
    dealerCards = []

    for (x, y, w, h), classId in zip(result.boxes.xywh.tolist(), result.boxes.cls.tolist()):
        name = result.names[int(classId)]
        side = playerCards if x < midpoint else dealerCards
        if name not in side:
            side.append(name)
    return playerCards, dealerCards, result.plot()

def detectCards(image, confidence=0.5):
    playerCards, dealerCards, _ = detectCardsLabeled(image, confidence)
    return playerCards, dealerCards
