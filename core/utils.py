def list_to_columns(l: list, columns: int) -> list[list]:
    '''
    Converts list of items to list of list of items
    Example:
    l = [1, 2, 3, 4, 5], columns = 3
    result: [ [1, 2, 3], [4, 5] ]
    '''
    res = [[]]
    counter = 0

    for i in l:
        if counter < columns:
            res[-1].append(i)
        else:
            res.append([i])
            counter = 0
        counter += 1

    return res
