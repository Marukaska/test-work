import argparse
import json
import os
import tempfile

storage_data = os.path.join(tempfile.gettempdir(), 'storage.data')


def read_data():
    if not os.path.exists(storage_data):
        return {}
    with open(storage_data, 'r', encoding='utf-8') as file:
       data = json.load(file)
    return data


def write_data(dict_data):
    with open(storage_data, 'w', encoding='utf-8') as file:
        json.dump(dict_data, file, ensure_ascii=False)


try:

    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--key', help='Key')
    arg_parser.add_argument('--val', help='Value')

    arguments = arg_parser.parse_args()

    if arguments.key is not None and arguments.val is not None:

        data_temp = read_data()

        if arguments.key in data_temp:
            data_temp[arguments.key].append(arguments.val)
        else:
            data_temp[arguments.key] = [arguments.val]

        write_data(data_temp)

    elif arguments.key is not None and arguments.val is None:

        data_temp = read_data()

        if arguments.key in data_temp:
            print(data_temp[arguments.key])
        else:
            print("None")

    else:
        print("The key (--key) is not specified, execution is impossible")

except Exception as err:
    print(f'Error in script: "{err}"')
