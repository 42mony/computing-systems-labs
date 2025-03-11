dickt = {"asbddb": 1, "bd": 5, "csd": 2, "fese0": 3, "fkruf": 4}

def validate_func(item: tuple[str, int], average: int):
    key, _value = item
    if len(key) >= average:
        return True
    else: 
        return False
    

def some_func(dickt: dict[str, int]):
    svaga = list(dickt.keys())
    min_key = min(svaga, key=str.__len__)
    max_key = max(svaga, key=str.__len__)
    min_value = dickt.get(min_key)
    max_value = dickt.get(max_key)
    average_value = (min_value + max_value) / 2
    filtered_dict = dict(filter(lambda item: validate_func(item, average_value), dickt.items()))
    return filtered_dict
   
res=some_func(dickt)
print(res)


