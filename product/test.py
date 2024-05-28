import cv2
import numpy as np

from product.generate_string import generate_binary_string
from product.magnification import embed_secret_message


# W = ["101"]
# print(W)
# W.append("010")
# print(W)
# W.append("011")
# print(W)
# combined_string = ''.join(W)
# print(combined_string)

# original_image = cv2.imread('lena1.png')
# original_height, original_width = original_image.shape[:2]
# modified_image = np.zeros((original_height, original_width), dtype=np.uint8)
# a = np.floor((original_image[1, 0] + original_image[0, 1]) / 2)
# print(original_image[1,0][0])
# print(original_image[1,0][1])
# print(original_image[1,0])
# print(original_image[1,1])
# print(original_image[23, 25])
# print(original_image[123, 12])
# print(modified_image[123, 12])
# print(modified_image[1, 271])
# modified_image[1, 271] = 12
# print(modified_image[1, 271])
# print(original_image[1, 271])
# print(original_image[1, 270])
# print(a)
# print(a[0])
# print(a[1])
