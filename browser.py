import os
from dataclasses import dataclass
from typing import Hashable, Callable
import functools
import threading


'''
@dataclass(slots=True, frozen=True)
class Node:
    parent: object
    current: object
    children: list[object]
'''

@dataclass(slots=True)
class Node:
    reference: object
    system: object
    unvisited: list


def diverge(obj, from_to: Callable, options: Callable, call: Callable):
    stack = [Node(None, obj, options(obj))]
    while stack:
        head = stack[-1]
        if head.unvisited:
            _reference = head.unvisited.pop()
            _system = from_to(head.system, _reference)
            stack.append(Node(_reference, _system, options(_system)))
            call(_system)
        else:
            del stack[-1]
    return



@dataclass(slots=True)
class Node:
    reference: object
    system: object
    branches: int

    def propagate(self, goto, next, unvisited):
        self.branches -= 1
        reference = unvisited.pop()
        system = goto(self.system, reference)
        branches = len(unvisited)
        unvisited.extend(next(system))
        return Node(reference, system, len(unvisited) - branches)


def converge(obj, goto: Callable, next: Callable, call: Callable):
    unvisited = next(obj)
    stack = [Node(None, obj, len(unvisited))]
    while stack:
        head = stack[-1]
        if head.branches:
            stack.append(head.propagate(goto, next, unvisited))
        else:
            call(head.system)
            del stack[-1]
    return


def doublewalk(obj, from_to: Callable, options: Callable, headcall: Callable, tailcall: Callable):
    stack = [Node(None, obj, options(obj))]
    while stack:
        head = stack[-1]
        if head.unvisited:
            _reference = head.unvisited.pop()
            _system = from_to(head.system, _reference)
            stack.append(Node(_reference, _system, options(_system)))
            headcall(_system)
        else:
            tailcall(head.system)
            del stack[-1]
    return


def multi_sleepwalk(obj, from_to: Callable, options: Callable, call: Callable, thread_count: int = 4):
    ARGS_FIXED = [from_to, options, call, thread_count]
    stack = [Node(None, obj, options(obj))]
    while stack:
        head = stack[-1]
        if head.unvisited:
            _reference = head.unvisited.pop()
            _system = from_to(head.system, _reference)
            if threading.active_count() < thread_count:
                threading.Thread(
                    target=multi_sleepwalk,
                    args=[_system] + ARGS_FIXED,
                ).start()
            else:
                stack.append(Node(_reference, _system, options(_system)))
        else:
            call(head.system)
            del stack[-1]
    return


def walk(obj, goto: Callable, options: Callable, call: Callable, output: dict[Hashable, Node]):
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
        output.append(call(_system))
        steps.append(stack[1:])
    return



#@dataclass(slots=True)
#class Node:
#    state: object
#    system: object
#    unvisited: list


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

    MAZE = {'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True, 'Z': False}}}, 'E': True}, 'C': False}}
    from time import sleep
    def slow_print(*args, **kwargs):
        #sleep(1.5)
        return print(*args, **kwargs)
    #converge(MAZE, map_goto, map_options, slow_print)
    multi_sleepwalk(MAZE, map_goto, map_options, slow_print)

    '''
    def find_bster(v):
        if isinstance(v, str) and "bsterthegawd" in v:
            print(v)

    multi_sleepwalk('/', path_goto, path_options, find_bster, thread_count=20)
    '''

    #MAZE = DictBrowser({'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True}}}, 'E': True}, 'C': False}})
    #print(MAZE.find_all(lambda v: type(v) == bool and bool(v)))


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
