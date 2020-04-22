from datetime import datetime

from utils.tool_funcs import get_length


def modify_width(msg_table):
    """
    对输入的二维列表数据的每一项进行宽度调整，宽度的基准是输入二维列表最后一行的各项宽度

    Args:
        msg_table: 输入的需要处理的二维列表，此时最后一行是表头

    Returns:
        new_msg_table: 调整以后的一维列表，此时原本的一行被合并为一个单独的字符串，
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


def disp_msg(msg):
    """
    一个简单的工具函数，用来生成比较合适的标题装饰后的输出

    Args:
        msg: 要显示的字符串

    Returns:
        None
    """
    space_width = 80 - get_length(msg)
    print("-" * 82)
    print("|" + " " * (space_width // 2) + str(msg) + " " * (space_width - space_width // 2) + "|")
    print("-" * 82)


def supply_space(max_length, target_str):
    """
    使用空格将指定字符串补充到特定宽度，如果字符串本身已经超过了这个宽度，那么就不处理

    Args:
        max_length: 目标宽度
        target_str: 需要补充的字符串

    Returns:
        target_str: 调整后的字符串
    """
    if max_length > len(target_str):
        target_str = " " * (max_length - len(target_str)) + target_str
    return target_str


def adjust_table(data_table):
    """
    将表格数据按照特定的格式打印出来

    Args:
        data_table: 目标文件路径

    Returns:
        new_data_table: 调整后的表格
    """
    new_data_table = []
    max_length_event_str = 0
    max_length_date_str = 0
    max_length_remain_str = 0

    if data_table["total_num"] != 0:
        for i in range(1, data_table["total_num"] + 1):
            event_str = data_table[str(i)]["event"]
            if get_length(event_str) > max_length_event_str:
                max_length_event_str = get_length(event_str)
            date_str = data_table[str(i)]["date"]
            if get_length(date_str) > max_length_date_str:
                max_length_date_str = get_length(date_str)
            remain_str = str(str2datetime(date_str) - datetime.now())
            if get_length(remain_str) > max_length_remain_str:
                max_length_remain_str = get_length(remain_str)
            new_data_table.append([event_str, date_str, remain_str])

    event_head_str = "Event"
    event_head_str = supply_space(max_length_event_str, event_head_str)
    date_head_str = "Date"
    date_head_str = supply_space(max_length_date_str, date_head_str)
    remain_head_str = "Remain"
    remain_head_str = supply_space(max_length_remain_str, date_head_str)
    new_data_table.append([event_head_str, date_head_str, remain_head_str])

    new_data_table = modify_width(new_data_table)
    return new_data_table
