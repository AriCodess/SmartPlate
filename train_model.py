from ultralytics import YOLO

def train_custom_model():
    # 1. Load the pre-trained model (starting point)
    model = YOLO('yolov8n.pt') 

    # 2. Train the model on your custom data
    # epochs=20: How many times it sees the data (increase to 50 for better accuracy)
    # imgsz=640: Image size
    model.train(
        data='dataset/food_dataset/data.yaml',
        epochs=30,
        imgsz=640,
        plots=True
    )

if __name__ == '__main__':
    train_custom_model()