'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-23 16:15:16
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-23 23:12:08
FilePath: \毕设\code\text2table_static.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
import pandas as pd 
import re 
import time
from preprocess2 import replace_dict

# 类别	条目名	衙署	下级机构	上级机构	隶属机构	下级官员	平级官员	官品文本	官品	编制文本	编制	编制人数	职掌文本	职掌	简称与别名	参考文档页数	职源与沿革文本	出处	始置时间	罢置时间	前身
def data_extract(replace_dict, text_file_name):
    f = open(text_file_name, "r", encoding="utf-8")
    attribute_dict = {"官品": "", "编制": "", "简称": "", "职源": "",  "职掌": "", "参考文档页数": ""}
    entity_dict = {}
    page = "" # 页数
    entity = "" # 条目
    table_name = "" # 大类名
    attribute = [] # 属性名
    text = f.readline()
    while text:
        if text.startswith("#### "):
            attribute = text[5:].replace("\n", "").replace(" ", "")
        elif text.startswith("### "):
            entity = text[4:].replace("\n", "")
            entity_dict[entity] = attribute_dict.copy()
            entity_dict[entity]["参考文档页数"] += "宋代官制辞典第"+page+"页，"
            attribute = []
        elif text.startswith("## "):
            page = text[text.find("{")+1:text.find("}")-1].replace("\n", "")
            if entity != "":
                if page not in entity_dict[entity]["参考文档页数"]:
                    entity_dict[entity]["参考文档页数"] += "宋代官制辞典第"+page+"页，"
        elif text.startswith("# "):
            table_name = text[2:].replace("\n", "")
            attribute = []
        else:
            if len(attribute) != 0:
                for key in replace_dict[attribute]:
                    entity_dict[entity][key] += text
        text = f.readline()
    print(entity_dict)
    # 类别	条目名	衙署	下级机构	上级机构	隶属机构	下级官员	平级官员	官品文本	官品	编制文本	编制	编制人数	职掌文本	职掌	简称与别名	参考文档页数	职源与沿革文本	出处	始置时间	罢置时间	前身
    leibie, tiaomuming, yashu, xiajijigou, shangjigou, lishujigou, xiajiguan, pingjiguan, guanpinwenben, guanpin, bianzhiwenben, bianzhi, bianzhirensu, zhizhangwenben, zhizhang, jiancheng, cankao, zhuyuanyuanyan, chuchu, shizhitime, bazhitime, qianshen = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
    for key, value in entity_dict.items():
        tiaomuming.append(key)
        guanpinwenben.append(value["官品"])
        bianzhiwenben.append(value["编制"])
        zhizhangwenben.append(value["职掌"])
        jiancheng.append(value["简称"])
        cankao.append(value["参考文档页数"])
        zhuyuanyuanyan.append(value["职源"])
    leibie = [""] * len(tiaomuming)
    yashu = [""] * len(tiaomuming)
    xiajijigou = [""] * len(tiaomuming)
    shangjigou = [""] * len(tiaomuming)
    lishujigou = [""] * len(tiaomuming)
    xiajiguan = [""] * len(tiaomuming)
    pingjiguan = [""] * len(tiaomuming)
    guanpin = [""] * len(tiaomuming)
    bianzhi = [""] * len(tiaomuming)
    bianzhirensu = [""] * len(tiaomuming)
    zhizhang = [""] * len(tiaomuming)
    chuchu = [""] * len(tiaomuming)
    shizhitime = [""] * len(tiaomuming)
    bazhitime = [""] * len(tiaomuming)
    qianshen = [""] * len(tiaomuming)
    tb = pd.DataFrame(
        {
            "类别": leibie,
            "条目名": tiaomuming,
            "衙署": yashu,
            "下级机构": xiajijigou,
            "上级机构": shangjigou,
            "隶属机构": lishujigou,
            "下级官员": xiajiguan,
            "平级官员": pingjiguan,
            "官品文本": guanpinwenben,
            "官品": guanpin,
            "编制文本": bianzhiwenben,
            "编制": bianzhi,
            "编制人数": bianzhirensu,
            "职掌文本": zhizhangwenben,
            "职掌": zhizhang,
            "简称与别名": jiancheng,
            "参考文档页数": cankao,
            "职源与沿革文本": zhuyuanyuanyan,
            "出处": chuchu,
            "始置时间": shizhitime,
            "罢置时间": bazhitime,
            "前身": qianshen
        }
    )
    tb.to_csv(text_file_name[:text_file_name.rfind('/')+1]+table_name+".csv", encoding="utf_8_sig", index=False)
    f.close()

if __name__ == "__main__":
    text_file = "元丰新制/测试/测试文本转换后处理后.md"
    data_extract(replace_dict, text_file)
