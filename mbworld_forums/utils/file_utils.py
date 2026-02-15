import json
import os
from csv import DictReader

from mbworld_forums.mbworld_forums.static import file_headers
from mbworld_forums.mbworld_forums.utils.clean_utils import clean


def get_feed(filepath, file_type="csv", csv_headers=file_headers, overwrite=True):
    return {
        filepath: {
            'format': file_type,
            'encoding': 'utf8',
            # 'store_empty': False,
            'fields': csv_headers,
            'indent': 4,
            'overwrite': overwrite,
        },
    }


def get_csv_records(filepath):
    if not os.path.exists(filepath):
        return []
    return [dict(r) for r in DictReader(open(filepath, encoding='utf-8')) if r]


def get_json_records(filename):
    # return json.load(open(filename, encoding='utf-8'))
    return json.loads(open(filename, encoding='utf-8').read() or '[]')


def get_jl_records(filename):
    if not os.path.exists(filename):
        return []
    return json.loads("[" + ",".join(open(filename, encoding='utf-8').readlines()) + "]" or '[]')


def get_csv_writer(filepath, csv_headers):
    if not os.path.exists(filepath) or has_records(filepath) < 1:
        file = open(filepath, mode='w', encoding='utf-8')
        file.write(','.join(h for h in csv_headers) + '\n')
        return file

    return open(filepath, mode='a+', encoding='utf-8')


def has_records(filepath):
    if not os.path.exists(filepath):
        return 0
    # return len([r for r in DictReader(open(filepath, encoding='utf-8')) if r])
    return len([clean(r) for r in open(filepath, encoding='utf-8').readlines()[:5] if clean(r)])


def write_to_csv(item, filepath, csv_headers):
    if not item:
        return
    row = ','.join('"{}"'.format(item.get(h, '')) for h in csv_headers) + '\n'
    csv_writer = get_csv_writer(filepath, csv_headers)
    csv_writer.write(row)
    csv_writer.close()
    print(f"Forum meta record inserted into a csv file-> {filepath}\n{item}")


def delete_file(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)


def make_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)
        print(f"Directory has been created:\n{dir_path}")
