import os
from pathlib import Path
import shutil


def create_folders(path):

    folders = ["archives", "video", "audio", "documents", "images"]

    # перебираэмо список з назвами тек, будуючи шлях до них і створюючи їх
    for f in folders:
        folder = os.path.join(p, f)
    # перевірка чи існують уже дані теки, якшо існують - не створюємо
        if not os.path.exists(folder):
            os.mkdir(folder)
        print(folder)


def sort_files(path):
    for filename in os.listdir(p):
        if filename.endswith(".txt"):
            shutil.move(os.path.join(p, filename),
                        os.path.join(p, 'documents'))
        if filename.endswith(".bmp"):
            shutil.move(os.path.join(p, filename),
                        os.path.join(p, 'images'))

        print(filename)


p = r"C:\Users\EgorM\Desktop\hlam"

if __name__ == "__main__":
    # create_folders(p)
    sort_files(p)
