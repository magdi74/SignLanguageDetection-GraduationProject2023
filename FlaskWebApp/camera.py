import cv2 
from hands import HandDetector
from PIL import Image
import tensorflow as tf
import numpy as np
import time
import math
import os
from tensorflow.keras.models import load_model
from keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as plt
from tensorflow.keras.preprocessing.image import ImageDataGenerator , img_to_array, load_img
from tensorflow.keras.optimizers import RMSprop

dic = ['drink',
 'food',
 'full',
 'have',
 'hello',
 'i',
 'i love you',
 'police',
 'prefer',
 'shirt',
 'telephone',
 'water',
 'wrong',
 'yes',
 'you']


offset = 10
imgSize = 350
frame_rate = 5
counter = 0
result = 0
detector = HandDetector(maxHands=1)
model = load_model("./models/VGG16_Augmented1.h5")

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()
    
    def get_frame_original(self):
        ret, img = self.video.read()
        ret, jpeg = cv2.imencode('.jpg',img)
        return jpeg.tobytes()

    def get_frame(self, time_elapsed):
        ret, img = self.video.read()
        imgOutput = img.copy()

        #Here we will manipulate the frame to pass it to the model
        hands, img = detector.findHands(img)

        if hands:

            hand = hands[0]
            x, y, w, h = hand['bbox']

            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
            imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

            imgCropShape = imgCrop.shape

            aspectRatio = h / w

            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            imgWhiteCopy = imgWhite.copy()
            imgWhite = img_to_array(imgWhite)
            imgWhite = imgWhite.reshape((1, imgWhite.shape[0], imgWhite.shape[1], imgWhite.shape[2]))
            imgWhite = preprocess_input(imgWhite)
            if time_elapsed > 1./frame_rate:
                prev = time.time()
                result = model.predict(imgWhite)
                word = dic[result.argmax()]
                oldWord = word
                result = result * 100000000
                maxVal = (result[0].max()/sum(result[0])) * 100
                if(maxVal > 99.9999999):
                    cv2.putText(imgOutput, dic[result.argmax()],(x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
                    # cv2.imshow(f"ImageCrop", imgCrop)
                else:
                    cv2.putText(imgOutput, "",(x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)
                    # cv2.imshow(f"ImageCrop", imgCrop)
            else:
                cv2.putText(imgOutput, word,(x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)

            result = model.predict(imgWhite)

            cv2.rectangle(imgOutput, (x-offset, y-offset),
                          (x + w+offset, y + h+offset), (255, 0, 255), 4)
            

            cv2.putText(imgOutput, dic[result.argmax()],(x,y-20), cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)           
            # cv2.imshow(f"ImageCrop", imgCrop)
            # cv2.imshow(f"imgWhite", imgWhiteCopy)


        ret, jpeg = cv2.imencode('.jpg',imgOutput)
        return jpeg.tobytes()


        # try:

        #     #Here we will manipulate the frame to pass it to the model
        #     hands, img = detector.findHands(img)

        #     if hands:

        #         hand = hands[0]
        #         x, y, w, h = hand['bbox']

        #         imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        #         imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        #         imgCropShape = imgCrop.shape

        #         aspectRatio = h / w

        #         if aspectRatio > 1:
        #             k = imgSize / h
        #             wCal = math.ceil(k * w)
        #             imgResize = cv2.resize(imgCrop, (wCal, imgSize))
        #             imgResizeShape = imgResize.shape
        #             wGap = math.ceil((imgSize - wCal) / 2)
        #             imgWhite[:, wGap:wCal + wGap] = imgResize
        #         else:
        #             k = imgSize / w
        #             hCal = math.ceil(k * h)
        #             imgResize = cv2.resize(imgCrop, (imgSize, hCal))
        #             imgResizeShape = imgResize.shape
        #             hGap = math.ceil((imgSize - hCal) / 2)
        #             imgWhite[hGap:hCal + hGap, :] = imgResize

        #         imgWhiteCopy = imgWhite.copy()
        #         imgWhite = img_to_array(imgWhite)
        #         imgWhite = imgWhite.reshape((1, imgWhite.shape[0], imgWhite.shape[1], imgWhite.shape[2]))
        #         imgWhite = preprocess_input(imgWhite)

        #         result = model.predict(imgWhite)

        #         cv2.rectangle(imgOutput, (x-offset, y-offset),
        #                     (x + w+offset, y + h+offset), (255, 0, 255), 4)
        

        #         cv2.putText(imgOutput, dic[result.argmax()], cv2.FONT_HERSHEY_COMPLEX,2,(255,0,255),2)             
        #         cv2.imshow(f"ImageCrop", imgCrop)
        #         cv2.imshow(f"imgWhite", imgWhiteCopy)


        #     ret, jpeg = cv2.imencode('.jpg',imgOutput)
        #     return jpeg.tobytes()

        # except:
        #     ret, jpeg = cv2.imencode('.jpg', img)
        #     return jpeg.tobytes()
