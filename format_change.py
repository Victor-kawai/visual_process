'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-04-03 01:39:28
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-22 11:26:21
FilePath: \毕设\code\format_change.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import os

# 输入文件夹地址
path = "元丰新制/测试/切分后测试"

# 获取旧名和新名
def change_format(path):
    print("==== 文件名修改开始 ====")
    files = os.listdir(path)
    # 输出所有文件名，只是为了看一下
    for file in files:
        print(file)
    i = 0
    for file in files:
        # old 旧名称的信息
        old = path + '/' + files[i]
        print(old)
        # new 新名称的信息
        new = path + '/' + files[i][1:files[i].rfind('.')] + files[i][0] + files[i][files[i].rfind('.'):]
        print(new)
        # 新旧替换
        os.rename(old,new)
        i+=1
    print("==== 文件名修改结束 ====")

if __name__ == "__main__":
    change_format(path)