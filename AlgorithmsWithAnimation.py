from typing import List, Tuple
from primitives import *
import matplotlib.pyplot as plt
from animation_api import *

wait = 1.5


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


def scttr(S: List[Point]):
    # Scatters all the points in S
    xcoord = []
    ycoord = []
    for p in S:
        xcoord.append(p.x)
        ycoord.append(p.y)
    plt.scatter(xcoord, ycoord)
    plt.draw()
    plt.pause(wait)

# def connect(p1, p2):
#     line = plt.plot([p1.x, p2.x], [p1.y,p2.y])  #Return this line to be able to remove it in future if required
#     plt.draw()
#     plt.pause(1)
#     return line


def connectPoints(S):
    # Connects list of points in order
    # List should have at least two points
    lines = []
    for i in range(1, len(S)):
        # Return this line to be able to remove it in future if required
        line = plt.plot([S[i].x, S[i-1].x], [S[i].y, S[i-1].y])
        lines.append(line)
    plt.draw()
    plt.pause(wait)
    return lines

# def removeLine(line):
#     line.pop(0).remove()
#     plt.draw()
#     plt.pause(1)


def removeLines(lines):
    # Removes all the lines in the list lines
    # Each line in lines is a plt.plot return
    for line in lines:
        line.pop(0).remove()
    plt.draw()
    plt.pause(wait)


def markPoints(S):
    # Highlights all the points in S
    for p in S:
        plt.scatter(p.x, p.y, s=200)
    plt.draw()
    plt.pause(wait)


def quickhull(S: List[Point]) -> List[Point]:
    scttr(S)
    P = []
    a = leftmost(S)
    b = rightmost(S)
    markPoints([a, b])
    connectPoints([a, b])
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
        markPoints([farthest])
        connectPoints([a, farthest, b])
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


# Jarvis Algorithm
def jarvis(S: List[Point]) -> List[Point]:
    scttr(S)
    pointOnHull = leftmost(S)  # linear cost scan
    markPoints([pointOnHull])
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
        connectPoints([pointOnHull, endpoint])
        markPoints([endpoint])
        pointOnHull = endpoint

        # End Condition
        if endpoint == P[0]:
            loop = False

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
    S = sorted(S, key=lambda z: z.x)
    return divideConquer(S)

# Andrew's Algorithm, Animated


def draw_andrews_state(S, U, L, p: Point | None, ax, wait, L_complete, U_complete):
    """Draws the current state of andrews algorithm

    Args:
        S (List[Point]): The full point set
        U (List[Point]): The current upper hull list
        L (List[Point]): The current lower hull list
        p (Point | None): The current point to add
        ax (Axes): The axes on which to draw the plot
        wait (float): The time length to wait after drawing the images
        L_complete (bool): If the lower hull is complete
        U_complete (bool): If the upper hull is complete
    """

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)

    if L_complete:
        mark_points(L, ax, c="tab:green", wait=0)
        link_points(L, ax, c="g", wait=0)
    else:
        mark_points(L, ax, c="tab:orange", wait=0)
        link_points(L, ax, c="k", wait=0)
        if p is not None:
            if len(L) != 0:
                link_points([L[-1], p], ax, c="y", wait=0)

    if U_complete:
        mark_points(U, ax, c="tab:green", wait=0)
        link_points(U, ax, c="g", wait=0)
    else:
        mark_points(U, ax, c="tab:orange", wait=0)
        link_points(U, ax, c="k", wait=0)
        if p is not None:
            if len(U) != 0:
                link_points([U[-1], p], ax, c="y", wait=0)

    if p is not None:
        if L_complete:
            mark_point(S[-1], ax, c="tab:green", wait=0)
        mark_point(S[0], ax, c="tab:green", wait=0)
        mark_point(p, ax, c="tab:blue", wait=0)

    pause(wait)


def andrew_animated(S: List[Point]) -> List[Point]:
    if len(S) <= 1:
        # Cover the case where the input set has one or zero points
        return S.copy()

    S = sorted(S, key=lambda p: (p.x, p.y))
    U = []
    L = []

    (_, ax) = new_plot()
    draw_andrews_state(S, U, L, None, ax, 1, False, False)

    # Compute lower hull
    for p in S:
        draw_andrews_state(S, U, L, p, ax, 1, False, False)

        while len(L) >= 2 and turn(L[-2], L[-1], p) <= 0:
            L.pop()
            draw_andrews_state(S, U, L, p, ax, 1, False, False)

        L.append(p)

    draw_andrews_state(S, U, L, None, ax, 1, True, False)

    # Compute upper hull
    for p in reversed(S):
        draw_andrews_state(S, U, L, p, ax, 1, True, False)

        while len(U) >= 2 and turn(U[-2], U[-1], p) <= 0:
            U.pop()
            draw_andrews_state(S, U, L, p, ax, 1, True, False)

        U.append(p)

    draw_andrews_state(S, U, L, None, ax, 1.5, True, True)

    # remove duplicate points, last of each is the first of the other
    L.pop()
    U.pop()

    return L + U


if __name__ == '__main__':
    S = [Point(-1, 0), Point(0, 1), Point(-1/math.sqrt(2), -1/math.sqrt(2)),
         Point(0, -1), Point(1, 0), Point(0.2, -0.2), Point(-0.5, -0.2)]
    # S = [Point(-1,0), Point(0,1), Point(-1/math.sqrt(2),-1/math.sqrt(2)), Point(0,-1), Point(1,0), Point(0.2,-0.2), Point(-0.5,-0.2)]

    # scttr(S)
    # # line = connect(Point(-1,0), Point(0,1))
    # lines = connectPoints([Point(-1,0), Point(0,1), Point(-1/math.sqrt(2),-1/math.sqrt(2)), Point(0,-1), Point(1,0)])
    # removeLines(lines)
    # markPoints([Point(-1,0), Point(0,1)])

    # print(quickhull(S))
    # print(jarvis(S))
    # print(divideConquer0(S))
    print(andrew_animated(S))
