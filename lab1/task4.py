my_list = list(range(5, 101, 5))

my_tuple = tuple(my_list)
my_list.clear()

for number in my_tuple:
    if number >= 50:
        my_list.append(number + 39)
    else:
        my_list.append(number * 3)

my_list.extend(reversed(my_tuple))

print(my_list)
