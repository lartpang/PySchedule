from datetime import datetime


def datetime2str(idt):
    """
    从datetime对象转化为字符串，以方便显示
    NOTE: 对于datetime对象计算差值之后，得到的是timedelta对象，而这个对象是没有
        strftime方法的，这时直接使用str()转化即可

    params: idt, datetime对象
    return: 一个特定格式的字符串
    """
    return idt.strftime("%Y-%m-%d %H:%M:%S")


def str2datetime(istr):
    """
    从字符串转化为datetime对象，以方便计算

    params: istr, 输入字符串
    return: 一个特定格式的datetime对象
    """
    return datetime.strptime(istr, "%Y-%m-%d %H:%M:%S")


def get_length(istr):
    """
    获取输入的字符串的长度（这里按照中文字符长度为2，英文为1来计算）

    params: istr, 输入字符串，可以是中英文混杂
    return: 按照中文长为2，英文为1计算得到的长度
    """
    return len(istr.encode("gbk"))
