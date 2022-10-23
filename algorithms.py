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
        for j in range(0, len(S)):  # Scans over every point
            if (endpoint == pointOnHull) or (sidedness(DLine(P[i], endpoint), S[j]) > 0):
                endpoint = S[j]
        i = i+1
        pointOnHull = endpoint

        # End Condition
        if endpoint == P[0]:
            loop = False

    return P
