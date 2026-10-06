### Start Label Studio

From the repository root, start Label Studio with:

`docker compose -f Docker/compose.yaml up -d label-studio`

Open http://localhost:8080 to create or label image projects. Label Studio data is persisted in `mydata`.

### Train the card detector

Export labeled images from Label Studio in YOLO format and place the extracted dataset under `PlayingCardsDetection/dataset/archive`, with the `train/images`, `valid/images`, and `test/images` folders expected by `PlayingCardsDetection/data_config/playing_cards.yaml`.

Run training on demand from the repository root:

`docker compose -f Docker/compose.yaml --profile training run --rm trainer detect train model=yolov8n.pt data=data_config/playing_cards.yaml epochs=50 imgsz=640 project=runs name=playing_cards`

Training outputs are persisted in `PlayingCardsDetection/runs`. The first training run downloads the YOLO base weights if they are not cached.

Stop Label Studio with `docker compose -f Docker/compose.yaml down`.

The BlackjackAdvisor/live-feed service is not enabled by default; it can be added once card inference is implemented.

### Deploying your application to the cloud

First, build your image, e.g.: `docker build -t myapp .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t myapp .`.

Then, push it to your registry, e.g. `docker push myregistry.com/myapp`.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)