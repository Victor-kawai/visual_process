'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-09 00:42:07
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-09 21:54:29
FilePath: \毕设\code\page_count.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import re
from gpt import *
import pandas as pd


# 计算页数
# 逻辑：找到所有page{数字L}和page{数字R}条目，提取其中数字部分，去重后计数
def count_page(text):
    pattern = re.compile(r"page{\d+[LR]}")
    pages = pattern.findall(text)
    page_set = set()
    for page in pages:
        page_set.add(page[page.find("{")+1:page.find("}")-1])
    return len(page_set)

def count_entry(text):
    pattern = re.compile(r"\n### .+\n")
    return len(pattern.findall(text))

def entry_detail(text, g):
    pattern = re.compile(r'\n(### .+?\n.+?)[，。]', re.DOTALL)
    entries = pattern.findall(text)
    prompt = "请你帮我判断一下这段文字中的条目（文字中第一部分是名字第二部分是类别说明）说的是机构还是官职，如果是机构请回答1，如果是官职请回答2：\n“{Content}”"
    ins_count, off_count, non_count = 0, 0, 0
    tags = []
    for entry in entries:
        content = entry
        response = get_response("gpt-4", prompt.format(Content=content)).choices[0].message.content
        print(content)
        print(response)
        if "1" in response:
            print("机构")
            tags.append(1)
            g.write(entry)
            g.write("\n")
            g.write("机构\n")
            ins_count += 1
        elif "2" in response:
            print("官职")
            tags.append(2)
            g.write(entry)
            g.write("\n")
            g.write("官职\n")
            off_count += 1
        else:
            print("未知")
            tags.append(response)
            g.write(entry)
            g.write("\n")
            g.write("未知\n")
            non_count += 1
    print("条目数量：", entries)
    print("机构数量：", ins_count)
    print("官职数量：", off_count)
    print("未知数量：", non_count)
    pd.DataFrame({'文本': entries, "标记": tags}).to_csv("tags.csv", index=False, encoding="utf-8")

if __name__ == "__main__":
    text_file = "原文.md"
    f = open(text_file, "r", encoding="utf-8")
    g = open("tags.txt", "w", encoding="utf-8")
    text = f.read()
    page_count = count_page(text)
    print("Pages: ", page_count)
    entry_count = count_entry(text)
    print("Entries: ", entry_count)
    entry_detail(text, g)
    f.close()
    g.close()