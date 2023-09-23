



def group_list(custom_list: list, size: int = 4):
    # my_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] -> convert this: res_list = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
    grouped_list = []
    group_size = size
    my_range = range(0, len(custom_list), group_size)
    print(list(my_range))
    for i in my_range:
        grouped_list.append(custom_list[i:i + group_size])
    return grouped_list