import json

# json.load(open("../json/file1.json"))
# json.load(open("../json/file2.json"))

# Открываем file1 для чтения
with open('hexlet_code/json/file1.json', 'r', encoding='utf-8') as file:
    # Парсим JSON из файла
    data = json.load(file)
print("--------------------------------")
print("Файл 1")
print("--------------------------------")


print(f"Хост: {data['host']}")
print(f"время: {data['timeout']}")
print(f"прокси: {data['proxy']}")
print(f"подписка: {data['follow']}")

print("--------------------------------")
print("Файл 2")
print("--------------------------------")

#открываем второй файл для чтения
with open('hexlet_code/json/file2.json', 'r', encoding='utf-8') as file:
    # Парсим JSON из файла
    data = json.load(file)


print(f"время: {data['timeout']}")
print(f"verbouse: {data['verbose']}")
print(f"Хост: {data['host']}")

