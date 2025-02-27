my_dict = {
    "1": 6,
    "2": 4,
    "3": 5,
    "4": 3,
    "5": 1,
}

keys = sorted(my_dict, key=my_dict.get)
print("Отсортированые ключи", keys)
