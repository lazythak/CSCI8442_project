from typing import List
from primitives import *


def leftmost(S: List[Point]) -> Point:
    left = S[0]
    for p in S[1:]:
        if p.x < left.x:
            left = p

    return left


def rightmost(S: List[Point]) -> Point:
    right = S[0]
    for p in S[1:]:
        if p.x > right.x:
            right = p

    return right


def quickhull(S: List[Point]) -> List[Point]:
    P = []
    a = leftmost(S)
    b = rightmost(S)
    S1 = []
    S2 = []
    for p in S:
        if sidedness_i(DLine(a, b), p) == -1:
            S1.append(p)
        elif sidedness_i(DLine(b, a), p) == -1:
            S2.append(p)
    P.append(a)
    DD = findquickhull(S1, a, b)
    if len(DD) > 0:
        P = P+DD
    P.append(b)
    DD = findquickhull(S2, b, a)
    if len(DD) > 0:
        P = P+DD
    return P


def findquickhull(S: List[Point], a, b) -> List[Point]:
    P = []
    if len(S) == 0:
        return []
    else:
        farthest = S[0]
        for p in S:
            if area(p, a, b) > area(farthest, a, b):
                farthest = p
        S1 = []
        S2 = []
        for p in S:
            if sidedness_i(DLine(a, farthest), p) == -1:
                S1.append(p)
            elif sidedness_i(DLine(farthest, b), p) == -1:
                S2.append(p)

        DD = findquickhull(S1, a, farthest)
        if len(DD) > 0:
            P = P+DD
        P.append(farthest)
        DD = findquickhull(S2, farthest, b)
        if len(DD) > 0:
            P = P+DD
        return P


if __name__ == '__main__':
    S = [Point(-1, 0), Point(0, 1), Point(-1/math.sqrt(2), -
                                          1/math.sqrt(2)), Point(0, -1), Point(1, 0)]
    print(quickhull(S))
