'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-22 14:09:41
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-23 17:44:04
FilePath: \毕设\code\paragraph_process.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
def paragraph_process(file_name):
    print("==== 换行处理开始 ====")
    f = open(file_name, 'r', encoding='utf-8')
    text = ""
    line = f.readline()
    first_line_flag = 0 # 第一行为0，否则都为1
    pre_line_flag = 0 # 前一行为标题行则为1，否则为0
    while line:
        line = line.replace('\n', '')
        if line[0] == '#':
            if first_line_flag == 0:
                text += line + "\n"
                first_line_flag = 1
            else:
                if pre_line_flag == 0:
                    text += "\n" + line + "\n"
                else:
                    text += line + "\n"
            pre_line_flag = 1
        else:
            if first_line_flag == 0:
                first_line_flag = 1
            text += line
            pre_line_flag = 0
        line = f.readline()
    g = open(file_name[:file_name.rfind(".")] + "处理后.md", 'w', encoding='utf-8')
    g.write(text)
    f.close()
    g.close()
    print("==== 换行处理完成 ====")

if __name__ == "__main__":
    filename = "元丰新制/测试/测试文本转换后.md"
    paragraph_process(filename)
