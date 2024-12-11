def get_tags_from_parts(parts: list[int], tags: list[int]):
    # IT IS MANDATORY THAT PARTS[0] = 0
    for i in range(len(parts) - 1):
        part = parts[i+1] - parts[i]
        while part:
            tags.append(i)
            part -=1

def compress(data: list, tags: list[int], udata: list, combos: list[int]):
    for i, d in enumerate(data):
        if d not in udata:
            udata.append(d)
            combos.append(2 ** tags[i])
        else:
            combos[udata.index(d)] += 2 ** tags[i]

def compress_dict(data: dict[str, list], udata: list, combos: list[str]):
    _data, _tags = [], []
    i = 0
    for values in data.values():
        _data.extend(values)
        _tags.extend([i for _ in values])
        i += 1
    
    compress(_data, _tags, udata, combos)

def decompress(udata: list, combos: list[int], data: list, tags: list[int]):

    def get_tag(n: int, l: list):
        while n > 0:
            l.append(n % 2)
            n //= 2
        l[:] = [t * i for i, t in enumerate(l) if t]

    raise NotImplementedError("Check later, this site is under construction...")


if __name__ == "__main__":
    from random import randint, choice
    data = [1, 2, 4, 6, 7, 9, 2, 3, 4, 5, 6, 7, 9, 1, 4, 5, 6, 7, 8]
    parts = [0, 6, 12, 19]

    tags = []
    get_tags_from_parts(parts, tags)

    udata, combos = [], []
    compress(data, tags, udata, combos)

    print(udata, combos, sep='\n')

    data = {
        'atk': [2, 1, 7, 4, 5, 3],
        'def': [7, 1, 4, 5, 2, 3],
        'spd': [7, 2, 1, 4, 5, 3],
        'flight': [7, 5, 3],
        'curse': [3, 1],
        'animal': [7, 5]
    }

    udata, combos = [], []
    compress_dict(data, udata, combos)

    print(udata, combos, sep='\n')
