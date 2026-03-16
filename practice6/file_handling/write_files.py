# Добавляем строки (не перезаписывая!)
with open("data.txt", "a") as file:
    file.write("Четвёртая строка — добавлена!\n")
    file.write("Пятая строка — тоже добавлена!\n")

# Проверяем — читаем весь файл
with open("data.txt", "r") as file:
    print(file.read())