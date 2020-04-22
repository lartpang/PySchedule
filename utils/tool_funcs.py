from datetime import datetime

from dateutil.parser import parse

DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


def datetime2str(idt):
    """
    从datetime对象转化为字符串，以方便显示
    NOTE: 对于datetime对象计算差值之后，得到的是timedelta对象，而这个对象是没有
        strftime方法的，这时直接使用str()转化即可

    Args:
        idt: datetime对象

    Returns:
        一个特定格式的字符串
    """
    return idt.strftime(DATE_FORMAT)


def str2datetime(istr):
    """
    从字符串转化为datetime对象，以方便计算

    Args:
        istr: 输入字符串

    Returns:
        一个特定格式的datetime对象
    """
    return datetime.strptime(istr, DATE_FORMAT)


def get_length(istr):
    """
    获取输入的字符串的长度（这里按照中文字符长度为2，英文为1来计算）

    Args:
        istr: 输入字符串，可以是中英文混杂

    Returns:
        按照中文长为2，英文为1计算得到的长度
    """
    return len(istr.encode("gbk"))


def read_data(mode="append", need_dt=False):
    """
    read input data from the command line

    Args:
        mode: 不同的读取数据的需求
        need_dt: 是否需要返回datetime格式的时间数据，如果不，则返回字符串类型的数据

    Returns:
        info_dict: 输入数据的字典形式
    """

    def read_idx(info_dict):
        idx_record = input(" >> Event ID: ").strip()
        assert idx_record.isnumeric()
        info_dict['idx_record'] = int(idx_record)
        return info_dict

    def read_event_date(info_dict, need_dt):
        info_dict["event"] = input(" >> Event: ").strip()
        if need_dt:
            info_dict["date"] = parse(input(" >> Date: ").strip())
        else:
            info_dict["date"] = datetime2str(parse(input(" >> Date: ").strip()))
        return info_dict

    print(" ==>> 请按照提示输入：")
    info_dict = dict()
    if mode == "append":
        info_dict = read_event_date(info_dict, need_dt)
    elif mode == "delete":
        info_dict = read_idx(info_dict)
    elif mode == "update":
        # TODO: 这里对于更新的策略设置太简单了
        #   - 起码应该考虑更新哪些内容
        #   - 还应该输出当前的方便比对
        info_dict = read_idx(info_dict)
        info_dict = read_event_date(info_dict, need_dt)
    else:
        raise NotImplementedError
    return info_dict
