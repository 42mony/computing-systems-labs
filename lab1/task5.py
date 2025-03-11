def filter_word(word: str):
    return word.istitle()


def sort_words(input_str: str):
    my_list = input_str.split(" ")  # ['Привет', 'пока', 'строки', 'записаны']
    filtered_words = list(filter(filter_word, my_list))
    new_list = sorted(filtered_words, key=str.lower)
    return new_list


some_string = "Привет Cтроки пока записаны"
print(sort_words(some_string))
