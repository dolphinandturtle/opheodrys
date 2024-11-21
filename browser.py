import os
from dataclasses import dataclass
from typing import Callable
import functools


@dataclass(slots=True, frozen=True)
class Node:
    depth: int
    parent: object
    children: list[object]


def sleepwalk(obj, goto: Callable, options: Callable, call: Callable):
    stack = [Node(None, obj, options(obj))]
    while stack:
        head = stack[-1]
        if not head.unvisited:
            del stack[-1]
            continue
        _state = head.unvisited.pop()
        _system = goto(head.system, _state)
        stack.append(Node(_state, _system, options(_system)))
        call(_state, _system)
    return


def walk(obj, goto: Callable, options: Callable, call: Callable, output: list):
    steps = []
    stack = [Node(None, obj, options(obj))]
    while stack:
        head = stack[-1]
        if not head.unvisited:
            del stack[-1]
            continue
        _state = head.unvisited.pop()
        _system = goto(head.system, _state)
        stack.append(Node(_state, _system, options(_system)))
        output.append(call(_state, _system))
        steps.append(stack[1:])
    return


@dataclass(slots=True)
class Node:
    state: object
    system: object
    unvisited: list


def browser(cls, goto: Callable, options: Callable):

    @functools.wraps(cls, updated=())
    class Wrapper(cls):

        def find_all(self, matching: Callable[[...], bool]) -> list[list]:
            output = []
            stack = [Node(None, self, options(self))]
            while stack:
                head = stack[-1]
                if not head.unvisited:
                    del stack[-1]
                    continue
                _state = head.unvisited.pop()
                _system = goto(head.system, _state)
                stack.append(Node(_state, _system, options(_system)))
                if matching(_system):
                    output.append([item.state for item in stack[1:]])
            return output

    return Wrapper


def map_goto(y, x):
    return y[x]

def map_options(y):
    if isinstance(y, list):
        return list(range(len(y)))
    elif isinstance(y, dict):
        return list(y.keys())
    else:
        return []


def path_goto(root, path):
    return f"{root.rstrip('/')}/{path.rstrip('/')}"

def path_options(path):
    if os.path.isdir(path):
        return os.listdir(path)
    else:
        return []


class Table(dict):

    def __init__(self, source: list | dict):
        if isinstance(source, list):
            super().__init__(zip(source, range(len(source))))
        else:
            super().__init__(source)


ListBrowser = browser(list, map_goto, map_options)
DictBrowser = browser(dict, map_goto, map_options)
TableBrowser = browser(Table, map_goto, map_options)
PathBrowser = browser(str, path_goto, path_options)


if __name__ == "__main__":


    MAZE = DictBrowser({'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True}}}, 'E': True}, 'C': False}})
    print(MAZE.find_all(lambda v: type(v) == bool and bool(v)))


    '''
    import json
    l = ListBrowser(json.load(open("large-file.json", "r")))
    o = l.find_all(lambda v: isinstance(v, str) and "Event" in v)
    print(o)
    '''

    '''
    file_path = browser(str, goto_file, options_file)('/home/user/')
    o = file_path.find_all(lambda v: isinstance(v, str) and "bsterthegawd" in v)
    print(o)
    '''
