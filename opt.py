def get_tags_from_parts(parts: list[int], tags: list[int]):
    # IT IS MANDATORY THAT PARTS[0] = 0
    for i in range(len(parts) - 1):
        part = parts[i+1] - parts[i]
        while part:
            tags.append(i)
            part -=1

def raster_dict(d: dict[str, list], data: list, tags: list[str]):
    i = 0
    for values in d.values():
        data.extend(values)
        tags.extend([i for _ in values])
        i += 1


def getcombos(data: list, labels: list[int], udata: list, combos: list):
    for (d, l) in zip(data, labels):
        if d not in udata:
            udata.append(d)
            combos.append(2 ** l)
        else:
            combos[udata.index(d)] += 2 ** l

def recombine(udata: list, combos: list[int], data: list, tags: list[int]):
    for i in range(max(combos).bit_length()):
        for j, d in enumerate(udata):
            if combos[j] & 2**i:
                tags.append(i)
                data.append(d)


def cstring(string, fcolor):
    INIT_FOREGROUND = '\033[38;5;'
    STOPPER = 'm'
    TERMINATOR = '\033[0;0m'
    return f"{INIT_FOREGROUND}{fcolor}{STOPPER}{string}{TERMINATOR}"

def debug(udata: list, combos: list[int]):
    UPPER = len(str(max(udata)))

    
    print(
        '\n'.join(' ' * (len(str(UPPER)) + 2) + ' '.join(
            str(n).zfill(UPPER)[i] for n in udata
        ) for i in range(UPPER))
    )

    UPPER = max(combos).bit_length()
    for i in range(UPPER):
        row = [str(i) + ' ' * (len(str(UPPER)) - len(str(i)) + 1)]
        for j, d in enumerate(udata):
            if combos[j] & 2**i:
                row.append(cstring('\u2593' * 2, combos[j] % (2**8-1)))
            else:
                row.append(' ' * 2)
        print(''.join(row))


if __name__ == "__main__":
    from random import randint, choice
    #data = [1, 2, 4, 6, 7, 9, 2, 3, 4, 5, 6, 7, 9, 1, 4, 5, 6, 7, 8]
    #parts = [0, 6, 12, 19]
    #
    #tags = []
    #get_tags_from_parts(parts, tags)
    #
    #udata, combos = [], []
    #getcombos(data, tags, udata, combos)
    #
    #trace = sorted(range(len(combos)), key=lambda i: combos[i])
    #udata[:] = [udata[i] for i in trace]
    #combos[:] = [combos[i] for i in trace]
    #
    #data, tags = [], []
    #recombine(udata, combos, data, tags)
    #
    #debug(udata, combos)

    d = {
        "health":       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "position":     [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "icon":         [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "sprite":       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "agility":      [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
        "velocity":     [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
        "experience":   [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
        "agility":      [1, 2, 3, 5, 6, 7, 8, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48],
        "attack":       [1, 3, 5, 6, 7, 8, 9, 12, 13, 14, 16, 18, 20, 21, 22, 24, 25, 27, 28, 30, 34, 35, 36, 37, 38, 39, 40, 41, 44, 45, 46, 47, 48],
        "resistance":   [2, 3, 5, 7, 9, 11, 12, 13, 16, 17, 18, 20, 21, 22, 23, 24, 25, 28, 30, 31, 33, 34, 35, 40, 41, 44, 46],
        "regeneration": [5, 6, 9, 11, 12, 13, 15, 16, 20, 22, 23, 28, 35, 39, 40, 45, 46],
        "onara":        [7, 8, 9, 15, 21, 24, 28, 30, 35, 38, 40, 43, 44, 46, 48],
        "magic":        [5, 6, 9, 11, 16, 24, 27, 29, 30, 33, 39, 41, 44],
        "cursed":       [3, 9, 17, 18, 24, 28, 38],
        "lighting":     [0, 4, 10, 19, 32, 49],
        "blessed":      [13, 24, 26, 43],
    }
    
    data, tags = [], []
    raster_dict(d, data, tags)
    
    udata, combos = [], []
    getcombos(data, tags, udata, combos)
    
    trace = sorted(range(len(combos)), key=lambda i: combos[i])
    udata[:] = [udata[i] for i in trace]
    combos[:] = [combos[i] for i in trace]
    
    debug(udata, combos)
