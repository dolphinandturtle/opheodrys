from typing import Callable
from dataclasses import dataclass
from threading import Thread, active_count
import os


###########
# Drivers #
###########

@dataclass(slots=True, frozen=True)
class Driver:
    visit_from: Callable
    discover: Callable


def table_visit_from(y, x):
    return y[x]

def table_discover(y):
    if isinstance(y, list):
        return list(range(len(y)))
    elif isinstance(y, dict):
        return list(y.keys())
    else:
        return []

TABLE_DRIVER = Driver(table_visit_from, table_discover)


def path_visit_from(root, path):
    return f"{root.rstrip('/')}/{path.rstrip('/')}"

def path_discover(path):
    if os.path.isdir(path):
        return os.listdir(path)
    else:
        return []

PATH_DRIVER = Driver(path_visit_from, path_discover)


#############
# Functions #
#############

class Buffer:
    """Comment:
    This object contains the same information as an
    iterated list, the reason for it is my affinity
    towards a C style implementation."""
    
    __slots__ = "data", "partitions"

    def __init__(self, data: list[object]):
        self.data = data
        self.partitions = [len(self.data)]

    @property
    def locked(self):
        return not self.partitions[-1]

    def unlock(self):
        del self.partitions[-1]

    def append(self, values: list):
        self.data.extend(values)
        self.partitions.append(len(values))

    def countdown(self):
        if self.partitions[-1]:
            self.partitions[-1] -=1
        else:
            raise Exception("Buffer underflow, out-of-bounds element popped")

    def cut(self):
        del self.data[-1]

    def use(self):
        self.countdown()
        return self.data[-1]

    def pop(self):
        self.countdown()
        return self.data.pop()


def get_tags(obj, driver: Driver, output: list):
    visited = [obj]
    unvisited = Buffer(driver.discover(obj))
    output.extend(unvisited.data)
    while unvisited.data:
        # Visit a branch
        root = driver.visit_from(visited[-1], unvisited.pop())

        # If there are not other branches to visit remove head
        if unvisited.locked:
            unvisited.unlock()
            del visited[-1]

        # If new branches are discovered visit them discover
        if branches := driver.discover(root):
            visited.append(root)
            unvisited.append(branches)
            output.extend(branches)
    return


def get_tags_multi(obj, driver: Driver, output: list, thread_count: int = 4):
    ARGS_FIXED = [driver, output, thread_count]
    threads = []

    visited = [obj]
    unvisited = Buffer(driver.discover(obj))
    output.extend(unvisited.data)
    while unvisited.data:
        # Visit a branch
        root = driver.visit_from(visited[-1], unvisited.pop())

        # If there are not other branches to visit remove head
        if unvisited.locked:
            unvisited.unlock()
            del visited[-1]

        # If no new branches are discovered, an extremity has been reached
        if not (branches := driver.discover(root)):
            continue

        # If threads are available let them handle the current head
        elif active_count() < thread_count:
            thread = Thread(target=get_tags_multi, args=[root]+ARGS_FIXED)
            threads.append(thread)
            thread.start()
        else:
            visited.append(root)
            unvisited.append(branches)
            output.extend(branches)

    for thread in threads:
        thread.join()
    return


def get_values(obj, driver: Driver, output: list):
    visited = [obj]
    unvisited = Buffer(driver.discover(obj))
    while unvisited.data:
        # Visit a branch
        root = driver.visit_from(visited[-1], unvisited.pop())

        # If there are not other branches to visit remove head
        if unvisited.locked:
            unvisited.unlock()
            del visited[-1]

        # If no new branches are discovered, an extremity has been reached
        if not (branches := driver.discover(root)):
            output.append(root)

        # If new branches are discovered, visit them discover
        else:
            visited.append(root)
            unvisited.append(branches)
    return


def get_values_multi(obj, driver: Driver, output: list, thread_count: int = 4):
    ARGS_FIXED = [driver, output, thread_count]
    threads = []

    visited = [obj]
    unvisited = Buffer(driver.discover(obj))
    while unvisited.data:
        # Visit a branch
        root = driver.visit_from(visited[-1], unvisited.pop())

        # If there are not other branches to visit remove head
        if unvisited.locked:
            unvisited.unlock()
            del visited[-1]

        # If no new branches are discovered, an extremity has been reached
        if not (branches := driver.discover(root)):
            output.append(root)

        # If threads are available let them handle the current head
        elif active_count() < thread_count:
            thread = Thread(target=get_values_multi, args=[root]+ARGS_FIXED)
            threads.append(thread)
            thread.start()
        else:
            visited.append(root)
            unvisited.append(branches)

    for thread in threads:
        thread.join()
    return


def reduce(obj, driver: Driver, call: Callable):
    visited = [obj]
    unvisited = Buffer(driver.discover(obj))
    while visited:
        if unvisited.locked:
            unvisited.unlock()
            call(visited.pop())
        else:
            root = driver.visit_from(visited[-1], unvisited.pop())
            branches = driver.discover(root)
            if branches:
                visited.append(root)
                unvisited.append(branches)
    return



if __name__ == "__main__":
    o = []

    maze = {'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True, 'Z': False}}}, 'E': True}, 'C': False}}
    get_values(maze, TABLE_DRIVER, o)
    print(o)

    #get_values_multi('/home/user/Downloads', PATH_DRIVER, o)
    #print(*o, sep='\n')
