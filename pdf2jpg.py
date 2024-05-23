'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-22 10:22:54
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-23 18:07:03
FilePath: \毕设\code\pdf2jpg.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import datetime
import os
import fitz  # fitz就是pip install PyMuPDF


def pyMuPDF_fitz(pdfPath, imagePath):
    print("==== pdf2img开始 ====")
    start_page = pdfPath[pdfPath.rfind('/') + 1 : pdfPath.rfind('-')]
    print("起始页数：", start_page)
    print("imagePath=" + imagePath)
    pdfDoc = fitz.open(pdfPath)
    for pg in range(pdfDoc.page_count):
        page = pdfDoc[pg]
        rotate = int(0)
        # 每个尺寸的缩放系数为1.3，这将为我们生成分辨率提高2.6的图像。
        # 此处若是不做设置，默认图片大小为：792X612, dpi=96
        zoom_x = 3  # (1.33333333-->1056x816)   (2-->1584x1224)
        zoom_y = 3
        mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
        pix = page.get_pixmap(matrix=mat, alpha=False)

        if not os.path.exists(imagePath):  # 判断存放图片的文件夹是否存在
            os.makedirs(imagePath)  # 若图片文件夹不存在就创建

        pix.save(imagePath + '/' + '%s.png' % (int(start_page)+pg))  # 将图片写入指定的文件夹内
    print('==== pdf2img结束 ====')


if __name__ == "__main__":
    # 1、PDF地址
    pdfPath = '元丰新制/测试/185-186测试.pdf'
    # 2、需要储存图片的目录
    imagePath = '元丰新制/测试/185-186测试'
    pyMuPDF_fitz(pdfPath, imagePath)

