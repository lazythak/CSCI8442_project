from typing import List, Tuple
from primitives import *
import matplotlib.pyplot as plt
from animation_api import *
import algorithms as alg
from DatasetCreationAndTimeAnalysis import *

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
    (fig, ax) = new_plot()

    plot_points(S, ax, c="tab:grey", wait=1)

    pointOnHull = leftmost(S)  # linear cost scan

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=1)

    i = 0
    loop = True
    P = []

    while loop:  # Runs once for each point on the hull
        P.append(pointOnHull)
        endpoint = S[0]

        for p in S:  # Scans over every point
            clear(ax)
            plot_points(S, ax, c="tab:grey", wait=0)
            mark_points(P, ax, c="tab:green", wait=0)
            link_points(P, ax, c="g", wait=0)
            mark_point(p, ax, c="tab:blue", wait=0)
            draw_line(P[-1], endpoint, ax, c="m", wait=0)
            link_points([P[-1], endpoint], ax, c="y", wait=0)
            mark_point(endpoint, ax, c="tab:orange", wait=1)

            if (endpoint == pointOnHull) or (sidedness(DLine(P[i], endpoint), p) > 0):
                mark_point(p, ax, c="tab:olive", wait=1)
                endpoint = p
            else:
                mark_point(p, ax, c="tab:red", wait=1)

        i = i+1
        pointOnHull = endpoint

        # End Condition
        if endpoint == P[0]:
            loop = False

    P.append(P[0])
    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)
    mark_points(P, ax, c="tab:green", wait=0)
    link_points(P, ax, c="g", wait=1)

    plt.close(fig)

    return P[0:-1]


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


def draw_andrews_state(S, U, L, p, ax, wait, L_complete, U_complete, c1, c2, c3, c4=None, Extra=[]):
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
    plot_points(Extra, ax, c=c4, wait=0)
    plot_points(S, ax, c=c1, wait=0)

    if L_complete:
        mark_points(L, ax, c=c2, wait=0)
        link_points(L, ax, c=c3, wait=0)
    else:
        mark_points(L, ax, c="tab:orange", wait=0)
        link_points(L, ax, c="k", wait=0)
        if p is not None:
            if len(L) != 0:
                link_points([L[-1], p], ax, c="y", wait=0)

    if U_complete:
        mark_points(U, ax, c=c2, wait=0)
        link_points(U, ax, c=c3, wait=0)
    else:
        mark_points(U, ax, c="tab:orange", wait=0)
        link_points(U, ax, c="k", wait=0)
        if p is not None:
            if len(U) != 0:
                link_points([U[-1], p], ax, c="y", wait=0)

    if p is not None:
        if L_complete:
            mark_point(S[-1], ax, c=c2, wait=0)
        mark_point(S[0], ax, c=c2, wait=0)
        mark_point(p, ax, c="tab:blue", wait=0)

    pause(wait)


def andrew_core(S: List[Point], c1, c2, c3, ax, c4=None, Extra=[]) -> List[Point]:
    if len(S) <= 1:
        # Cover the case where the input set has one or zero points
        return S.copy()

    S = sorted(S, key=lambda p: (p.x, p.y))
    U = []
    L = []

    draw_andrews_state(S, U, L, None, ax, 1, False,
                       False, c1, c2, c3, c4, Extra)

    # Compute lower hull
    for p in S:
        draw_andrews_state(S, U, L, p, ax, 1, False,
                           False, c1, c2, c3, c4, Extra)

        while len(L) >= 2 and turn(L[-2], L[-1], p) <= 0:
            L.pop()
            draw_andrews_state(S, U, L, p, ax, 1, False,
                               False, c1, c2, c3, c4, Extra)

        L.append(p)

    draw_andrews_state(S, U, L, None, ax, 1, True,
                       False, c1, c2, c3, c4, Extra)

    # Compute upper hull
    for p in reversed(S):
        draw_andrews_state(S, U, L, p, ax, 1, True,
                           False, c1, c2, c3, c4, Extra)

        while len(U) >= 2 and turn(U[-2], U[-1], p) <= 0:
            U.pop()
            draw_andrews_state(S, U, L, p, ax, 1, True,
                               False, c1, c2, c3, c4, Extra)

        U.append(p)

    draw_andrews_state(S, U, L, None, ax, 1.5, True,
                       True, c1, c2, c3, c4, Extra)

    # remove duplicate points, last of each is the first of the other
    L.pop()
    U.pop()

    return L + U


def andrew_animated(S: List[Point]) -> List[Point]:
    (fig, ax) = new_plot()
    data = andrew_core(S, "tab:grey", "tab:green", "g", ax)
    plt.close(fig)
    return data


# Chan's Algorithm with Animation


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

    # right tangent is local maximum for ordering where points to left of line are lower than those on
    if (alg.below(p, v[1], v[0]) and not alg.above(p, v[n-1], v[0])):
        return 0

    a = 0
    b = n       # initial chain = [0, n], let v[n] = v[0]
    olda = a
    oldb = b
    while True:
        c: int = (a + b) // 2                       # c is midpoint
        print(v[a:b])
        dnC = alg.below(p, v[(c+1) % n], v[c])
        if (dnC and not alg.above(p, v[c-1], v[c])):
            return c  # v[c] is tangent

        # no max found, continue search
        # select either [a, c] or [c, b]
        upA = alg.above(p, v[(a+1) % n], v[a])
        if (upA):
            if (dnC):
                oldb = b
                olda = a
                b = c
            else:
                if (alg.above(p, v[a], v[c])):
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
                if alg.below(p, v[a], v[c]):
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


def to_points(P: List[Tuple[int, int]], SH: List[List[Point]]) -> List[Point]:
    out = []
    for (h, p) in P:
        out.append(SH[h][p])
    return out


def chan_step(S: List[Point], m: int, H: int, ax) -> List[Point]:
    partitions: List[List[Point]] = alg.partition_list(S, m)
    subhulls: List[List[Point]] = []

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=1)

    for i in range(0, len(partitions)):
        subhulls.append(andrew_core(partitions[i], "tab:grey", colors[i % len(
            colors)], colors[i % len(colors)], ax, "xkcd:light grey", S))

    # P[0] is the rightmost point, which we know must be on the hull
    P = [alg.subhull_rightmost(subhulls)]

    for k in range(0, H):
        clear(ax)
        plot_points(S, ax, c="tab:grey", wait=0)
        for (i, subhull) in enumerate(subhulls):
            mark_points(subhull, ax, c=colors[i %
                        len(colors)], s=100, wait=0)
            link_points(subhull, ax, c=colors[i % len(colors)], wait=0)
            link_points([subhull[0], subhull[-1]], ax,
                        c=colors[i % len(colors)], wait=0)
        mark_points(to_points(P, subhulls), ax, c="tab:green", wait=0)
        link_points(to_points(P, subhulls), ax, c="g", wait=0)
        mark_points(to_points(P[-1:], subhulls), ax, c="tab:blue", wait=1)

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

        mark_points(to_points(q, subhulls), ax, c="tab:orange", wait=1)

        # append point with max angle from q, use step of jarvis march
        (eh, ep) = q[0]
        for (ph, pp) in q:
            (ch, cp) = P[-1]
            if (subhulls[eh][ep] == subhulls[ch][cp]) or (sidedness(DLine(subhulls[ch][cp], subhulls[eh][ep]), subhulls[ph][pp]) < 0):
                eh = ph
                ep = pp
        P.append((eh, ep))

        if P[-1] == P[0]:
            return to_points(P, subhulls)

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)
    mark_points(to_points(P, subhulls), ax, c="tab:red", wait=0)
    link_points(to_points(P, subhulls), ax, c="r", wait=1)

    return []  # "incomplete"


def chan(S: List[Point]) -> List[Point]:
    (fig, ax) = new_plot()

    for t in range(1, len(S)):
        print(f"~~~~Step: {t}~~~~~~~~~")
        m = min(len(S), pow(2, pow(2, t)))
        L = chan_step(S, m, m, ax)

        clear(ax)
        plot_points(S, ax, c="tab:grey", wait=0)

        if L != []:
            mark_points(L, ax, c="tab:green", wait=0)
            link_points(L, ax, c="g", wait=1)
            return L[0:-1]
        pause(1)

    return []  # Error case, should never be reached


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
    # print(andrew_animated(S))
    data = CreateCircleDataset(50, 8)
    print(chan(S))
