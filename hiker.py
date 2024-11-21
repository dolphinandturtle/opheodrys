import os
from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class Node:
    state: object
    system: object
    unvisited: list

@dataclass(slots=True, frozen=True)
class Hiker:
    goto: Callable
    choices: Callable

    def __call__(self, obj, matching: Callable[[...], bool], start) -> list[list]:
        output = []
        system = self.goto(obj, start)
        stack = [Node(start, system, self.choices(system))]
        while stack:
            head = stack[-1]
            #print([_.state for _ in stack], [_.unvisited for _ in stack])
            if not head.unvisited:
                del stack[-1]
                continue
            _state = head.unvisited.pop()
            _system = self.goto(head.system, _state)
            stack.append(Node(_state, _system, self.choices(_system)))
            if matching(_system):
                output.append([item.state for item in stack])
        return output


dict_hiker = Hiker(
    lambda d, k: d[k],
    lambda obj: list(range(len(obj))) if isinstance(obj, list)
                     else (list(obj.keys()) if isinstance(obj, dict)
                           else list())
)
file_hiker = Hiker(
    lambda d, k: f"{d.rstrip('/')}/{k.rstrip('/')}",
    lambda obj: os.listdir(obj) if os.path.isdir(obj) else []
)


if __name__ == "__main__":

    #MAZE = {'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True}}}, 'E': True}, 'C': False}}
    #print(dict_hiker(MAZE, lambda v: type(v) == bool and bool(v), 'A'))


    import json
    d = json.load(open("large-file.json", "r"))
    output = []
    for i in range(len(d)):
        output += dict_hiker(d, lambda v: isinstance(v, str) and "Event" in v, i)
    print(output)

    #print(file_hiker('/home/user/', lambda v: isinstance(v, str) and "bsterthegawd" in v, ''))
