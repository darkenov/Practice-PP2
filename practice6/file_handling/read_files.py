# Создаём файл и пишем данные
with open("data.txt", "w") as file:
    file.write("Привет, это первая строка!\n")
    file.write("Вторая строка данных\n")
    file.write("Третья строка данных\n")

print("Файл создан!")

with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())