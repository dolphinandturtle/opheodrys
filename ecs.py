from dataclasses import dataclass
from random import randint, random
from typing import Tuple, Any


@dataclass(slots=True)
class Component:
    ids: list[int]
    data: list[Any]

    
def cstring(string, fcolor=None, bcolor=None):
    '''Color id's span from 1 to 255'''
    init_background = '\033[48;5;'
    init_foreground = '\033[38;5;'
    stopper = 'm'
    terminator = '\033[0;0m'
    if fcolor is not None or bcolor is not None:
        string += terminator
    if fcolor is not None:
        foreground = init_foreground + str(fcolor) + stopper
        string = foreground + string
    if bcolor is not None:
        background = init_background + str(bcolor) + stopper
        string = background + string
    return string


def get_components_random(count_id: int, count_component: int) -> list[Component]:
    ASCII_RANGE = 48, 123
    LENGHT_WORD = 10
    THRESHOLD_SPARSITY = .7
    output = []
    while count_component:
        ids_random = [i for i in range(count_id) if random() > THRESHOLD_SPARSITY]
        values_random = [i * random() for i in ids_random]
        output.append(Component(ids_random, values_random))
        count_component -= 1
    return output

def get_ids(system: list[Component]) -> list[int]:
    output = set()
    for component in system:
        output |= set(component.ids)
    return list(sorted(output))

def pretty_entropy_map(system: list[Component]):
    LENGHT_MAX = len(str(len(system)))
    ids = get_ids(system)
    return '\n'.join(''.join('\u2593' if i in component.ids else ' ' for i in ids) for component in system)

def get_entropy_map(system: list[Component]) -> dict[int, list[int]]:
    return {id: [i for i, component in enumerate(system) if id in component.ids]
            for id in get_ids(system)}

def optimize(system: list[Component]) -> list[list[Component]]:
    emap = get_entropy_map(system)
    archetypes = {}
    for id, partition in emap.items():
        if tuple(partition) in archetypes:
            archetypes[tuple(partition)].append(id)
        elif partition:
            archetypes[tuple(partition)] = [id]

    return [[Component(ids, [system[i].data[system[i].ids.index(id)] for id in ids])
             for i in indeces] for indeces, ids in archetypes.items()]


count_id = 100
count_component = 3
c = get_components_random(count_id, count_component)
print(pretty_entropy_map(c))
#print(get_entropy_map(c))

o = optimize(c)
#print(*o, sep='\n')
o.sort(key=lambda s: len(s[0].ids), reverse=True)
print(*[pretty_entropy_map(s) for s in o[:10]], sep='\n')
print(count_id * count_component, '->', count_id)
