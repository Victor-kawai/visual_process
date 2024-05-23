import pandas as pd 
import json
import datetime

'''
- 读取机构变更表
-- 生成：机构路径链字典 和 机构对象字典
- 读取机构静态表
-- 补全机构对象的静态信息
- 读取官职变更表
-- 生成：官职对象字典
- 读取官职静态表
-- 补全官职对象的静态信息
- 生成机构官职树
'''
# 控制截止时间
time = datetime.datetime.now().year


# 变更表表项插入
def institution_insert(institutions, row):
    institutions[row['现机构']] = {
        "type": "机构",
        "name": row['现机构'],
        "office": row['衙署'] if row['衙署']==row['衙署'] else "",
        "function": row['新职能'] if row['新职能']==row['新职能'] else "",
        "establishment": row['编制文本'] if row['编制文本']==row['编制文本'] else "",
        "other_names": [],
        "ref_pdf_page": "",
        "trace": "",
        "ref_book": "",
        "children_list": [],
        "children": [],
        "parents": row['新上级机构'].split("，") if row['新上级机构']==row['新上级机构'] else [],
        "start_time_old": row['开始-时间'] if row['开始-时间']==row['开始-时间'] else "",
        "end_time_old": "",
        "start_time_new": row["开始-公元年份"] if row["开始-公元年份"]==row["开始-公元年份"] else "",
        "end_time_new": ""
    }
    
def official_insert(officials, row):
    officials[row['现官职']] = {
        "type": row['类别'],
        "name": row['现官职'],
        "rank_text": row["官品文本"] if row["官品文本"]==row["官品文本"] else "",
        "rank": row["官品"] if row["官品"]==row["官品"] else "",
        "establishment": row["编制文本"] if row["编制文本"]==row["编制文本"] else "",
        "junior_officials": row['下级官员'] if row['下级官员']==row['下级官员'] else "",
        "peer_officials": row['平级官员'] if row['平级官员']==row['平级官员'] else "",
        "function": row['职掌'] if row['职掌']==row['职掌'] else "",
        "other_names": [],
        "ref_pdf_page": "",
        "trace": "",
        "ref_book": "",
        "parents": [],
        "start_time_old": row['开始-时间'] if row['开始-时间']==row['开始-时间'] else "",
        "end_time_old": "",
        "start_time_new": row["开始-公元年份"] if row["开始-公元年份"]==row["开始-公元年份"] else "",
        "end_time_new": ""
    }

# 读取机构变更表
org_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="机构变更表")

# 根据机构变更表生成 机构路径链 和 机构对象
institution_tag = {} # 上级机构链
institutions = {} # 机构对象
for index, row in org_table.iterrows():
    if row['公元年份'] > time: # 暂时只考虑截止到元丰改制的机构结构
        break
    if row['变更类型'] == '新增' or row['变更类型'] == '重启' or row['变更类型'] == '拆分': # 0-1
        institution_tag[row["现机构"]] = "" if row["新上级机构"]!=row["新上级机构"] else row["新上级机构"]
        institution_insert(institutions, row)
    elif row['变更类型'] == '变更' or row['变更类型'] == '移置': # 1-1
        # 原机构条目删除，新机构条目重新加入
        if row['原机构'] in institutions:
            institution_tag.pop(row['原机构'])
            institutions.pop(row['原机构'])
        institution_tag[row['现机构']] = "" if row["新上级机构"]!=row["新上级机构"] else row["新上级机构"]
        institution_insert(institutions, row)
    elif row['变更类型'] == '取消': # 1-0
        # 索引链中若有原机构存在，则删除
        if row['原机构'] in institutions:
            institution_tag.pop(row['原机构']) 
            institutions.pop(row['原机构'])
    elif row['变更类型'] == '合并' or row['变更类型'] == '并入': # n-1
        origin_institution = row['原机构'].split("，")
        for ins in origin_institution:
            if ins in institutions:
                institution_tag.pop(ins)
        institution_tag[row['现机构']] = "" if row["新上级机构"]!=row["新上级机构"] else row["新上级机构"]
        func = ""
        for ins in origin_institution:
            func += " | " + institutions[ins]['function']
            if ins in institutions:
                institutions.pop(ins)
        institution_insert(institutions, row)
        institutions[row['现机构']]['function'] += func
    elif row['变更类型'] == '打散': # 1-n
        if row['原机构'] in institutions:
            institution_tag.pop(row['原机构'])
            institutions.pop(row['原机构'])
        institution_tag[row['现机构']] = "" if row["新上级机构"]!=row["新上级机构"] else row["新上级机构"]
        institution_insert(institutions, row)
    else:
        print("Error: 未知的变更类型")
        break

# 读取机构静态表
org_info_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="机构静态表")
# 补全机构对象的静态信息
for index, row in org_info_table.iterrows():
    if row['机构名'] in institutions:
        institutions[row['机构名']]['type'] = row['类别']
        institutions[row['机构名']]['other_names'] = row['简称与别名'] if row['简称与别名']==row['简称与别名'] else ""
        institutions[row['机构名']]['ref_pdf_page'] = row['参考文档页数'] if row['参考文档页数']==row['参考文档页数'] else ""
        institutions[row['机构名']]['trace'] = row['职源与沿革文本'] if row['职源与沿革文本']==row['职源与沿革文本'] else ""
        institutions[row['机构名']]['ref_book'] = row['出处'] if row['出处']==row['出处'] else ""

# 读取官职变更表
job_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="官职变更表")

# 生成：官职对象字典——嵌入机构对象字典中
for index, row in job_table.iterrows():
    if row['公元年份'] > time:
        break
    if row['变更类型'] == '新增' or row['变更类型'] == '重启': # 0-1
        institution_tag[row["现官职"]] = ""
        official_insert(institutions, row)
    elif row['变更类型'] == '变更': # 1-1
        # 原机构条目删除，新机构条目重新加入
        if row['原官职'] in institutions:
            institution_tag.pop(row['原官职'])
            institutions.pop(row['原官职'])
        institution_tag[row['现官职']] = ""
        official_insert(institutions, row)
    elif row['变更类型'] == '取消': # 1-0
        # 索引链中若有原机构存在，则删除
        if row['原官职'] in institutions:
            institution_tag.pop(row['原官职']) 
            institutions.pop(row['原官职'])
    elif row['变更类型'] == '合并': # n-1
        origin_institution = row['原官职'].split("，")
        for ins in origin_institution:
            if ins in institutions:
                institution_tag.pop(ins)
        institution_tag[row['现官职']] = ""
        func = ""
        for ins in origin_institution:
            func += " | " + institutions[ins]['function']
            if ins in institutions:
                institutions.pop(ins)
        official_insert(institutions, row)
        institutions[row['现官职']]['function'] += func
    elif row['变更类型'] == '打散': # 1-n
        if row['原官职'] in institutions:
            institution_tag.pop(row['原官职'])
            institutions.pop(row['原官职'])
        institution_tag[row['现官职']] = ""
        official_insert(institutions, row)
    else:
        print("Error: 未知的变更类型")
        break

# 读取官职静态表
job_info_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="官职静态表")

# 补全官职对象的静态信息
for index, row in job_info_table.iterrows():
    if row['官职名'] in institutions:
        institutions[row['官职名']]['other_names'] = row['简称与别名'] if row['简称与别名']==row['简称与别名'] else ""
        institutions[row['官职名']]['ref_pdf_page'] = row['参考文档页数'] if row['参考文档页数']==row['参考文档页数'] else ""
        institutions[row['官职名']]['trace'] = row['职源与沿革文本'] if row['职源与沿革文本']==row['职源与沿革文本'] else ""
        institutions[row['官职名']]['ref_book'] = row['出处'] if row['出处']==row['出处'] else ""
        institutions[row['官职名']]['parents'] = row['隶属机构'].split("，") if row['隶属机构']==row['隶属机构'] else []
        institution_tag[row["官职名"]] = row['隶属机构'].split("，") if row['隶属机构']==row['隶属机构'] else ""

# 生成机构树
def build_json(instituitions):
    # 节点的子节点应该由其他节点的父节点决定
    for name, ins_info in instituitions.items():
        if ins_info['parents'] != []:
            for parent in ins_info['parents']:
                # print(parent, name, institution_tag[name]) # 检查表格用
                institutions[parent]['children_list'].append(name)
    root_name = "皇帝"
    def build_tree(node_name):
        node_info = institutions[node_name]
        if node_info['type'] == "机构":
            children_names = node_info['children_list']
            if len(children_names) > 0:
                node_info['children'] = [build_tree(name) for name in children_names]
        return node_info
    nested_tree = build_tree(root_name)
    return nested_tree
nested_tree_json = build_json(institutions)
json.dump(nested_tree_json, open("nested_tree.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
