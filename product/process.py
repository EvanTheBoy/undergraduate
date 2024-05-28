import math

import cv2
import numpy as np

from product.number_conversion import binary_to_decimal, decimal_to_binary


def embed_secret_message(image, scale_factor, step, W):
    # Get the original image dimensions
    original_height, original_width = image.shape[:2]

    # Calculate the new dimensions after magnification
    new_height = int(original_height * scale_factor)
    new_width = int(original_width * scale_factor)

    # Resize the image using nearest-neighbor interpolation
    magnified_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_NEAREST)

    # 确保二者不会指向同一块内存区域, 也就是说对其中一个的修改不会影响另一个
    # cover_image = copy.deepcopy(magnified_image)
    cover_image = magnified_image.copy()

    # Create a two-dimensional array of the same size as the magnified image to mark information
    secret_array = np.zeros((new_height, new_width), dtype=np.uint8)

    d_max1 = pow(2, step)
    start = 0

    # 遍历图像第一排的边界像素
    for x in range(0, original_width):
        value = image[0, x][0]
        magnified_image[0, 2 * x + 1] = value
        magnified_image[1, 2 * x] = value
        magnified_image[1, 2 * x + 1] = value

    # 遍历图像第一竖列除了第一个像素之外的所有像素
    for y in range(1, original_height):
        value = image[y, 0][0]
        magnified_image[2 * y, 1] = value
        magnified_image[2 * y + 1, 0] = value
        magnified_image[2 * y + 1, 1] = value

    # 遍历最后一排除了第一个像素之外的所有像素
    for x in range(1, original_width):
        y = original_height - 1
        value = image[y, x][0]
        magnified_image[2 * y, 2 * x + 1] = value
        magnified_image[2 * y + 1, 2 * x] = value
        magnified_image[2 * y + 1, 2 * x + 1] = value

    # 遍历最后一列除了首尾两个像素之外的所有像素
    for y in range(1, original_height - 1):
        x = original_width - 1
        value = image[y, x][0]
        magnified_image[2 * y, 2 * x + 1] = value
        magnified_image[2 * y + 1, 2 * x] = value
        magnified_image[2 * y + 1, 2 * x + 1] = value

    # 对可以嵌入秘密信息的像素块进行操作
    for y in range(1, original_height - 1):
        for x in range(1, original_width - 1):
            mean_top_left = (image[y, x - 1][0] + image[y - 1, x][0]) >> 1
            mean_top_right = (image[y - 1, x][0] + image[y, x + 1][0]) >> 1
            mean_bottom_left = (image[y, x - 1][0] + image[y + 1, x][0]) >> 1
            mean_bottom_right = (image[y + 1, x][0] + image[y, x + 1][0]) >> 1

            mean1 = max(mean_top_right, mean_top_left)
            mean2 = max(mean1, mean_bottom_left)
            p_hat = max(mean2, mean_bottom_right)
            d_max2 = abs(image[y, x][0] - p_hat)
            # 这里的取最大值有待深入研究，这个d如果很大的话，会导致最终bC的值也很大，从而导致p1和p2全部溢出
            # 这样一来会导致无法往图片中嵌入任何信息，visited数组也没有值是1
            d = max(d_max1, d_max2)

            # 视情况修改 nS 的值
            nS = step
            # if d != 0:
            #     nS = math.floor(math.log(d, 2))
            secret_bits = W[start:start + nS]
            bC = binary_to_decimal(secret_bits)
            # 向上取整
            p1 = image[y, x][0] + math.ceil(bC / 2)
            # 向下取整
            p2 = image[y, x][0] - math.floor(bC / 2)
            if p1 > 255 or p2 < 0 or start >= len(W):
                # 不嵌入信息, 改为用原像素值填充
                value = image[y, x][0]
                magnified_image[2 * y, 2 * x + 1] = value
                magnified_image[2 * y + 1, 2 * x] = value
                magnified_image[2 * y + 1, 2 * x + 1] = value
            else:
                # 嵌入秘密信息
                # 在标记数组中进行标记, 表示这个位置嵌入了秘密信息
                secret_array[2 * y, 2 * x] = 1
                magnified_image[2 * y, 2 * x] = image[y, x][0]
                # print("右上角修改前: ", magnified_image[2 * y, 2 * x + 1])
                magnified_image[2 * y, 2 * x + 1] = p1
                # print("右上角修改后: ", magnified_image[2 * y, 2 * x + 1])
                magnified_image[2 * y + 1, 2 * x] = p2
                magnified_image[2 * y + 1, 2 * x + 1] = (p1 + p2) >> 1
                start += nS

    print(W)
    # print("处理前后图像等价吗: ", magnified_image == cover_image)
    return magnified_image, secret_array, cover_image


# 从图像中提取嵌入的秘密信息
def extract_secret_message(image, visited, length):
    W = []
    height, width = image.shape[:2]
    print(height, width)

    for y in range(2, height - 2):
        for x in range(2, width - 2):
            # 对于没有嵌入秘密信息的像素块, 直接跳过
            if visited[y][x] == 1:
                bC = image[y, x + 1][0] - image[y + 1, x][0]
                secret_bits = decimal_to_binary(bC, length)
                W.append(secret_bits)
            x += 1
        y += 1

    return ''.join(W)


def recover_image(image):
    height, width = image.shape[:2]
    original_image = cv2.resize(image, (int(width >> 1), int(height >> 1)), interpolation=cv2.INTER_NEAREST)
    return original_image
