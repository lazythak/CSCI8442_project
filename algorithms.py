from typing import List
from primitives import *


def leftmost(S: List[Point]) -> Point:
    left = S[0]
    for p in S[1:]:
        if p.x < left.x:
            left = p

    return left


def jarvis(S: List[Point]) -> List[Point]:
    pointOnHull = leftmost(S)  # linear cost scan
    i = 0
    loop = True
    P = []

    while loop:  # Runs once for each point on the hull
        P.append(pointOnHull)
        endpoint = S[0]
        for p in S:  # Scans over every point
            if (endpoint == pointOnHull) or (sidedness(DLine(P[i], endpoint), p) > 0):
                endpoint = p
        i = i+1
        pointOnHull = endpoint

        # End Condition
        if endpoint == P[0]:
            loop = False

    return P


def andrew(S: List[Point]) -> List[Point]:
    S = sorted(S, key=lambda p: (p.x, p.y))
    U = []
    L = []

    # Compute lower hull
    for p in S:
        while len(L) >= 2 and turn(L[-2], L[-1], p) >= 0:
            L.pop()
        L.append(p)

    # Compute upper hull
    for p in reversed(S):
        while len(U) >= 2 and turn(U[-2], U[-1], p) >= 0:
            U.pop()
        U.append(p)

    # remove duplicate points, last of each is the first of the other
    L.pop()
    U.pop()

    return L + U
