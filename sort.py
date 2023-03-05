import os
from pathlib import Path
import re
import shutil
import string
import sys


folders_dict = {
    "archives": ['.zip', '.gz', '.tar'],
    "video": ['.avi', '.mp4', '.mov', '.mkv'],
    "audio": ['.mp3', '.ogg', '.wav', '.amr'],
    "documents": ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx'],
    "images": ['.jpeg', '.png', '.jpg', '.svg', '.bmp'],
    "others": []
}

# для збору інфи (в майбутньому перенести у функцію, все підвзяати на словники)


info_arch = []
info = []
info_others = []


def first_folder():
    try:
        my_path = Path(sys.argv[1])
    except IndexError:
        raise IndexError("Введіть шлях")
    if not my_path.exists():
        raise TypeError("Такий шлях не існує")

    return my_path


# Ітеруємось по теці і виводимо всі файли на 1 рівень


def find_and_up(path: Path, target_path: Path):

    for file_path in path.iterdir():

        if file_path.is_dir():
            find_and_up(file_path, target_path)

        elif file_path.is_file():
            try:

                file_path.replace(target_path / file_path.name)
            except FileExistsError:
                print(
                    f"{file_path.name} in {file_path.resolve()} - exist, plese rename ")

# міняємо назви, з кирилиці на латинські, замість знаків "_"


def normalize(my_path: Path):

    CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"

    TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
                   "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

    TRANS = {}

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS[ord(c)] = l
        TRANS[ord(c.upper())] = l.upper()

    for file_dir in my_path.iterdir():
        fd_name = file_dir.name.split(".")[0]

        for w in fd_name:
            if w in string.punctuation:
                fd_name = fd_name.replace(w, "_")
        fd_new = fd_name.translate(TRANS)

        fd_suf = ""
        nfd_suf = fd_suf.join(re.findall(r"\.\w{2,4}", file_dir.name))

        if nfd_suf:
            fool_name = fd_new + nfd_suf
            old_file_path = my_path / file_dir.name
            new_file_path = old_file_path.with_name(fool_name)
            old_file_path.rename(new_file_path)
        else:
            old_file_path = my_path / file_dir.name
            new_file_path = old_file_path.with_name(fd_new)
            old_file_path.rename(new_file_path)

    # функція для видалення тек


# видяляэмо пусті теки


def del_empty_folders(my_path: Path):

    for file_path in my_path.iterdir():

        if file_path.is_dir():
            del_empty_folders(file_path)

            if not any(file_path.iterdir()):
                file_path.rmdir()


# функція для створення тек для сортування по назві ключів словника

def create_folders(my_path: Path):

    for key in folders_dict.keys():
        try:
            my_path.joinpath(key).mkdir()
        except FileExistsError as e:
            print(e)


# Розпаковуємо архів у новостворену теку по назві архіву(в створену раніше папку архів)


def unpack_archive(my_path: Path):

    for file_path in my_path.iterdir():

        search = re.findall(r"\.\w+", str(file_path), flags=re.IGNORECASE)

        try:
            if search[0] in folders_dict["archives"]:
                info_arch.append(search[0])
                name_fldr_arch = file_path.name.split('.')[0]
                (my_path / 'archives').joinpath(name_fldr_arch).mkdir()

                path_archives = my_path / r"archives" / name_fldr_arch
                shutil.unpack_archive(
                    my_path / file_path.name, path_archives)

                os.remove(my_path / file_path.name)

        except IndexError as i:
            print("")
    return set(info_arch)

# сортуємо файли по розширенню зі створенням відповідних тек(згідно словнику+ збираэмо інформацію про всі відомі розширення в файлі)


def sort_and_move(my_path: Path):

    for file_path in my_path.iterdir():

        search = re.findall(r"\.\w+", str(file_path), flags=re.IGNORECASE)

        try:
            if search[0] in folders_dict["video"]:
                info.append(search[0])
                file_path.rename(my_path/"video"/file_path.name)

            elif search[0] in folders_dict["audio"]:
                info.append(search[0])
                file_path.rename(my_path/"audio"/file_path.name)

            elif search[0] in folders_dict["documents"]:
                info.append(search[0])
                file_path.rename(my_path/"documents"/file_path.name)

            elif search[0] in folders_dict["images"]:
                info.append(search[0])
                file_path.rename(my_path/"images"/file_path.name)

            else:
                info_others.append(search[0])
                file_path.rename(my_path/"others"/file_path.name)

        except IndexError as i:
            print("")
    return print(f" Розширення які зустрічались в папці: {set(info)} Архіви: {set(info_arch)}\n Невідомі розширення {set(info_others)}"),

# виводимо інформацію про файли в теках


def list_files(my_path: Path):
    for file_path in my_path.iterdir():

        if file_path.is_dir():
            print(f"-{file_path.name} :")
            list_files(file_path)
        elif file_path.is_file():
            print(f"----{file_path.name}")
    return


def main():
    my_path = first_folder()

    find_and_up(my_path, my_path)
    normalize(my_path)
    del_empty_folders(my_path)
    create_folders(my_path)
    unpack_archive(my_path)
    sort_and_move(my_path)
    list_files(my_path)


if __name__ == "__main__":
    main()
