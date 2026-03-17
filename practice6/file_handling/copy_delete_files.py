import shutil

# Копируем файл
shutil.copy("data.txt", "data_backup.txt")
print("copy created: data_backup.txt")

# Копируем в другую папку
import os
os.makedirs("backup_folder", exist_ok=True)
shutil.copy("data.txt", "backup_folder/data.txt")
print("copy in folder: backup_folder/data.txt")

import os

# Безопасное удаление — проверяем перед удалением
if os.path.exists("data_backup.txt"):
    os.remove("data_backup.txt")
    print("file deleted")
else:
    print("file not found")

# Удалить папку с содержимым
import shutil
if os.path.exists("backup_folder"):
    shutil.rmtree("backup_folder")
    print("file deleted")