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


p = r"C:\Users\EgorM\Desktop\hlam"

if __name__ == "__main__":
    create_folders(p)
