'''
Author: Victor-kawai 1900017878@pku.edu.cn
Date: 2024-05-22 11:40:23
LastEditors: Victor-kawai 1900017878@pku.edu.cn
LastEditTime: 2024-05-23 19:46:12
FilePath: \毕设\code\preprocess2.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from ocr_api import *
from trans_format import *

# 字段：官品 编制 简称 职源 职掌
replace_dict = {"简称与别名": ["简称"],
                "简称与别称": ["简称"],
                "官品、编制、简称与别名": ["官品", "编制", "简称"],
                "简称与追改": ["简称"],
                "简称与旧称": ["简称"],
                "职源与沿革": ["职源"], 
                "职源与改革": ["职源"],
                "职源与沿革、职掌、官品": ["职源", "职掌", "官品"], 
                "职掌与沿革": ["职掌", "职源"],
                "职源、职掌、编制": ["职源", "职掌", "编制"], 
                "职掌、官品、编制": ["职掌", "官品", "编制"],
                "职源、职掌、官品、编制": ["职源", "职掌", "官品", "编制"], 
                "职源、职掌、官品": ["职源", "职掌", "官品"],
                "职源、职掌": ["职源", "职掌"],
                "职掌、品位": ["职掌", "官品"], 
                "职掌": ["职掌"],
                "职能": ["职掌"],
                "编制与品位": ["编制", "官品"], 
                "位遇": ["官品"],
                "序位": ["官品"], 
                "地位": ["官品"],
                "品秩": ["官品"],
                "编制": ["编制"],
                "职源": ["职源"], 
                "简称": ["简称"], 
                "通称": ["简称"], 
                "省称": ["简称"], 
                "别名": ["简称"], 
                "别称": ["简称"], 
                "合称": ["简称"],
                "官品": ["官品"], 
                "品位": ["官品"]}
if __name__ == "__main__":
    organization = "测试"
    text_file_path = ocr_request(organization)
    print(replace_dict)
    md_format_change2(text_file_path, replace_dict)
    print("\n 处理结束，请人工检查文本内容！")