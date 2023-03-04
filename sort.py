import os
from pathlib import Path
import re
import shutil
import glob

folders_dict = {
    "archives": ['.zip', '.gz', '.tar'],
    "video": ['.avi', '.mp4', '.mov', '.mkv'],
    "audio": ['.mp3', '.ogg', '.wav', '.amr'],
    "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    "images": ['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
    "others": []
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

# функція для видалення тек


def del_empty_folders(path: Path):
    for file_path in path.iterdir():
        if file_path.is_dir():
            del_empty_folders(file_path)
            if not any(file_path.iterdir()):
                file_path.rmdir()


# функція для створення тек згідно ключів словника


def create_folders(path: Path):
    for key in folders_dict.keys():
        try:
            path.joinpath(key).mkdir()
        except FileExistsError as e:
            print(e)


# працюємо з архівом
def unpack_archive(path: Path):
    for file_path in path.iterdir():
        search = re.findall(r"\.\w+", str(file_path), flags=re.IGNORECASE)
        try:
            if search[0] in folders_dict["archives"]:
                name_fldr_arch = file_path.name.split('.')[0]
                (my_path / 'archives').joinpath(name_fldr_arch).mkdir()
                path_archives = path / r"archives" / name_fldr_arch
                shutil.unpack_archive(
                    path / file_path.name, path_archives)

                os.remove(path / file_path.name)
        except IndexError as i:
            print(i)

# сортуємо файли по розширенню зі створенням відповідних тек(згідно словнику+)


def sort_and_move(path):
    for file_path in my_path.iterdir():
        search = re.findall(r"\.\w+", str(file_path), flags=re.IGNORECASE)
        try:
            if search[0] in folders_dict["video"]:
                file_path.rename(my_path/"video"/file_path.name)
            elif search[0] in folders_dict["audio"]:
                file_path.rename(my_path/"audio"/file_path.name)
            elif search[0] in folders_dict["documents"]:
                file_path.rename(my_path/"documents"/file_path.name)
            elif search[0] in folders_dict["images"]:
                file_path.rename(my_path/"images"/file_path.name)
            else:
                file_path.rename(my_path/"others"/file_path.name)
        except IndexError as i:
            print(i)


find_and_up(my_path)
del_empty_folders(my_path)
create_folders(my_path)
unpack_archive(my_path)
sort_and_move(my_path)
