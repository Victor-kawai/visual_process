'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-03-28 23:50:13
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-22 11:27:46
FilePath: \毕设\代码\cut_image.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

# 代码链接：https://blog.csdn.net/welkin_ring/article/details/120634490
from PIL import Image
import os

path = '元丰新制/测试/185-186测试'   #文件目录
def cut_image(path):
    print("==== 图片切分开始 ====")
    #path这个目录处理完之后需要手动更改
    new_path = path[:path.rfind('/')+1]+'切分后'+path[path.find('/')+1:path.rfind('/')]
    print(new_path)
    if  os.path.exists(new_path):
        print("目录存在")
    else:
        os.mkdir(new_path)
        path_list = os.listdir(path)
        #path_list.remove('.DS_Store')   #macos中的文件管理文件，默认隐藏，这里可以忽略，如果是mac可能需要加回这行（笔者没有用过mac）
        print(path_list)

        for i in path_list: #截左半张图片
            a = open(os.path.join(path,i),'rb')
            img = Image.open(a)
            w = img.width       #图片的宽
            h = img.height      #图片的高
            print('正在处理图片',i,'宽',w,'长',h)
        
            box = (0,0,w*0.5,h) #box元组内分别是 所处理图片中想要截取的部分的 左上角和右下角的坐标
            img = img.crop(box)
            print('正在截取左半张图...')
            img.save(new_path+'/L'+i) #这里需要对截出的图加一个字母进行标识，防止名称相同导致覆盖
            print('L-',i,'保存成功')
            a.close()

        for i in path_list: #截取右半张图片
            a = open(os.path.join(path,i),'rb')
            img = Image.open(a)
            w = img.width       #图片的宽
            h = img.height      #图片的高
            print('正在处理图片',i,'宽',w,'长',h)

            box = (w*0.5,0,w,h)
            img = img.crop(box)
            print('正在截取右半张图...')
            img.save(new_path+'/R'+i)
            print('R-',i,'保存成功')
            a.close()
        
        print("'{}'目录下所有图片已经保存到本文件目录下。".format(path))
        print("==== 图片切分结束 ====")
        return new_path

if __name__ == "__main__":
    p = cut_image(path)
    print(p)




