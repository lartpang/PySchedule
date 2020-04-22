from utils.tool_funcs import adjust_table


def append_record(data_table, new_record):
    """
    向原有的数据表的最后插入新的记录

    Args:
        data_table: 原始的数据表
        new_record: 将要添加的新数据

    Returns:
        data_table: 添加新数据后的新表
    """
    assert set(new_record.keys()) == {"event", "date"}

    data_table["total_num"] += 1
    data_table[str(data_table["total_num"])] = new_record
    return data_table


def delete_record(data_table, idx_record):
    """
    从原有的数据表中删除特定序号的数据

    Args:
        data_table: 原始数据表
        idx_record: 将要删除的行的序号，这里的序号是按照表格中所示，也就是从1开始的计数

    Returns:
        data_table: 删除特定行之后的新表
    """
    total_num = data_table["total_num"]
    assert 0 < idx_record <= total_num

    pop_kv = data_table[str(idx_record)]
    # idx_record 是合法的
    if idx_record == total_num:
        # .pop()方法返回的是被删除的键值对，本身是一个in-place操作
        data_table.pop(str(idx_record))
    else:
        for idx in range(idx_record, total_num):
            data_table[str(idx)] = data_table[str(idx + 1)]
        data_table.pop(str(total_num))

    data_table["total_num"] -= 1
    return data_table


def update_record(data_table, idx_record, new_record):
    """
    对原有的数据表内的数据进行修改

    Args:
        data_table: 原始数据表
        idx_record: 要修改的行的序号，同样是从1开始计数
        new_record: 要更新的内容

    Returns:
        data_table: 修改后的新表
    """
    assert 0 < idx_record <= data_table["total_num"]

    # idx_record 是合法的
    data_table[str(idx_record)] = new_record
    return data_table


def display_all(data_table):
    """
    打印整个美化好的表格

    Args:
        data_table: 原始数据表

    Returns:
        None
    """
    data_table = adjust_table(data_table)
    for line in data_table:
        print(line)
