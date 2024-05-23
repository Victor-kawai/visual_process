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


# 机构变更表表项插入
def institution_insert(institution_tag, institutions, row):
    if row["现机构"] not in institutions:
        institution_tag[row["现机构"]] = {}
        institutions[row["现机构"]] = {}
    (institution_tag[row["现机构"]])[row['开始-公元年份']] = "" if row["新上级机构"]!=row["新上级机构"] else row["新上级机构"]
    (institutions[row['现机构']])[row['开始-公元年份']] = {
        "name": row['现机构'],
        "type": "机构",
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
        "start_time_old": row['时间'] if row['时间']==row['时间'] else "",
        "end_time_old": "",
        "start_time_new": row["公元年份"] if row["公元年份"]==row["公元年份"] else "",
        "end_time_new": ""
    }
    
# 官职变更表表项插入
def official_insert(institution_tag, officials, row):
    if row["现官职"] not in officials:
        institution_tag[row["现官职"]] = {}
        officials[row["现官职"]] = {}
    (institution_tag[row["现官职"]])[row['开始-公元年份']] = ""
    (officials[row['现官职']])[row['开始-公元年份']] = {
        "name": row['现官职'],
        "type": row['类别'],
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
        "start_time_old": row['时间'] if row['时间']==row['时间'] else "",
        "end_time_old": "",
        "start_time_new": row["公元年份"] if row["公元年份"]==row["公元年份"] else "",
        "end_time_new": ""
    }

# 机构对象添加结束时间
def add_end_time(institutions, name, old_time, new_time):
    if name in institutions:
        for start in institutions[name].keys(): # 顺链寻找第一个未有结束时间的条目——即最新的条目
            if institutions[name][start]['end_time_new'] == "":
                institutions[name][start]['end_time_old'] = old_time
                institutions[name][start]['end_time_new'] = new_time
                break

# 读取变更表并生成总表
def dynamic_table_read(institution_tag, institutions):
    # 读取机构变更表
    org_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="机构动态表2")
    for index, row in org_table.iterrows():
        if row['变更类型'] == '新增' or row['变更类型'] == '重启': # 0-1
            institution_insert(institution_tag, institutions, row)
        elif row['变更类型'] == '拆分':
            add_end_time(institutions, row['原机构'], row['开始-时间'], row['开始-公元年份'])
            institution_insert(institution_tag, institutions, row)
        elif row['变更类型'] == '变更' or row['变更类型'] == '移置': # 1-1
            # 原机构条目删除，新机构条目重新加入
            add_end_time(institutions, row['原机构'], row['开始-时间'], row['开始-公元年份'])
            institution_insert(institution_tag, institutions, row)
        elif row['变更类型'] == '取消': # 1-0
            # 索引链中若有原机构存在，则删除
            add_end_time(institutions, row['原机构'], row['开始-时间'], row['开始-公元年份'])
        elif row['变更类型'] == '合并' or row['变更类型'] == '并入': # n-1
            origin_institution = row['原机构'].split("，")
            for ins in origin_institution:
                add_end_time(institutions, ins, row['开始-时间'], row['开始-公元年份'])
            func = ""
            for ins in origin_institution:
                for start in institutions[ins].keys():
                    if institutions[ins][start]['end_time_new'] == "":
                        func += " | " + institutions[ins][start]['function']
                        break
                add_end_time(institutions, ins, row['开始-时间'], row['开始-公元年份'])
            institution_insert(institution_tag, institutions, row)
            institutions[row['现机构']][row['开始-公元年份']]['function'] += func
        elif row['变更类型'] == '打散': # 1-n
            add_end_time(institutions, row['原机构'], row['开始-时间'], row['开始-公元年份'])
            institution_insert(institution_tag, institutions, row)
        else:
            print("Error: 未知的变更类型")
            break

    # 读取官职变更表
    job_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="官职动态表2")
    # 生成：官职对象字典——嵌入机构对象字典中
    for index, row in job_table.iterrows():
        if row['变更类型'] == '新增' or row['变更类型'] == '重启': # 0-1
            official_insert(institution_tag, institutions, row)
        elif row['变更类型'] == '变更': # 1-1
            # 原机构条目删除，新机构条目重新加入
            add_end_time(institutions, row['原官职'], row['开始-时间'], row['开始-公元年份'])
            official_insert(institution_tag, institutions, row)
        elif row['变更类型'] == '取消': # 1-0
            # 索引链中若有原机构存在，则删除
            add_end_time(institutions, row['原官职'], row['开始-时间'], row['开始-公元年份'])
        elif row['变更类型'] == '合并': # n-1
            origin_institution = row['原官职'].split("，")
            for ins in origin_institution:
                add_end_time(institutions, ins, row['开始-时间'], row['开始-公元年份'])
            func = ""
            for ins in origin_institution:
                for start in institutions[ins].keys():
                    if institutions[ins][start]['end_time_new'] == "":
                        func += " | " + institutions[ins][start]['function']
                        break
                add_end_time(institutions, ins, row['开始-时间'], row['开始-公元年份'])
            official_insert(institution_tag, institutions, row)
            institutions[row['现官职']][row['开始-公元年份']]['function'] += func
        elif row['变更类型'] == '打散': # 1-n
            add_end_time(institutions, row['原官职'], row['开始-时间'], row['开始-公元年份'])
            official_insert(institution_tag, institutions, row)
        else:
            print("Error: 未知的变更类型")
            break

# 静态表和展示表数据拼接
def table_combination(ins_table):
    # 读取机构静态表——需要的时候再结合
    org_info_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="机构静态表")
    # 补全机构对象的静态信息
    for index, row in org_info_table.iterrows():
        if row['机构名'] in ins_table:
            ins_table[row['机构名']]['type'] = row['类别']
            ins_table[row['机构名']]['other_names'] = row['简称与别名'] if row['简称与别名']==row['简称与别名'] else ""
            ins_table[row['机构名']]['ref_pdf_page'] = row['参考文档页数'] if row['参考文档页数']==row['参考文档页数'] else ""
            ins_table[row['机构名']]['trace'] = row['职源与沿革文本'] if row['职源与沿革文本']==row['职源与沿革文本'] else ""
            ins_table[row['机构名']]['ref_book'] = row['出处'] if row['出处']==row['出处'] else ""

    # 读取官职静态表
    job_info_table = pd.read_excel("../元丰改制尚书省下机构官职表总表.xlsx", sheet_name="官职静态表")
    # 补全官职对象的静态信息
    for index, row in job_info_table.iterrows():
        if row['官职名'] in ins_table:
            ins_table[row['官职名']]['other_names'] = row['简称与别名'] if row['简称与别名']==row['简称与别名'] else ""
            ins_table[row['官职名']]['ref_pdf_page'] = row['参考文档页数'] if row['参考文档页数']==row['参考文档页数'] else ""
            ins_table[row['官职名']]['trace'] = row['职源与沿革文本'] if row['职源与沿革文本']==row['职源与沿革文本'] else ""
            ins_table[row['官职名']]['ref_book'] = row['出处'] if row['出处']==row['出处'] else ""
            ins_table[row['官职名']]['parents'] = row['隶属机构'].split("，") if row['隶属机构']==row['隶属机构'] else []
            # 是否需要该链，暂时保留
            # institution_tag[row["官职名"]][start] = row['隶属机构'].split("，") if row['隶属机构']==row['隶属机构'] else ""

# 根据时间获取临时机构表
def get_institution(src_ins_dict, dst_ins_dict, time):
    for ins in src_ins_dict:
        for start in src_ins_dict[ins]:
            if start < time and (src_ins_dict[ins][start]['end_time_new'] == "" or src_ins_dict[ins][start]['end_time_new'] > time):
                dst_ins_dict[ins] = src_ins_dict[ins][start]
                break

# 生成机构树
def build_json(ins_table):
    # 节点的子节点应该由其他节点的父节点决定
    for name, ins_info in ins_table.items():
        if ins_info['parents'] != []:
            for parent in ins_info['parents']:
                # print(parent, name, institution_tag[name]) # 检查表格用
                ins_table[parent]['children_list'].append(name)
    root_name = "皇帝"
    def build_tree(node_name):
        node_info = ins_table[node_name]
        print(node_info)
        if node_info['type'] == "机构":
            children_names = node_info['children_list']
            if len(children_names) > 0:
                node_info['children'] = [build_tree(name) for name in children_names]
        return node_info
    nested_tree = build_tree(root_name)
    return nested_tree

# 根据机构变更表生成 机构路径链 和 机构对象
institution_tag = {} # 上级机构链
institutions = {} # 机构对象
showing_institutions = {}
dynamic_table_read(institution_tag, institutions)
get_institution(institutions, showing_institutions, time)
table_combination(showing_institutions)
nested_tree_json = build_json(showing_institutions)
json.dump(nested_tree_json, open("nested_tree2.json", "w", encoding="utf-8"), ensure_ascii=False, indent=2)
