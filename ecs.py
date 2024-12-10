from random import randint, random
from typing import Tuple, Any


def get_components_random(count_id: int, count_component: int):
    seed_ids = [[i for i in range(count_id) if random() > .6] for _ in range(count_component)]
    return {''.join(chr(randint(48, 123)) for _ in range(randint(0, 10))): {
        'ids': seed_ids[_],
        'values': [i * random() for i in seed_ids[_]]
    } for _ in range(count_component)}

def get_id_max(components: dict):
    return max([max(value['ids']) for value in components.values() if value['ids']])

def pretty_entropy_map(components: dict):
    len_type_max = max(map(len, components)) + 1
    id_max = get_id_max(components)
    grid_id = ' '.join(map(str, range(id_max + 1)))
    output = ' ' * len_type_max + grid_id + '\n'
    output += ' ' * len_type_max + '-' * len(grid_id) + '\n'
    for key, data in components.items():
        output += key
        output += ' ' * (len_type_max - len(key))
        output += ' '.join('1' if i in data['ids'] else '0' for i in range(id_max + 1))
        output += '\n'
    return output

def get_entropy_map(components: dict):
    id_max = get_id_max(components)
    return {id: [key for key, data in components.items() if id in data['ids']] for id in range(id_max + 1)}


def optimize(components: dict) -> list[dict]:
    emap = get_entropy_map(components)
    archetypes = {}
    for key, partition in emap.items():
        if tuple(partition) in archetypes:
            archetypes[tuple(partition)].append(key)
        elif partition:
            archetypes[tuple(partition)] = [key]

    return [{key: {'ids': ids,
                   'values': [components[key]['values'][components[key]['ids'].index(i)] for i in ids]}
             for key in keys} for keys, ids in archetypes.items()]




c = get_components_random(30, 3)
print(pretty_entropy_map(c))
#print(get_entropy_map(c))

o = optimize(c)
#print(*o, sep='\n')
print(*list(map(pretty_entropy_map, o)), sep='\n')
