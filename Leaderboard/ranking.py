"""



"""


def quick_sort(lst):
    if len(lst) == 1:
        return lst
    else:
        low, same, high = quick_split(lst[0], lst[0])
        return quick_sort(low) + same + quick_sort(high)


def quick_split(pivot, lst):
    low, same, high = [], [], []
    for element in lst:
        if element[1] < pivot[1]:
            low.append(element)
        elif element[1] > pivot[1]:
            high.append(element)
        else:
            same.append(element)
    return low, same, high


def merge_sort(lst):
    """
    Args:
        lst: A list of tuples of regions and home price indices

    Returns: A new, sorted list sorted in order of descending home price indices
    """
    if len(lst) <= 1:
        return lst
    else:
        lst1, lst2 = split(lst)
        return merge(merge_sort(lst1), merge_sort(lst2))


def split(lst):
    """
    Args:
        lst: A list of tuples of regions and home price indices

    Returns: Two lists split by the even and odd indices of the original list
    """
    lst1, lst2 = [], []
    for idx in range(len(lst)):
        if idx % 2 == 0:
            lst1.append(lst[idx])
        else:
            lst2.append(lst[idx])
    return lst1, lst2


def merge(lst1, lst2):
    """
    Args:
        lst1: A sorted list of tuples of regions and home price indices ordered by descending home price indices
        lst2: A sorted list of tuples of regions and home price indices ordered by descending home price indices

    Returns: A sorted list of tuples of regions and home price indices ordered by descending home price indices
    """
    lst = []
    idx1, idx2 = 0, 0
    while idx1 < len(lst1) and idx2 < len(lst2):
        if lst1[idx1][1] >= lst2[idx2][1]:
            lst.append(lst1[idx1])
            idx1 += 1
        else:
            lst.append(lst2[idx2])
            idx2 += 1
    if idx1 < len(lst1):
        for element in lst1[idx1:]:
            lst.append(element)
    if idx2 < len(lst2):
        for element in lst2[idx2:]:
            lst.append(element)
    return lst
