import cv2
import matplotlib.pyplot as plt

from product.generate_string import generate_binary_string
from product.process import embed_secret_message, extract_secret_message, recover_image
from product.calculation import calculate_psnr, calculate_ssim

if __name__ == '__main__':
    # 加载图像
    original_image = cv2.imread('Lena.png')

    # 放大倍数
    magnification_factor = 2.0

    # 长度
    length = 10
    secret_message = generate_binary_string(length)

    step = 5

    # 主函数核心逻辑
    # embedded_image, array, magnified_image = embed_secret_message(original_image, magnification_factor,
    #                                                               step, secret_message)
    # secret_information = extract_secret_message(embedded_image, array, step)
    embedded_image, array, magnified_image, length_map = embed_secret_message(original_image, magnification_factor,
                                                                  step, secret_message)
    secret_information = extract_secret_message(embedded_image, array, length_map)
    print(len(secret_information))
    print(secret_information == secret_message)
    print("----------------")
    print(secret_information)
    recovered_image = recover_image(embedded_image)

    # 测试
    psnr = calculate_psnr(embedded_image, magnified_image)
    print('PSNR: {:.2f}'.format(psnr))

    ssim = calculate_ssim(embedded_image, magnified_image)
    print('SSIM: {:.4f}'.format(ssim))

    # 展示结果
    plt.figure(figsize=(8, 6))
    plt.subplot(121)
    plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(cv2.cvtColor(embedded_image, cv2.COLOR_BGR2RGB))
    plt.title('Data Embedded Image')
    plt.axis('off')

    # plt.subplot(122)
    # plt.imshow(cv2.cvtColor(recovered_image, cv2.COLOR_BGR2RGB))
    # plt.title('Recovered Image')
    # plt.axis('off')

    plt.tight_layout()
    plt.show()
