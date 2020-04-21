# coding: utf-8

import json
import os
import argparse
from datetime import datetime
from dateutil.parser import parse
from utils.tool_funcs import str2datetime, datetime2str, get_length

NOT_EXIST = -1
DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def read4json(file_path: str):
    """
    从json文件中读取数据

    params: file_path, json文件路径
    return: all_info_dict, 从文件中载入的数据，核心的事件内容和日期都是字符串
    """

    def not_exist_or_empty():
        all_info_dict["total_num"] = 0
        return all_info_dict

    all_info_dict = dict()
    if not os.path.exists(file_path):
        print(" ==>> 文件不存在 <<== ")
        all_info_dict = not_exist_or_empty()
    else:
        with open(file_path, mode="r", encoding="utf-8") as record_file:
            try:
                # 载入成功没必要提示
                all_info_dict = json.load(record_file)
            except json.decoder.JSONDecodeError:
                context = record_file.readlines()
                if len(context) == 0:
                    print(" ==>> 文件是空的 <<== ")
                    all_info_dict = not_exist_or_empty()
                else:
                    raise Exception(" ==>> 请检查json内容 <<== ")
    return all_info_dict


def save2json(file_path: str, info_dict: dict):
    """
    将输入的数据附加到原始的文件内数据中

    params:
        file_path, 目标文件路径
        info_dict, 要保存的输入数据
    return: None
    """
    all_info_dict = read4json(file_path=file_path)
    with open(file_path, mode="w", encoding="utf-8") as record_file:
        all_info_dict["total_num"] += 1
        all_info_dict[str(all_info_dict["total_num"])] = info_dict
        json.dump(all_info_dict, record_file)
    print(f"{info_dict} has saved in {file_path}.")


def modify_width(msg_table):
    """
    对输入的二维列表数据的每一项进行宽度调整，宽度的基准是输入二维列表最后一行的各项宽度

    params: msg_table, 输入的需要处理的二维列表，此时最后一行是表头
    return: new_msg_table, 调整以后的一维列表，此时原本的一行被合并为一个单独的字符串，
        此时第一行是表头，同时第二行使用了虚线分开
    """
    column_width_list = [len(x) for x in msg_table[-1]]

    new_msg_table = []

    temp_raw = " --"
    for item in column_width_list:
        temp_raw += "-" * item + " - "
    new_msg_table.append(temp_raw)

    temp_raw = " | "
    for idx, item in enumerate(msg_table[-1]):
        temp_raw += item + " " * (column_width_list[idx] - get_length(item)) + " | "
    new_msg_table.append(temp_raw)

    temp_raw = " | "
    for item in column_width_list:
        temp_raw += "-" * item + " | "
    new_msg_table.append(temp_raw)

    for raw in msg_table[:-1]:
        temp_raw = " | "
        for idx, item in enumerate(raw):
            temp_raw += item + " " * (column_width_list[idx] - get_length(item)) + " | "
        new_msg_table.append(temp_raw)

    temp_raw = " --"
    for item in column_width_list:
        temp_raw += "-" * item + " - "
    new_msg_table.append(temp_raw)

    return new_msg_table


def json2table(file_path):
    """
    将目标文件中存储的数据按照特定的格式打印出来

    params: file_path, 目标文件路径
    return: None
    """
    table = []
    max_length_event_str = 0
    max_length_date_str = 0
    max_length_remain_str = 0

    all_info_dict = read4json(file_path=file_path)
    if all_info_dict["total_num"] != 0:
        for i in range(1, all_info_dict["total_num"] + 1):
            event_str = all_info_dict[str(i)]["event"]
            if get_length(event_str) > max_length_event_str:
                max_length_event_str = get_length(event_str)
            date_str = all_info_dict[str(i)]["date"]
            if get_length(date_str) > max_length_date_str:
                max_length_date_str = get_length(date_str)
            remain_str = str(str2datetime(date_str) - datetime.now())
            if get_length(remain_str) > max_length_remain_str:
                max_length_remain_str = get_length(remain_str)
            table.append([event_str, date_str, remain_str])

    event_head_str = "Event"
    if max_length_event_str > len(event_head_str):
        event_head_str = " " * (max_length_event_str - len(event_head_str)) + event_head_str
    date_head_str = "Date"
    if max_length_date_str > len(date_head_str):
        date_head_str = " " * (max_length_date_str - len(date_head_str)) + date_head_str
    remain_head_str = "Remain"
    if max_length_remain_str > len(remain_head_str):
        remain_head_str = " " * (max_length_remain_str - len(remain_head_str)) + remain_head_str
    table.append([event_head_str, date_head_str, remain_head_str])

    table = modify_width(table)
    return table


def read4cli(need_dt=False):
    """
    read input data from the command line

    params:
        need_dt, 是否需要返回datetime格式的时间数据，如果不，则返回字符串类型的数据
    return: info_dict, 输入数据的字典形式
    """
    info_dict = dict()

    print(" ==>> 请按照提示输入：")
    info_dict["event"] = input(" >> Event: ").strip()
    info_dict["date"] = datetime2str(parse(input(" >> Date: ").strip()))
    return info_dict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool script to record schedule.")
    # type参数理论上可以是任何合法的类型， 但有些参数传入格式比较麻烦，例如list，
    # 一般使用bool, int, str, float这些基本类型，更复杂的需求可以通过str传入，然后手动解析。
    # bool类型的解析比较特殊，传入任何值都会被解析成True，传入空值时才为False
    parser.add_argument("--disp", type=bool, required=False, default=True)
    args = parser.parse_args()

    file_path = "./test.json"
    if args.disp:
        table = json2table(file_path)
        for line in table:
            print(line)
    else:
        print("-" * 82)
        print("|" + " " * 34 + "添加新的事件" + " " * 34 + "|")
        print("-" * 82)
        info_dict = read4cli(need_dt=False)
        save2json(file_path, info_dict)
