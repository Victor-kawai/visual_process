'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-22 11:18:46
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-22 22:40:49
FilePath: \毕设\code\preprocess1.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from pdf2jpg import *
from cut_image import *
from format_change import *

'''
该脚本用于处理PDF到图片切割的自动化步骤：
1、将PDF转化为图片；
2、对图片进行切割；
3、对图片的表述格式进行转换。
最后的处理结果需要人工检查图片切分状况，需对切分不良的图片进行人工重新切分。
'''
if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = '元丰新制/测试/185-186测试.pdf'
    # 2、需要储存图片的目录
    imagePath = pdfPath[:pdfPath.rfind('.')]
    pyMuPDF_fitz(pdfPath, imagePath)
    cut_image_path = cut_image(imagePath)
    change_format(cut_image_path)
    print("\n处理结束，请对切分图片进行人工检查！")
