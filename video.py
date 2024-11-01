from dataclasses import dataclass, field
from typing import Any, Hashable, Callable



def hiker(maze: dict, start: str) -> list[list[str]]:
    output = []
    path = [start]
    space = [maze[start]]
    plan = [[door for door in space[-1]]]
    while plan:
        print("path:", path)
        print("plan:", plan, '\n')
        # Door?
        for door in plan[-1]:
            # Why is it called room?
            room = space[-1][door]
            if isinstance(room, dict):
                # Why looking for the element to remove, it always first
                plan[-1].remove(door)
                path.append(door)
                space.append(room)
                plan.append(list(room.keys()))
                break
            # Why not else
            elif isinstance(room, bool):
                if room == True:
                    plan[-1] = []
                    output.append(path.copy() + [door])
                # Why not else?
                elif room == False:
                    plan[-1].remove(door)
                # Three nested loops???
                while True:
                    if plan and plan[-1] == []:
                        del plan[-1]
                        del space[-1]
                        del path[-1]
                    else:
                        break
    return output


def hiker2(d: dict, start: str) -> list[list[str]]:
    output = []
    path = [start]
    references = [d[start]]
    unvisited = [[tag for tag in references[-1]]]
    while unvisited:
        print("path:", path)
        print("unvisited:", unvisited, '\n')

        # Out of the for loop
        if unvisited and unvisited[-1] == []:
            del path[-1]
            del references[-1]
            del unvisited[-1]
            continue

        for tag in unvisited[-1]:
            del unvisited[-1][0]
            next = references[-1][tag]
            if isinstance(next, dict):
                references.append(next)
                path.append(tag)
                unvisited.append(list(next.keys()))
                break
            elif next == True:
                unvisited[-1].clear()
                output.append(path.copy() + [tag])

    return output


def hiker3(d: dict, matcher: Callable[str, bool], start) -> list[list[str]]:
    output = []

    path = [start]
    references = [d[start]]
    unvisited = [[tag for tag in references[-1]]]
    while unvisited:

        if len(unvisited) > 0 and unvisited[-1] == []:
            # Redundant del
            del path[-1]
            del references[-1]
            del unvisited[-1]
            continue

        # Frequently accessing last element 3 times
        for tag in unvisited[-1]:
            del unvisited[-1][0]
            next = references[-1][tag]
            if isinstance(next, dict):
                references.append(next)
                path.append(tag)
                unvisited.append(list(next.keys()))
                break
            # Custom matching function
            elif matcher(next):
                unvisited[-1].clear()
                output.append(path.copy() + [tag])

    return output



@dataclass(slots=True)
class Node:
    tag: Hashable
    reference: dict
    unvisited: list[Hashable]


def hiker4(d: dict, matcher: Callable[str, bool], start) -> list[list[str]]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, d[start], list(d[start].keys()))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        # Nodes with no unvisited tags can be removed
        if len(nodes) > 0 and node.unvisited == []:
            del nodes[-1]
            continue
        for tag in node.unvisited:
            # Un-optimal deleting
            del node.unvisited[0]
            next = node.reference[tag]
            if isinstance(next, dict):
                nodes.append(Node(tag, next, list(next.keys())))
                break
            elif matcher(next):
                node.unvisited.clear()
                output.append([_.tag for _ in nodes] + [tag])
                
    return output


def hiker5(d: dict, matcher: Callable[str, bool], start) -> list[list[str]]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, d[start], list(d[start].keys()))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while len(node.unvisited) > 0:
            tag = node.unvisited.pop()
            next = node.reference[tag]
            if isinstance(next, dict):
                nodes.append(Node(tag, next, list(next.keys())))
                break
            elif matcher(next):  # More flexible matcher
                output.append([_.tag for _ in nodes] + [tag])
                
    return output


def hiker6(d: dict, matcher: Callable[[Hashable, Any], bool], start) -> list[list[str]]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, d[start], list(d[start].keys()))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while len(node.unvisited) > 0:
            print([_.tag for _ in nodes], [_.unvisited for _ in nodes])
            tag = node.unvisited.pop()
            next = node.reference[tag]
            if matcher(tag, next):
                output.append([_.tag for _ in nodes] + [tag])
            elif isinstance(next, dict):  # Support for lists?
                nodes.append(Node(tag, next, list(next.keys())))
                break
    return output


def hiker7(d: dict, matcher: Callable[[Hashable, Any], bool], start) -> list[list[str]]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, d[start], list(d[start].keys()))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while node.unvisited:
            tag = node.unvisited.pop()
            next = node.reference[tag]
            if matcher(tag, next):
                output.append([_.tag for _ in nodes] + [tag])
            # Can i condense this?
            elif isinstance(next, list):
                nodes.append(Node(tag, next, list(range(len(next)))))
                break
            elif isinstance(next, dict):
                nodes.append(Node(tag, next, list(next.keys())))
                break
    return output











def plan(obj):
    if isinstance(obj, list):
        return list(range(len(obj)))
    elif isinstance(obj, dict):
        return list(obj.keys())
    else:
        return list()


def hiker8(d: dict, matcher: Callable[[Hashable, Any], bool], start) -> list[list[str]]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, d[start], list(d[start].keys()))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while node.unvisited:
            tag = node.unvisited.pop()
            next = node.reference[tag]
            if matcher(tag, next):
                output.append([_.tag for _ in nodes] + [tag])
            elif (unvisited := plan(next)) is not None:
                nodes.append(Node(tag, next, unvisited))
                break
    return output


def hiker9(d: dict, matcher: Callable[[Hashable, Any], bool], start) -> list[list[str]]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, d[start], list(d[start].keys()))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while node.unvisited:
            tag = node.unvisited.pop()
            next = node.reference[tag]
            nodes.append(Node(tag, next, plan(next)))
            if matcher(tag, next):
                output.append([_.tag for _ in nodes])
            break
    return output


def hiker10(obj, forward: Callable, choices: Callable, matching: Callable[[...], bool], start) -> list[list]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, forward(obj, start), choices(forward(obj, start)))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while node.unvisited:
            tag = node.unvisited.pop()
            next = forward(node.reference, tag)
            nodes.append(Node(tag, next, choices(next)))
            if matching(tag, next):
                output.append([_.tag for _ in nodes])
            break
    return output



@dataclass(slots=True)
class Node:
    state: Any
    system: object
    unvisited: list


def hiker11(obj, goto: Callable, choices: Callable, matching: Callable[[...], bool], start) -> list[list]:
    output: list[list[str]] = []
    nodes: list[Node] = [Node(start, goto(obj, start), choices(goto(obj, start)))]
    while len(nodes) > 0:
        node: Node = nodes[-1]
        if not node.unvisited:
            del nodes[-1]
            continue
        while node.unvisited:
            state = node.unvisited.pop()
            next = goto(node.system, state)
            nodes.append(Node(state, next, choices(next)))
            if matching(state, next):
                output.append([_.state for _ in nodes])
            break
    return output


@dataclass(slots=True, frozen=True)
class Hiker:
    goto: Callable
    choices: Callable

    def __call__(self, obj, matching: Callable[[...], bool], start) -> list[list]:
        output = []                                                           # Definire uno spazio per i risultati.
        system = self.goto(obj, start)                                        # Definire il sistema di partenza.
        unvisited = self.choices(system)                                      # Definire gli stati non ancora visitati.
        stack = [Hiker.Node(start, system, unvisited)]                        # Definire una pila di dati.
        while stack:                                                          # Mentre la pila non e' vuota
            head = stack[-1]                                                  # si accede ai dati in cima.
            print([_.state for _ in stack], [_.unvisited for _ in stack])     # Disegnare sul display dei dati (non necessario).
            if not head.unvisited:                                            # Se tutti gli stati in cima alla pila sono stati visitati
                del stack[-1]                                                 # rimuovere questi dati e
                continue                                                      # riaccedere alla nuova cima della pila.
            _state = head.unvisited.pop()                                     # Accedere ad uno dei prossimi stati visitabili (visitandoli).
            _system = self.goto(head.system, _state)                          # Definire il sistema associato allo stato visitato.
            stack.append(Hiker.Node(_state, _system, self.choices(_system)))  # Aggiungere alla pila questi dati.
            if matching(_system):                                             # Se il sistema ha delle proprieta' desiderate.
                output.append([item.state for item in stack])                 # si aggiunge il cammino degli stati percorsi fino ad ora ai risultati.
        return output                                                         # Finita la pila dei dati si riportano i risultati ottenuti.

    @dataclass(slots=True)
    class Node:
        state: object
        system: object
        unvisited: list


dict_hiker = Hiker(
    lambda d, k: d[k],
    lambda obj: list(range(len(obj))) if isinstance(obj, list)        # plan()
                     else (list(obj.keys()) if isinstance(obj, dict)  #
                           else list())                               #
)


if __name__ == "__main__":

    MAZE = {'A': {'B': {'D': {'G': False, 'H': {'J': {'M': True}}}, 'E': True}, 'C': False}}
    print(dict_hiker(MAZE, lambda v: type(v) == bool and v == True, 'A'))
