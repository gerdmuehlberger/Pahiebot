import cv2
import tensorflow as tf
from google.protobuf import text_format
import matplotlib.pyplot as plt
from google.transit import gtfs_realtime_pb2
import urllib.request

class SSD_Mobilenet_v3:
    def __init__(self):
        pass

        
    def runModel(self):
        config_file = './setup/SSD_Mobilenet_v3/ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        frozen_model = './setup/SSD_Mobilenet_v3/frozen_inference_graph.pb'
        labels = './setup/SSD_Mobilenet_v3/labels.txt'

        model = cv2.dnn_DetectionModel(frozen_model, config_file)
        model.setInputSize(320, 320)
        model.setInputScale(1.0/127.5)
        model.setInputMean((127.5, 127.5,127.5))
        model.setInputSwapRB(True)

        classLabels = []
        with open(labels, 'rt') as fpt:
            classLabels = fpt.read().rstrip('\n').split('\n')

        img = cv2.imread('./setup/SSD_Mobilenet_v3/img/temp.png')

        ClassIndex, confidence, bbox = model.detect(img, confThreshold=0.55)

        font_scale = 2
        font = cv2.FONT_HERSHEY_PLAIN
        for ClassInd, conf, boxes in zip(ClassIndex.flatten(), confidence.flatten(), bbox):
            cv2.rectangle(img, boxes, (255, 0, 0), 6)
            cv2.putText(img, classLabels[ClassInd - 1], (boxes[0] + 10, boxes[1] + 40), font, fontScale=font_scale,
                        color=(0, 255, 0), thickness=3)

        plt.figure(figsize=(30, 30))
        plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        plt.savefig('./setup/SSD_Mobilenet_v3/img/sf.png')