from typing import List, Tuple
from primitives import *


# Helpers

def leftmost(S: List[Point]) -> Point:
    left = S[0]
    for p in S[1:]:
        if (p.x, p.y) < (left.x, left.y):
            left = p

    return left


def rightmost(S: List[Point]) -> Point:
    right = S[0]
    for p in S[1:]:
        if (p.x, p.y) > (right.x, right.y):
            right = p

    return right


def leftmostWithInd(S: List[Point]) -> Tuple[Point, int]:
    left = S[0]
    left_ind = 0
    for j in range(1, len(S)):
        if S[j].x < left.x:
            left = S[j]
            left_ind = j

    return left, left_ind


def rightmostWithInd(S: List[Point]) -> Tuple[Point, int]:
    right = S[0]
    right_ind = 0
    for j in range(1, len(S)):
        if S[j].x >= right.x:
            right = S[j]
            right_ind = j

    return right, right_ind


# Jarvis

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


# Andrew's

def andrew(S: List[Point]) -> List[Point]:
    if len(S) <= 1:
        # Cover the case where the input set has one or zero points
        return S.copy()

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


# Chan's

def partition_list(S: List, size: int) -> List[List]:
    return [S[i: i + size] for i in range(0, len(S), size)]


def subhull_rightmost(S: List[List[Point]]) -> Tuple[int, int]:
    """Calculates and returns the index into S of the rightmost point

    Args:
        S (List[List[Point]]): A list of convex hulls, where each hull is represented by its own list

    Returns:
        Tuple[int, int]: (h, p), the index h into S, and the index p into S[h], where S[h][p] is the rightmost point in S
    """
    rh = 0
    ri = 0
    for (hi, hull) in enumerate(S):
        for (pi, p) in enumerate(hull):
            if (p.x, p.y) > (S[rh][ri].x, S[rh][ri].y):
                rh = hi
                ri = pi

    return (rh, ri)


def below(c: Point, to: Point, frm: Point) -> bool:
    return angular_about_point(c, to, frm) > 0


def above(c: Point, to: Point, frm: Point) -> bool:
    return angular_about_point(c, to, frm) < 0


def to_points(P: List[Tuple[int, int]], SH: List[List[Point]]) -> List[Point]:
    out = []
    for (h, p) in P:
        out.append(SH[h][p])
    return out


def rtangent(v: List[Point], p: Point) -> int:
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
    if n == 1:
        # case to handle when v is of size 1
        print("Size 1 hull, short-circuit")
        return 0

    print(f"tangent request: {p}")

    # right tangent is local maximum for ordering where points to left of line are lower than those on
    if (below(p, v[1], v[0]) and not above(p, v[n-1], v[0])):
        print(f"early exit, {v[0]}")
        return 0

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
            print(f"Normal exit, {v[c]}")
            return c  # v[c] is tangent

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
            return 0


def chan_step(S: List[Point], m: int, H: int) -> List[Point]:
    partitions: List[List[Point]] = partition_list(S, m)
    subhulls: List[List[Point]] = []
    for i in range(0, len(partitions)):
        subhulls.append(andrew(partitions[i]))

    print(partitions)
    print(subhulls)

    # P[0] is the rightmost point, which we know must be on the hull
    P = [subhull_rightmost(subhulls)]

    for k in range(0, H):
        q: List[Tuple[int, int]] = []  # point
        (ch, cp) = P[-1]  # hull and point indices of most recent point on hull
        for i in range(0, len(subhulls)):
            if ch == i:
                # Special case, most recent point is on this hull, get next element on this subhull
                if len(subhulls[i]) != 1:
                    # If the size is one, then that's the point we're currently at. Don't want to
                    # get the current point, so just skip this subhull in this case
                    q.append((i, (cp + 1) % len(subhulls[i])))
            else:
                q.append((i, rtangent(subhulls[i], subhulls[ch][cp])))

        # append point with max angle from q, use step of jarvis march
        (eh, ep) = q[0]
        for (ph, pp) in q:
            (ch, cp) = P[-1]
            if (subhulls[eh][ep] == subhulls[ch][cp]) or (sidedness(DLine(subhulls[ch][cp], subhulls[eh][ep]), subhulls[ph][pp]) < 0):
                eh = ph
                ep = pp
        P.append((eh, ep))
        print(q)
        print(f"Added {subhulls[eh][ep]} to hull.\n")

        if P[-1] == P[0]:
            return to_points(P[0:-1], subhulls)

    return []  # "incomplete"


def chan(S: List[Point]) -> List[Point]:
    for t in range(1, len(S)):
        print(f"~~~~Step: {t}~~~~~~~~~")
        m = min(len(S), pow(2, pow(2, t)))
        L = chan_step(S, m, m)
        if L != []:
            return L
    return []  # Error case, should never be reached


# Quickhull

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


# Divide and Conquer

def combine(S1, S2):
    # Upper half
    p1, i1 = rightmostWithInd(S1)
    p2, i2 = leftmostWithInd(S2)

    go_on = True
    while go_on:
        go_on = False
        while True:
            if sidedness_i(DLine(S1[i1], S2[i2]), S2[(i2-1) % len(S2)]) == 1:
                go_on = True
                i2 = (i2-1) % len(S2)
            else:
                break

        while True:
            if sidedness_i(DLine(S2[i2], S1[i1]), S1[(i1+1) % len(S1)]) == -1:
                go_on = True
                i1 = (i1+1) % len(S1)
            else:
                break
    left_up = i1
    right_up = i2

    # Lower half
    p1, i1 = rightmostWithInd(S1)
    p2, i2 = leftmostWithInd(S2)

    go_on = True
    while go_on:
        go_on = False
        while True:
            if sidedness_i(DLine(S1[i1], S2[i2]), S2[(i2 + 1) % len(S2)]) == -1:
                go_on = True
                i2 = (i2 + 1) % len(S2)
            else:
                break

        while True:
            if sidedness_i(DLine(S2[i2], S1[i1]), S1[(i1 - 1) % len(S1)]) == 1:
                go_on = True
                i1 = (i1 - 1) % len(S1)
            else:
                break
    left_down = i1
    right_down = i2

    P = []
    if left_up > left_down:
        left_down = left_down+len(S1)
    for j in range(left_up, left_down+1):
        P.append(S1[(j % len(S1))])

    if right_down > right_up:
        right_up = right_up+len(S2)
    for j in range(right_down, right_up+1):
        P.append(S2[(j % len(S2))])
    return (P)


def divideConquer(S: List[Point]) -> List[Point]:
    if len(S) <= 1:
        return S
    else:
        return combine(divideConquer(S[0:len(S)//2]), divideConquer(S[len(S)//2:len(S)]))

def divideConquer0(S: List[Point]) -> List[Point]:
    S = sorted(S, key = lambda p: p.x)
    return divideConquer(S)
