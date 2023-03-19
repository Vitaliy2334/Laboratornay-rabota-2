import os
import shutil
import argparse
import datetime


def parse_args():
    parser = argparse.ArgumentParser(description='Reorganize files in directory')
    parser.add_argument('--source', required=True, help='Path to source directory')
    parser.add_argument('--days', type=int, required=True, help='Minimum number of days since last modification')
    parser.add_argument('--size', type=int, required=True, help='Maximum file size in bytes')
    return parser.parse_args()


def main():
    args = parse_args()
    source_dir = args.source
    archive_dir = os.path.join(source_dir, 'Archive')
    small_dir = os.path.join(source_dir, 'Small')
    today = datetime.datetime.today()
    min_date = today - datetime.timedelta(days=args.days)

    if not os.path.isdir(archive_dir):
        os.mkdir(archive_dir)

    if not os.path.isdir(small_dir):
        os.mkdir(small_dir)

    flag_archive = False
    flag_size = False

    for filename in os.listdir(source_dir):
        file_path = os.path.join(source_dir, filename)
        if os.path.isfile(file_path):
            file_size = os.path.getsize(file_path)
            file_date = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
            if file_size < args.size:
                flag_size = True
                shutil.move(file_path, small_dir)
            elif file_date < min_date:
                flag_archive = True
                shutil.move(file_path, archive_dir)

    if not flag_size:
        os.rmdir(small_dir)
    elif not flag_archive:
        os.rmdir(archive_dir)

    print('Reorganization complete')


# запуск задания в терминале: py .\reorganize.py --source "task6" --days 2 --size 4096


if __name__ == '__main__':
    main()
