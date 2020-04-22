import json
import os


def read_json(file_path):
    """
    从json文件中读取数据

    Args:
        file_path: json文件路径

    Returns:
        all_info_dict: 从文件中载入的数据，核心的事件内容和日期都是字符串
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


def save_table(file_path, data_table):
    """
    将输入的数据写入json文件中

    Args:
        file_path: 目标文件路径
        data_table: 要保存的输入数据

    Returns:
        None
    """
    with open(file_path, mode="w", encoding="utf-8") as record_file:
        json.dump(data_table, record_file)
