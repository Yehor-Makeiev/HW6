import os
from pathlib import Path
import re
import shutil
import glob

folders_dict = {
    "archives": ['ZIP', 'GZ', 'TAR'],
    "video": ['AVI', 'MP4', 'MOV', 'MKV'],
    "audio": ['MP3', 'OGG', 'WAV', 'AMR'],
    "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    "images": ['JPEG', 'PNG', 'JPG', 'SVG']
}

first_folder = r"C:\Users\EgorM\Desktop\hlam"
my_path = Path(first_folder)

# Ітеруємось по теці і виводимо всі файли на 1 рівень


def find_and_up(path: Path):

    for file_path in path.iterdir():

        if file_path.is_dir():
            find_and_up(file_path)

        elif file_path.is_file():
            try:
                file_path.rename(my_path / file_path.name)
            except FileExistsError:
                print(
                    f"{file_path.name} in {file_path.resolve()} - exist, plese rename ")  # додати можливість відразу перейменувати

# cтворити функцыю для видалення тек!!!!!!

# функція для створення тек згідно ключів словника


def create_folders(path: Path):
    for key in folders_dict.keys():
        try:
            path.joinpath(key).mkdir()
        except FileExistsError as e:
            print(e)

    # сортуємо файли по розширенню зі створенням відповідних тек(згідно словнику)
for file_path in my_path.iterdir():
    search = re.findall(r"\.\w+", str(file_path), flags=re.IGNORECASE)
    try:
        if search[0] in folders_dict["documents"]:
            file_path.rename(my_path/"documents"/file_path.name)

    except IndexError as i:
        print(i)

# find_and_up(my_path)


create_folders(my_path)
