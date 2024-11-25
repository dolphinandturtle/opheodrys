from typing import Callable
from dataclasses import dataclass
from threading import Thread, active_count



# one-to-one

def flatten(obj, from_to: Callable, next: Callable, output: list):
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        #print(breaks, buffered)
        print(buffered, breaks, path)
        breaks[-1] -= 1
        step = from_to(path[-1], buffered.pop())
        discovered = next(step)
        if not breaks[-1]:
            del path[-1]
            del breaks[-1]
        if not discovered:
            output.append(step)
        else:
            path.append(step)
            breaks.append(len(discovered))
            buffered.extend(discovered)
    return





def analyze(obj, from_to: Callable, next: Callable):
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        print(buffered, breaks)
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            if step not in path:
                discovered = next(step)
                path.append(step)
                breaks.append(len(discovered))
                buffered.extend(discovered)
        else:
            del path[-1]
            del breaks[-1]
    return


def multi_converge(obj, from_to: Callable, next: Callable, finite: list, loops: list, thread_count: int = 4):
    ARGS_FIXED = [from_to, next, call, finite, loops, thread_count]
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            if active_count() < thread_count:
                Thread(target=multi_converge, args=[step]+ARGS_FIXED).start()
            elif step in path:
                loops.append(path.copy())
            else:
                discovered = next(step)
                path.append(step)
                breaks.append(len(discovered))
                buffered.extend(discovered)
        else:
            finite.append(path.copy())
            del path[-1]
            del breaks[-1]
    return


if __name__ == "__main__":

    def map_goto(y, x):
        return y[x]

    def map_options(y):
        if isinstance(y, list):
            return list(range(len(y)))
        elif isinstance(y, dict):
            return list(y.keys())
        else:
            return []

    MAZE = {'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True, 'Z': False}}}, 'E': True}, 'C': False}}
    o = []
    flatten(MAZE, map_goto, map_options, o)
    print(o)
