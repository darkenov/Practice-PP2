import shutil

# Копируем файл
shutil.copy("data.txt", "data_backup.txt")
print("Копия создана: data_backup.txt")

# Копируем в другую папку
import os
os.makedirs("backup_folder", exist_ok=True)
shutil.copy("data.txt", "backup_folder/data.txt")
print("Копия в папке: backup_folder/data.txt")

import os

# Безопасное удаление — проверяем перед удалением
if os.path.exists("data_backup.txt"):
    os.remove("data_backup.txt")
    print("Файл удалён!")
else:
    print("Файл не найден!")

# Удалить папку с содержимым
import shutil
if os.path.exists("backup_folder"):
    shutil.rmtree("backup_folder")
    print("Папка удалена!")