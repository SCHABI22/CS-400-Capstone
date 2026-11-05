"""Export submitted Label Studio annotations into the YOLO dataset layout.

Writes dataset/archive/{train,valid,test}/{images,labels} as expected by
data_config/playing_cards.yaml. Class ids come from that yaml (matched by label
name), so they always line up with the model.

Usage (PowerShell, from the repo root):
    $env:LABEL_STUDIO_TOKEN = "<access token>"
    .venv\Scripts\python.exe PlayingCardsDetection\export_dataset.py [project_id]
"""
import os
import random
import shutil
import sys
from pathlib import Path

import requests
import yaml

HERE = Path(__file__).parent
DATA_YAML = HERE / "data_config" / "playing_cards.yaml"
OUT = HERE / "dataset" / "archive"
SPLITS = {"train": 0.7, "valid": 0.2, "test": 0.1}
# Sample images from the README; test_result.jpg has old predictions drawn on it.
EXCLUDE = ("test_result.jpg",)
LS_URL = os.environ.get("LABEL_STUDIO_URL", "http://localhost:8080")
MEDIA_DIR = HERE.parent / "mydata" / "media"


def make_session(token):
    s = requests.Session()
    if token.count(".") == 2:  # JWT refresh token
        r = requests.post(f"{LS_URL}/api/token/refresh", json={"refresh": token})
        r.raise_for_status()
        s.headers["Authorization"] = f"Bearer {r.json()['access']}"
    else:
        s.headers["Authorization"] = f"Token {token}"
    return s


def local_path(image_url):
    return MEDIA_DIR / image_url.split("/data/", 1)[1]


def main():
    token = os.environ.get("LABEL_STUDIO_TOKEN") or sys.exit("Set LABEL_STUDIO_TOKEN")
    project_id = sys.argv[1] if len(sys.argv) > 1 else "1"
    s = make_session(token)
    tasks = s.get(f"{LS_URL}/api/projects/{project_id}/export", params={"exportType": "JSON"}).json()
    class_ids = {name: int(i) for i, name in yaml.safe_load(open(DATA_YAML))["names"].items()}

    items = []
    for task in tasks:
        image = local_path(task["data"]["image"])
        anns = [a for a in task["annotations"] if not a.get("was_cancelled")]
        if not anns or image.name.endswith(EXCLUDE):
            print(f"skip task {task['id']}: {image.name}")
            continue
        ann = max(anns, key=lambda a: a["updated_at"])  # latest submission
        lines = []
        for r in ann["result"]:
            if r.get("type") != "rectanglelabels":
                continue
            v = r["value"]
            x, y, w, h = v["x"] / 100, v["y"] / 100, v["width"] / 100, v["height"] / 100
            if v.get("rotation"):
                print(f"WARNING task {task['id']}: rotated box exported unrotated")
            lines.append(f"{class_ids[v['rectanglelabels'][0]]} {x + w / 2:.6f} {y + h / 2:.6f} {w:.6f} {h:.6f}")
        items.append((image, lines))

    random.Random(0).shuffle(items)
    if OUT.exists() and any(OUT.iterdir()):
        sys.exit(f"{OUT} already exists; move or delete it first, then re-run")
    start = 0
    for i, (split, frac) in enumerate(SPLITS.items()):
        end = len(items) if i == len(SPLITS) - 1 else start + round(frac * len(items))
        (OUT / split / "images").mkdir(parents=True)
        (OUT / split / "labels").mkdir(parents=True)
        for image, lines in items[start:end]:
            shutil.copy2(image, OUT / split / "images" / image.name)
            (OUT / split / "labels" / f"{image.stem}.txt").write_text("\n".join(lines))
        boxes = sum(len(l) for _, l in items[start:end])
        print(f"{split}: {end - start} images, {boxes} boxes")
        start = end


if __name__ == "__main__":
    main()
