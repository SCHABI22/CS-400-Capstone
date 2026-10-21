from ultralytics import YOLO

# Load a model
model = YOLO("yolov8n.yaml")  # build a new model from scratch
# model = YOLO("./yolov8s_playing_cards.pt")  # load a pretrained model (recommended for training)

# Added, used for training 
'''model.save("yolov8n_playing_cards_initial.pt")  # Optional: save the untrained checkpoint

model.train(
    data="data_config/playing_cards.yaml",
    epochs=50,
    imgsz=640,
    batch=16,
    project="runs/playing_cards",
    name="yolov8n_scratch",
)'''

# Use the model
results = model.train(data="PlayingCardsDetection/data_config/playing_cards.yaml", epochs=3)  # train the model
# results = model.val()  # evaluate model performance on the validation set
#results = model("./assets/test.jpg")  # predict on an image
# success = YOLO("yolov8n.pt").export(format="onnx")  # export a model to ONNX format
print([x for x in results])
print("End Run")