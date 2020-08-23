import cv2
import numpy as np
import core.utils as utils
import tensorflow as tf
from core.yolov3 import YOLOv3, decode
from core.config import cfg
import time
from PIL import Image


class Detection:
    ''' 使用时, 通过 Detection.get_instance() 获取实例.
    在程序初始化时, 调用 Detection.get_instance().init() 来载入模型,
    以提高第一次的识别速度.
    '''
    detection = None

    @classmethod
    def get_instance(cls):
        if cls.detection:
            return cls.detection
        else:
            cls.detection = Detection()
            return cls.detection

    def __init__(self):
        self.input_size = 416
        self.inited = False
        self.cnt = 0
        self.img_path = './cv_test1.jpg'  # 默认测试图片路径

    def init(self):
        if self.inited:
            return
        self.inited = True
        input_layer = tf.keras.layers.Input(
            [self.input_size, self.input_size, 3])
        feature_maps = YOLOv3(input_layer)

        bbox_tensors = []
        for i, fm in enumerate(feature_maps):
            bbox_tensor = decode(fm, i)
            bbox_tensors.append(bbox_tensor)

        self.model = tf.keras.Model(input_layer, bbox_tensors)
        self.model.load_weights('./yolov3')
        self.model.summary()

    def get_commodities(self):
        if not self.inited:
            print("Warning: Detection instance has not been "
                  "initialized and is initializing now. "
                  "This will cause low performance")
        original_image = self._read_img()  # TODO: get a frame from camera
        original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
        original_image_size = original_image.shape[:2]
        image_data = utils.image_preporcess(
            np.copy(original_image),
            [self.input_size, self.input_size])
        image_data = image_data[np.newaxis, ...].astype(np.float32)

        prev_time = time.time()
        pred_bbox = self.model.predict_on_batch(image_data)
        curr_time = time.time()
        self.exec_time = curr_time - prev_time

        pred_bbox = [tf.reshape(x, (-1, tf.shape(x)[-1])) for x in pred_bbox]
        pred_bbox = tf.concat(pred_bbox, axis=0)
        bboxes = utils.postprocess_boxes(pred_bbox, original_image_size, self.input_size, 0.3)
        bboxes = utils.nms(bboxes, 0.45, method='nms')
        image = utils.draw_bbox(original_image, bboxes)
        image = Image.fromarray(image)
        image.save(str(self.cnt) + 'test.jpg')
        self.cnt += 1

        return self._get_commodities_from_bboxes(bboxes)


    def _read_img(self):
        return cv2.imread(self.img_path)

    @staticmethod
    def _get_commodities_from_bboxes(bboxes):
        classes: dict = utils.read_class_names(cfg.YOLO.CLASSES)
        result: dict = {}

        for bbox in bboxes:
            class_ind = int(bbox[5])
            class_name = classes[class_ind]
            result[class_name] = result.get(class_name, 0) + 1

        return result



if __name__ == '__main__':
    dection = Detection.get_instance()
    dection.init()
    dection.img_path = './cv_test3.jpg'
    print(dection.get_commodities(), dection.exec_time)
    dection.img_path = './cv_test2.jpg'
    print(dection.get_commodities(), dection.exec_time)
    dection.img_path = './cv_test1.jpg'
    print(dection.get_commodities(), dection.exec_time)
    pass
