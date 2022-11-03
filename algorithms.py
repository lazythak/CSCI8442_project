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
            if (endpoint == pointOnHull) or (sidedness(DLine(P[i], endpoint), p) < 0):
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
        while len(L) >= 2 and turn(L[-2], L[-1], p) <= 0:
            L.pop()
        L.append(p)

    # Compute upper hull
    for p in reversed(S):
        while len(U) >= 2 and turn(U[-2], U[-1], p) <= 0:
            U.pop()
        U.append(p)

    # remove duplicate points, last of each is the first of the other
    L.pop()
    U.pop()

    return L + U


def partition_list(S: List, size: int) -> List[List]:
    return [S[i: i + size] for i in range(0, len(S), size)]


def rightmost(S: List[Point]) -> Point:
    right = S[0]
    for p in S[1:]:
        if (p.x, p.y) > (right.x, right.y):
            right = p

    return right


def below(P: Point, L1: Point, L2: Point) -> bool:
    return (L1.x - P.x) * (L2.y - P.y) - (L2.x - P.x) * (L1.y - P.y) < 0


def above(P: Point, L1: Point, L2: Point) -> bool:
    return (L1.x - P.x) * (L2.y - P.y) - (L2.x - P.x) * (L1.y - P.y) > 0


def rtangent(v: List[Point], p: Point) -> Point:
    """computes the right, or upper, tangent from p to v.
    Preconditions: v has size > 1, p on exterior of v

    Algorithm found here, and modified to fit needs:
    https://web.archive.org/web/20190714200906/http://geomalgorithms.com/a15-_tangents.html#tangent_PointPolyC()

    Args:
        v (List[Point]): convex polygon to find upper tangent on
        p (Point): point to find upper tangent from

    Returns:
        int: index of point that the tangent hits in v
    """
    n = len(v)
    print(f"tangent request: {p}")

    # right tangent is local maximum for ordering where points to left of line are lower than those on
    if (below(p, v[1], v[0]) and not above(p, v[n-1], v[0])):
        print(f"early exit, {v[0]}")
        return v[0]

    a = 0
    b = n       # initial chain = [0, n], let v[n] = v[0]
    olda = a
    oldb = b
    while True:
        c: int = (a + b) // 2                       # c is midpoint
        print(f"a: {a}, b: {b}, c: {c}")
        print(v[a:b])
        dnC = below(p, v[(c+1) % n], v[c])
        if (dnC and not above(p, v[c-1], v[c])):
            return v[c]  # v[c] is tangent

        # no max found, continue search
        # select either [a, c] or [c, b]
        upA = above(p, v[(a+1) % n], v[a])
        print(f"dnC: {dnC}, upA: {upA}")
        if (upA):
            if (dnC):
                oldb = b
                olda = a
                b = c
            else:
                if (above(p, v[a], v[c])):
                    oldb = b
                    olda = a
                    b = c
                else:
                    olda = a
                    oldb = b
                    a = c
        else:
            if not dnC:
                olda = a
                oldb = b
                a = c
            else:
                if below(p, v[a], v[c]):
                    oldb = b
                    olda = a
                    b = c
                else:
                    olda = a
                    oldb = b
                    a = c

        if (olda == a and oldb == b):
            # Error case, should not happen.
            # Known causes: p is in v, or p is colinear with all points in v
            print(".....................LOOP")
            return v[0]


def chan_step(S: List[Point], m: int, H: int) -> List[Point]:
    partitions = partition_list(S, m)
    subhulls = []
    for i in range(0, len(partitions)):
        subhulls.append(andrew(partitions[i]))

    print(partitions)
    print(subhulls)

    # P[0] is the rightmost point, which we know must be on the hull
    P = [rightmost(S)]

    for k in range(0, H):
        q = []  # point
        for i in range(0, len(subhulls)):
            q.append(rtangent(subhulls[i], P[-1]))

        # append point with max angle from q, use step of jarvis march
        endpoint = q[0]
        for potential in q:
            if (endpoint == P[-1]) or (sidedness(DLine(P[-1], endpoint), potential) < 0):
                endpoint = potential
        P.append(endpoint)
        print(q)
        print(f"Added {P[-1]} to hull.\n")

        if P[-1] == P[0]:
            return P[0:-1]

    return []  # "incomplete"


def chan(S: List[Point]) -> List[Point]:
    for t in range(1, len(S)):
        print(f"~~~~Step: {t}~~~~~~~~~")
        m = min(len(S), pow(2, pow(2, t)))
        L = chan_step(S, m, m)
        if L != []:
            return L
    return []  # Error case, should never be reached
