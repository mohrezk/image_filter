from ultralytics import YOLO
from ultralytics.utils.metrics import ConfusionMatrix
import cv2
import supervision as sv
from multiprocessing import Pool


class Classify:
    def __init__(self, folder_name):
        self.folder_name = folder_name

    def classify_image(self, image):

        # Load the model
        # model = YOLO("YOLOv8n.pt")
        # model = YOLO("YOLOv8x.pt")
        # model = YOLO("yolov8x-oiv7.pt")
        # model = YOLO("YOLOv8n-oiv7.pt")
        model = YOLO("yolov8m-oiv7.pt")
        # model = YOLO('yolov8x-cls.pt')
        
        
  
        # image = cv2.imread(image)
        # resized_image = cv2.resize(image, (640, 640))
            
        results = model.predict(source=image, save=True, project="media", name=f"{self.folder_name}")

        # conf_matrix = ConfusionMatrix(model.info)
        # print(conf_matrix.matrix())

        

        classes = results[0].boxes.cls
        names = []
        for name in classes:
            names.append(model.names[name.item()])

        return names

    # def classify_images(self, images):
    #     # model = YOLO("yolov8x-oiv7.pt")
    #     model = YOLO("yolov8m-oiv7.pt")
    #     # model = YOLO("yolov8n-oiv7.pt")
    #     # model = YOLO('yolov8x-cls.pt')
       

    #     # resized_images = []

    #     # for image in images:
    #     #     image = cv2.imread(image)
    #     #     resized_image = cv2.resize(image, (640, 640))
    #     #     resized_images.append(resized_image)
        
    #     results = model.predict(source=images)
    #     labels = []
    #     for result in results:
    #         classes = result.boxes.cls
    #         names = []
    #         for name in classes:
    #             names.append(model.names[name.item()])

    #         labels.append(names)

    #     return labels


    def classify_images(self, images):
        with Pool() as pool:
            result = pool.map(self.classify_image, images)

        print(result)
        return result