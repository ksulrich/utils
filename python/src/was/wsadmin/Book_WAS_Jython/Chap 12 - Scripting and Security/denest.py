def denest(L):
    "De-nest a nested list"
    result = []
    for item in L:
        if type(item) == type ([]):
            result.extend(item)
        else:
            result.append(item)
    return result
