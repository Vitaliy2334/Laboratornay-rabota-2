import os
import subprocess
import argparse
import random


def process_file(file_path, duration, extended, num):
    """Вырезает случайный кусок из заданного файла с указанной длительностью и
       применяет эффекты fade in и fade out, если extended = True"""
    start = round(random.uniform(0, max(0, duration - 10)), 3)
    end = round(min(start + duration, duration), 3)

    input_options = ['-ss', str(start), '-t', str(end - start), '-i', file_path]
    effect_options = []
    if extended:
        effect_options = ['-af', f'afade=t=in:st=0:d=0.5,afade=t=out:st={end - start - 0.5}:d=0.5']

    output_path = os.path.join(os.getcwd(), f'temp{num}.mp3')
    output_options = ['-y', '-vn', '-ar', '44100', '-ac', '2', '-b:a', '192k', output_path]

    cmd = ['ffmpeg'] + input_options + effect_options + output_options
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return output_path


def process_directory(source_dir, count, _duration, log, extended):
    """Обрабатывает все mp3-файлы в указанной директории и возвращает список
       путей к временным файлам, содержащим обработанные аудиоданные"""
    audio_files = [os.path.join(source_dir, f) for f in os.listdir(source_dir) if f.endswith('.mp3')]

    if count is not None and count < len(audio_files):
        audio_files = random.sample(audio_files, count)

    output_files = []
    for i, file_path in enumerate(audio_files):
        if log:
            print(f'--- processing file {i + 1}: {os.path.basename(file_path)}')
        output_path = process_file(file_path, _duration, extended, i)
        output_files.append(output_path)

    if log:
        print('--- done!')
    return output_files


def create_mix(output_files, dest_name):
    """Объединяет все обработанные аудиофайлы в один микс"""
    output_path = os.path.join(os.getcwd(), dest_name)
    input_options = ['-i', 'concat:' + '|'.join(output_files)]
    output_options = ['-y', '-ac', '2', '-b:a', '192k', output_path]

    cmd = ['ffmpeg'] + input_options + output_options
    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--source", required=True, help="имя рабочей директории с треками", default="task7")
    parser.add_argument("-d", "--destination", help="имя выходного файла", default="mix.mp3")
    parser.add_argument("-c", "--count", type=int, help="количество файлов в 'нарезке'", default=3)
    parser.add_argument("-f", "--frame", type=int, help="количество секунд на каждый файл", default=10)
    parser.add_argument("-l", "--log", action="store_true", help="выводить лог процесса обработки файлов",
                        default=False)
    parser.add_argument("-e", "--extended", action="store_true", help="fade in/fade out для каждого фрагмента",
                        default=False)
    args = parser.parse_args()

    temp = process_directory(args.source, args.count, args.frame, args.log, args.extended)

    create_mix(temp, args.destination)

    # чистим за собой мусор
    for tmp in temp:
        os.remove(tmp)


if __name__ == '__main__':
    main()
# py .\trackmix.py --source "task7" --count 4 --frame 10 -l -e