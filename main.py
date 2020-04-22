import argparse

from utils.file_funcs import read_json, save_table
from utils.operator_funcs import append_record, delete_record, display_all, update_record
from utils.print_funcs import disp_msg
from utils.tool_funcs import read_data


def main(args):
    file_path = args.path
    if args.mode == "dispall":
        data_table = read_json(file_path)
        display_all(data_table)
    elif args.mode == "append":
        disp_msg("插入新数据")
        input_dict = read_data(mode="append", need_dt=False)
        data_table = read_json(file_path)
        new_record = {"event": input_dict["event"], "date": input_dict["date"]}
        data_table = append_record(data_table, new_record=new_record)
        save_table(file_path, data_table)
    elif args.mode == "delete":
        disp_msg("删除指定记录")
        input_dict = read_data(mode="delete", need_dt=False)
        data_table = read_json(file_path)
        idx_record = input_dict["idx_record"]
        data_table = delete_record(data_table, idx_record=idx_record)
        save_table(file_path, data_table)
    elif args.mode == "update":
        disp_msg("更新指定记录")
        input_dict = read_data(mode="update", need_dt=False)
        data_table = read_json(file_path)
        idx_record = input_dict["idx_record"]
        new_record = {"event": input_dict["event"], "date": input_dict["date"]}
        data_table = update_record(data_table, idx_record=idx_record, new_record=new_record)
        save_table(file_path, data_table)
    else:
        raise NotImplementedError


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A tool script to record schedule.")
    # type参数理论上可以是任何合法的类型， 但有些参数传入格式比较麻烦，例如list，
    # 一般使用bool, int, str, float这些基本类型，更复杂的需求可以通过str传入，然后手动解析。
    # bool类型的解析比较特殊，传入任何值都会被解析成True，传入空值时才为False
    parser.add_argument("--mode", type=str, required=False, default="dispall")
    parser.add_argument("--path", type=str, required=False, default="./test.json")
    # TODO: 这里目前仅实现了显示所有数据，之后应该尝试设定如何显示的问题，例如可以单独显示多
    #   少时间内的事件，等等
    args = parser.parse_args()
    main(args)
