from typing import Callable
from dataclasses import dataclass
from threading import Thread, active_count



def analyze(obj, from_to: Callable, next: Callable, finite: list, loops: list):
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            if step in path:
                loops.append(path)
            else:
                discovered = next(step)
                path.append(step)
                breaks.append(len(discovered))
                buffered.extend(discovered)
        else:
            finite.append(path)
            del path[-1]
            del breaks[-1]
    return







def free(obj, from_to: Callable, next: Callable, output: list):
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            if step not in path:
                discovered = next(step)
                path.append(step)
                breaks.append(len(discovered))
                buffered.extend(discovered)
        else:
            output.append(path)
            del path[-1]
            del breaks[-1]
    return


def noloops(obj, from_to: Callable, next: Callable, output: list):
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            discovered = next(step)
            path.append(step)
            breaks.append(len(discovered))
            buffered.extend(discovered)
        else:
            output.append(path)
            del path[-1]
            del breaks[-1]
    return






def converge(obj, from_to: Callable, next: Callable, call: Callable):
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            path.append(step)
            discovered = next(step)
            breaks.append(len(discovered))
            buffered.extend(discovered)
        else:
            call(path.pop())
            del breaks[-1]
    return


def multi_converge(obj, from_to: Callable, next: Callable, call: Callable, thread_count: int = 4):
    ARGS_FIXED = [from_to, next, call, thread_count]
    path = [obj]
    buffered = next(obj)
    breaks = [len(buffered)]
    while path:
        if breaks[-1]:
            breaks[-1] -= 1
            step = from_to(path[-1], buffered.pop())
            if active_count() < thread_count:
                Thread(target=multi_converge, args=[step]+ARGS_FIXED).start()
            else:
                path.append(step)
                discovered = next(step)
                breaks.append(len(discovered))
                buffered.extend(discovered)
        else:
            call(path.pop())
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
    converge(MAZE, map_goto, map_options, print)
