import cv2
import os

def binarize_image(path, out_name, folder='BW_Record/'):
    originalImage = cv2.imread(path)
    grayImage = cv2.cvtColor(originalImage, cv2.COLOR_BGR2GRAY)

    (thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 200, 255, cv2.THRESH_BINARY)

    '''cv2.imshow('Black white image', blackAndWhiteImage)
    cv2.imshow('Original image', originalImage)
    cv2.imshow('Gray image', grayImage)'''
    cv2.imwrite(folder + out_name, blackAndWhiteImage)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

PATH = 'ECG_Record/'
images = os.listdir(PATH)
for image in images:
    binarize_image(PATH+image, image)