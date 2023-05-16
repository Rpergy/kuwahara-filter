import cv2 as cv
import numpy as np
import math
import time

def kuwahara(photo, KERNEL):
    resolution = [len(photo[0]), len(photo)]
    newPhoto = np.empty_like(photo)

    for y in range(math.ceil(KERNEL/2), resolution[1] - math.ceil(KERNEL/2), 1):
        for x in range(math.ceil(KERNEL/2), resolution[0] - math.ceil(KERNEL/2), 1):
            quad_size = math.ceil(KERNEL/2)
            for channel in range(3):
                Q1 = photo[y - quad_size:y + 1, x - quad_size:x + 1, channel]
                Q2 = photo[y - quad_size:y + 1, x + 1:x + quad_size, channel]
                Q3 = photo[y + 1:y + quad_size, x - quad_size:x + 1, channel]
                Q4 = photo[y + 1:y + quad_size, x + 1:x + quad_size, channel]

                Q1std = np.std(Q1)
                Q2std = np.std(Q2)
                Q3std = np.std(Q3)
                Q4std = np.std(Q4)

                stds = [Q1std, Q2std, Q3std, Q4std]
                if min(stds) == Q1std:
                    newPhoto[y, x, channel] = np.mean(Q1)
                elif min(stds) == Q2std:
                    newPhoto[y, x, channel] = np.mean(Q2)
                elif min(stds) == Q3std:
                    newPhoto[y, x, channel] = np.mean(Q3)
                elif min(stds) == Q4std:
                    newPhoto[y, x, channel] = np.mean(Q4)
        print(f"row {y} completed ({(y/(resolution[1] - math.ceil(KERNEL/2)) * 100):.2f}%)")
    
    return newPhoto

start_time = time.time()

photo = cv.cvtColor(cv.imread("canyon.jpg"), cv.COLOR_BGR2HSV)
kuwaharaPhoto = kuwahara(cv.resize(photo, (756, 1008)), 7)

print("--- %s minutes ---" % ((time.time() - start_time) / 60))
cv.imwrite("canyon3.jpg", cv.cvtColor(kuwaharaPhoto, cv.COLOR_HSV2BGR))
