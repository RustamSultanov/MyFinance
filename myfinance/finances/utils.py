months = {
    1: 'January',
    2: 'February',
    3: 'March',
    4: 'April',
    5: 'May',
    6: 'June',
    7: 'July',
    8: 'August',
    9: 'September',
    10: 'October',
    11: 'November',
    12: 'December'
}


def get_month_name(month):
    return months[month]


def get_elem(arr, el):
    for elem in arr:
        key, val = elem
        if key == el:
            return True
    return False


def get_index(arr, el):
    i = 0
    for elem in arr:
        fst, snd = elem
        if fst == el:
            return i
        i = i + 1
    return None

def get_annual(arr, el):
    res = []
    for elem in arr:
        year, months = elem
        if year == el:
            res = months
    return res

def transform_data(variables, acc=None):
    if len(variables) == 0:
        return acc
    else:
        year, month, total = variables.pop(-1)
        if acc is None:
            acc = [[year, [[get_month_name(month), total]]]]
        else:
            if get_elem(acc, year):
                months = get_annual(acc, year)
                if not get_elem(months, get_month_name(month)):
                    acc[get_index(acc, year)][1].append([get_month_name(month), total])
            else:
                acc.append([year, [[get_month_name(month), total]]])
        return transform_data(variables, acc)
