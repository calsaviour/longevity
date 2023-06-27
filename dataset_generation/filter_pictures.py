import os
import glob
import cv2

if __name__ == '__main__': 
    paths = glob.glob("dataset/*.jpg")
    for p in paths:
        if cv2.imread(p) is None:
            print("remove {}".format(p))
            os.remove(p)

