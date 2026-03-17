# Добавляем строки (не перезаписывая!)
with open("data.txt", "a") as file:
    file.write("fourth line added!\n")
    file.write("Fives line also added!\n")

# Проверяем — читаем весь файл
with open("data.txt", "r") as file:
    print(file.read())