# Создаём файл и пишем данные
with open("data.txt", "w") as file:
    file.write("Hello,it is first line!\n")
    file.write("Second line of dates\n")
    file.write("Third line of dates\n")

print("File created")

with open("data.txt", "r") as file:
    for line in file:
        print(line.strip())