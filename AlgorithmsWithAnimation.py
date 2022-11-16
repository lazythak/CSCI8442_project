from typing import List, Tuple, Union
from primitives import *
import matplotlib.pyplot as plt
from animation_api import *
import algorithms as alg
from DatasetCreationAndTimeAnalysis import *

wait = 1.5


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


def quickhull_animated(S: List[Point], wait: float = wait) -> List[Point]:
    (fig, ax) = new_plot()

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=wait)

    P = []
    a = alg.leftmost(S)
    b = alg.rightmost(S)

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)
    mark_point(a, ax, c="tab:green", wait=0)
    mark_point(b, ax, c="tab:green", wait=0)
    link_points([a, b], ax, c="y", wait=wait)

    S1 = []
    S2 = []
    for p in S:
        if sidedness_i(DLine(a, b), p) == -1:
            S1.append(p)
        elif sidedness_i(DLine(b, a), p) == -1:
            S2.append(p)

    P.append(a)
    DD = findquickhull_animated(S1, a, b, S, [a], [b], ax, wait)
    if len(DD) > 0:
        P = P+DD
    P.append(b)
    DD = findquickhull_animated(S2, b, a, S, P, [], ax, wait)
    if len(DD) > 0:
        P = P+DD

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)
    mark_points(P, ax, c="tab:green", wait=0)
    link_points(P, ax, c="g", wait=0)
    link_points([P[0], P[-1]], ax, c="g", wait=wait)

    plt.close(fig)

    return P


def findquickhull_animated(S: List[Point], a: Point, b: Point, extra: List[Point], k1: List[Point], k2: List[Point], ax, wait: float = wait) -> List[Point]:
    P = []
    if len(S) == 0:
        return []
    else:

        known = k1 + k2

        clear(ax)
        plot_points(extra, ax, c="xkcd:light grey", wait=0)
        plot_points(S, ax, c="tab:grey", wait=0)
        mark_points(known, ax, c="tab:green", wait=0)
        draw_line(a, b, ax, c="m", wait=0)
        link_points(known, ax, c="y", wait=0)
        link_points([known[-1], known[0]], ax, c="y", wait=0)
        mark_points([a, b], ax, c="tab:green", wait=wait)

        farthest = S[0]
        for p in S:
            clear(ax)
            plot_points(extra, ax, c="xkcd:light grey", wait=0)
            plot_points(S, ax, c="tab:grey", wait=0)
            mark_points(known, ax, c="tab:green", wait=0)
            draw_line(a, b, ax, c="m", wait=0)
            link_points(known, ax, c="y", wait=0)
            link_points([known[-1], known[0]], ax, c="y", wait=0)
            mark_points([a, b], ax, c="tab:green", wait=0)
            mark_point(farthest, ax, c="tab:orange", wait=0)
            mark_point(p, ax, c="tab:blue", wait=wait)

            if area(p, a, b) >= area(farthest, a, b):
                mark_point(p, ax, c="tab:olive", wait=wait)
                farthest = p
            else:
                mark_point(p, ax, c="tab:red", wait=wait)

        clear(ax)
        plot_points(extra, ax, c="xkcd:light grey", wait=0)
        plot_points(S, ax, c="tab:grey", wait=0)
        mark_points(known, ax, c="tab:green", wait=0)
        link_points(known, ax, c="y", wait=0)
        link_points([known[-1], known[0]], ax, c="y", wait=0)
        mark_points([a, b], ax, c="tab:green", wait=0)
        mark_point(farthest, ax, c="tab:green", wait=0)
        link_points([a, farthest, b], ax, c="y", wait=wait)

        S1 = []
        S2 = []
        for p in S:
            if sidedness_i(DLine(a, farthest), p) == -1:
                S1.append(p)
            elif sidedness_i(DLine(farthest, b), p) == -1:
                S2.append(p)

        DD = findquickhull_animated(S1, a, farthest, extra, k1, [
                                    farthest] + k2, ax, wait)

        if len(DD) > 0:
            P = P+DD
        P.append(farthest)

        DD = findquickhull_animated(
            S2, farthest, b, extra, k1 + P + [farthest], k2, ax, wait)
        if len(DD) > 0:
            P = P+DD
        return P


# Jarvis Algorithm
def jarvis_animated(S: List[Point], wait: float = wait) -> List[Point]:
    (fig, ax) = new_plot()

    plot_points(S, ax, c="tab:grey", wait=wait)

    pointOnHull = alg.leftmost(S)  # linear cost scan

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=wait)

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
            mark_point(endpoint, ax, c="tab:orange", wait=wait)

            if (endpoint == pointOnHull) or (sidedness(DLine(P[i], endpoint), p) < 0):
                mark_point(p, ax, c="tab:olive", wait=wait)
                endpoint = p
            else:
                mark_point(p, ax, c="tab:red", wait=wait)

        i = i+1
        pointOnHull = endpoint

        # End Condition
        if endpoint == P[0]:
            loop = False

    P.append(P[0])
    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)
    mark_points(P, ax, c="tab:green", wait=0)
    link_points(P, ax, c="g", wait=wait)

    plt.close(fig)

    return P[0:-1]


# Divide and Conquer

def combine_animated(S1: List[Point], S2: List[Point], ax, wait: float = wait, extra=[]):
    # Upper half
    _, i1 = rightmostWithInd(S1)
    _, i2 = leftmostWithInd(S2)

    linex = (S1[i1].x + S2[i2].x)/2
    line = [Point(linex, 0), Point(linex, 1)]

    clear(ax)
    plot_points(extra, ax, c="tab:grey", wait=0)
    draw_line(line[0], line[1], ax, c='k', wait=0)
    mark_points(S1, ax, c="xkcd:blue", wait=0)
    link_points(S1, ax, c="xkcd:blue", wait=0)
    link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
    mark_points(S2, ax, c="xkcd:purple", wait=0)
    link_points(S2, ax, c="xkcd:purple", wait=0)
    link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=wait)
    link_points([S1[i1], S2[i2]], ax, c="y", wait=wait)

    go_on = True
    while go_on:
        go_on = False
        while True:
            if sidedness_i(DLine(S1[i1], S2[i2]), S2[(i2-1) % len(S2)]) == 1:
                go_on = True
                i2 = (i2-1) % len(S2)

                clear(ax)
                plot_points(extra, ax, c="tab:grey", wait=0)
                draw_line(line[0], line[1], ax, c='k', wait=0)
                mark_points(S1, ax, c="xkcd:blue", wait=0)
                link_points(S1, ax, c="xkcd:blue", wait=0)
                link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
                mark_points(S2, ax, c="xkcd:purple", wait=0)
                link_points(S2, ax, c="xkcd:purple", wait=0)
                link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=0)
                link_points([S1[i1], S2[i2]], ax, c="y", wait=wait)
            else:
                break

        while True:
            if sidedness_i(DLine(S2[i2], S1[i1]), S1[(i1+1) % len(S1)]) == -1:
                go_on = True
                i1 = (i1+1) % len(S1)

                clear(ax)
                plot_points(extra, ax, c="tab:grey", wait=0)
                draw_line(line[0], line[1], ax, c='k', wait=0)
                mark_points(S1, ax, c="xkcd:blue", wait=0)
                link_points(S1, ax, c="xkcd:blue", wait=0)
                link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
                mark_points(S2, ax, c="xkcd:purple", wait=0)
                link_points(S2, ax, c="xkcd:purple", wait=0)
                link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=0)
                link_points([S1[i1], S2[i2]], ax, c="y", wait=wait)
            else:
                break

    left_up = i1
    right_up = i2

    # Lower half
    _, i1 = rightmostWithInd(S1)
    _, i2 = leftmostWithInd(S2)

    clear(ax)
    plot_points(extra, ax, c="tab:grey", wait=0)
    draw_line(line[0], line[1], ax, c='k', wait=0)
    mark_points(S1, ax, c="xkcd:blue", wait=0)
    link_points(S1, ax, c="xkcd:blue", wait=0)
    link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
    mark_points(S2, ax, c="xkcd:purple", wait=0)
    link_points(S2, ax, c="xkcd:purple", wait=0)
    link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=0)
    link_points([S1[left_up], S2[right_up]], ax,
                c="xkcd:blue green", wait=wait)
    link_points([S1[i1], S2[i2]], ax, c="y", wait=wait)

    go_on = True
    while go_on:
        go_on = False
        while True:
            if sidedness_i(DLine(S1[i1], S2[i2]), S2[(i2 + 1) % len(S2)]) == -1:
                go_on = True
                i2 = (i2 + 1) % len(S2)

                clear(ax)
                plot_points(extra, ax, c="tab:grey", wait=0)
                draw_line(line[0], line[1], ax, c='k', wait=0)
                mark_points(S1, ax, c="xkcd:blue", wait=0)
                link_points(S1, ax, c="xkcd:blue", wait=0)
                link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
                mark_points(S2, ax, c="xkcd:purple", wait=0)
                link_points(S2, ax, c="xkcd:purple", wait=0)
                link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=0)
                link_points([S1[left_up], S2[right_up]],
                            ax, c="xkcd:blue green", wait=0)
                link_points([S1[i1], S2[i2]], ax, c="y", wait=wait)
            else:
                break

        while True:
            if sidedness_i(DLine(S2[i2], S1[i1]), S1[(i1 - 1) % len(S1)]) == 1:
                go_on = True
                i1 = (i1 - 1) % len(S1)

                clear(ax)
                plot_points(extra, ax, c="tab:grey", wait=0)
                draw_line(line[0], line[1], ax, c='k', wait=0)
                mark_points(S1, ax, c="xkcd:blue", wait=0)
                link_points(S1, ax, c="xkcd:blue", wait=0)
                link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
                mark_points(S2, ax, c="xkcd:purple", wait=0)
                link_points(S2, ax, c="xkcd:purple", wait=0)
                link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=0)
                link_points([S1[left_up], S2[right_up]],
                            ax, c="xkcd:blue green", wait=0)
                link_points([S1[i1], S2[i2]], ax, c="y", wait=wait)
            else:
                break
    left_down = i1
    right_down = i2

    clear(ax)
    plot_points(extra, ax, c="tab:grey", wait=0)
    draw_line(line[0], line[1], ax, c='k', wait=0)
    mark_points(S1, ax, c="xkcd:blue", wait=0)
    link_points(S1, ax, c="xkcd:blue", wait=0)
    link_points([S1[0], S1[-1]], ax, c="xkcd:blue", wait=0)
    mark_points(S2, ax, c="xkcd:purple", wait=0)
    link_points(S2, ax, c="xkcd:purple", wait=0)
    link_points([S2[0], S2[-1]], ax, c="xkcd:purple", wait=0)
    link_points([S1[left_up], S2[right_up]], ax, c="xkcd:blue green", wait=0)
    link_points([S1[left_down], S2[right_down]],
                ax, c="xkcd:blue green", wait=wait)

    P = []
    if left_up > left_down:
        left_down = left_down+len(S1)
    for j in range(left_up, left_down+1):
        P.append(S1[(j % len(S1))])

    if right_down > right_up:
        right_up = right_up+len(S2)
    for j in range(right_down, right_up+1):
        P.append(S2[(j % len(S2))])

    clear(ax)
    plot_points(extra, ax, c="tab:grey", wait=0)
    draw_line(line[0], line[1], ax, c='k', wait=0)
    mark_points(P, ax, c="xkcd:blue green", wait=0)
    link_points(P, ax, c="xkcd:blue green", wait=0)
    link_points([P[0], P[-1]], ax, c="xkcd:blue green", wait=wait)

    return (P)


def divideConquer_animated(S: List[Point], wait: float = wait, extra: List[Point] = [], ax: Union[axes.Axes, None] = None) -> List[Point]:
    if len(S) <= 1:
        return S
    else:
        if ax is None:
            (fig, ax) = new_plot()
        else:
            fig = None

        clear(ax)
        plot_points(extra, ax, c="xkcd:light grey", wait=0)
        plot_points(S, ax, c="tab:grey", wait=0)
        x = (S[len(S)//2].x + S[(len(S)//2)-1].x)/2
        draw_line(Point(x, 0),
                  Point(x, 1), ax, c="k", wait=wait)

        out = combine_animated(divideConquer_animated(S[0:len(S)//2], wait, extra, ax),
                               divideConquer_animated(S[len(S)//2:len(S)], wait, extra, ax), ax, wait, extra)
        if fig is not None:
            clear(ax)
            plot_points(S, ax, c="tab:grey", wait=0)
            draw_line(Point(x, 0), Point(x, 1), ax, c="k", wait=0)
            mark_points(out, ax, c="tab:green", wait=0)
            link_points(out, ax, c="g", wait=0)
            link_points([out[0], out[-1]], ax, c="g", wait=wait)
            plt.close(fig)
        return out


def divideConquer_unsorted_animated(S: List[Point], wait=wait) -> List[Point]:
    S = sorted(S, key=lambda z: (z.x, z.y))
    return divideConquer_animated(S, wait, extra=S)

# Andrew's Algorithm, Animated


def draw_andrews_state(S, U, L, p, ax, wait: float, L_complete, U_complete, c1, c2, c3, c4=None, Extra=[]):
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


def andrew_core_animated(S: List[Point], c1, c2, c3, ax, wait: float, c4=None, Extra=[]) -> List[Point]:
    if len(S) <= 1:
        # Cover the case where the input set has one or zero points
        return S.copy()

    S = sorted(S, key=lambda p: (p.x, p.y))
    U = []
    L = []

    draw_andrews_state(S, U, L, None, ax, wait, False,
                       False, c1, c2, c3, c4, Extra)

    # Compute lower hull
    for p in S:
        draw_andrews_state(S, U, L, p, ax, wait, False,
                           False, c1, c2, c3, c4, Extra)

        while len(L) >= 2 and turn(L[-2], L[-1], p) <= 0:
            L.pop()
            draw_andrews_state(S, U, L, p, ax, wait, False,
                               False, c1, c2, c3, c4, Extra)

        L.append(p)

    draw_andrews_state(S, U, L, None, ax, wait, True,
                       False, c1, c2, c3, c4, Extra)

    # Compute upper hull
    for p in reversed(S):
        draw_andrews_state(S, U, L, p, ax, wait, True,
                           False, c1, c2, c3, c4, Extra)

        while len(U) >= 2 and turn(U[-2], U[-1], p) <= 0:
            U.pop()
            draw_andrews_state(S, U, L, p, ax, wait, True,
                               False, c1, c2, c3, c4, Extra)

        U.append(p)

    draw_andrews_state(S, U, L, None, ax, wait, True,
                       True, c1, c2, c3, c4, Extra)

    # remove duplicate points, last of each is the first of the other
    L.pop()
    U.pop()

    return L + U


def andrew_animated(S: List[Point], wait: float = wait) -> List[Point]:
    (fig, ax) = new_plot()
    data = andrew_core_animated(S, "tab:grey", "tab:green", "g", ax, wait)
    plt.close(fig)
    return data


# Chan's Algorithm with Animation


def rtangent_animated(v: List[Point], p: Point, ci: int, Extra: List[Point], ax, wait: float = wait) -> int:
    """computes the right, or upper, tangent from p to v.
    Preconditions: v has size > 1, p on exterior of v

    Algorithm found here, and modified to fit needs:
    https://web.archive.org/web/20190714200906/http://geomalgorithms.com/a15-_tangents.html#tangent_PointPolyC()

    Args:
        v (List[Point]): convex polygon to find upper tangent on
        p (Point): point to find upper tangent from
        ci (int): index into colors list to use
        Extra (List[Point]): Extra points to plot
        ax (_type_): axes to plot points on

    Returns:
        int: index of point that the tangent hits in v
    """

    clr = colors[ci % len(colors)]

    clear(ax)
    plot_points(Extra, ax, c="xkcd:light grey", wait=0)
    mark_points(v, ax, c=clr, wait=0)
    link_points(v, ax, c=clr, wait=0)
    link_points([v[0], v[-1]], ax, c=clr, wait=0)
    mark_point(p, ax, c="tab:green", wait=wait)

    n = len(v)
    if n == 1:
        # case to handle when v is of size 1
        print("Size 1 hull, short-circuit")
        return 0

    # right tangent is local maximum for ordering where points to left of line are lower than those on
    if (alg.below(p, v[1], v[0]) and not alg.above(p, v[n-1], v[0])):
        clear(ax)
        plot_points(Extra, ax, c="xkcd:light grey", wait=0)
        mark_points(v, ax, c=clr, wait=0)
        link_points(v, ax, c=clr, wait=0)
        link_points([v[0], v[-1]], ax, c=clr, wait=0)
        mark_point(p, ax, c="tab:green", wait=0)
        mark_point(v[0], ax, c="tab:orange", wait=wait)

        return 0

    a = 0
    b = n       # initial chain = [0, n], let v[n] = v[0]
    olda = a
    oldb = b

    while True:
        c: int = (a + b) // 2                       # c is midpoint

        clear(ax)
        plot_points(Extra, ax, c="xkcd:light grey", wait=0)
        plot_points(v, ax, c="tab:grey", wait=0)
        mark_points(v[a:b], ax, c=clr, wait=0)
        link_points(v[a:b], ax, c=clr, wait=0)
        mark_point(p, ax, c="tab:green", wait=0)
        mark_point(v[c], ax, c="tab:blue", wait=0)
        draw_line(v[c], p, ax, c="y", wait=wait)

        dnC = alg.below(p, v[(c+1) % n], v[c])
        if (dnC and not alg.above(p, v[c-1], v[c])):
            clear(ax)
            plot_points(Extra, ax, c="xkcd:light grey", wait=0)
            plot_points(v, ax, c="tab:grey", wait=0)
            mark_points(v[a:b], ax, c=clr, wait=0)
            link_points(v[a:b], ax, c=clr, wait=0)
            mark_point(p, ax, c="tab:green", wait=0)
            mark_point(v[c], ax, c="tab:orange", wait=wait)
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


def chan_step_animated(S: List[Point], m: int, H: int, ax, wait: float = wait) -> List[Point]:
    partitions: List[List[Point]] = alg.partition_list(S, m)
    subhulls: List[List[Point]] = []

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=wait)

    for i in range(0, len(partitions)):
        subhulls.append(andrew_core_animated(partitions[i], "tab:grey", colors[i % len(
            colors)], colors[i % len(colors)], ax, wait, "xkcd:light grey", S))

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
        mark_points(alg.to_points(P, subhulls), ax, c="tab:green", wait=0)
        link_points(alg.to_points(P, subhulls), ax, c="g", wait=0)
        mark_points(alg.to_points(P[-1:], subhulls),
                    ax, c="tab:blue", wait=wait)

        q: List[Tuple[int, int]] = []  # point
        (ch, cp) = P[-1]  # hull and point indices of most recent point on hull
        for i in range(0, len(subhulls)):
            if ch == i:
                # Special case, most recent point is on this hull, get next element on this subhull
                if len(subhulls[i]) != 1:
                    # If the size is one, then that's the point we're currently at. Don't want to
                    # get the current point, so just skip this subhull in this case
                    q.append((i, (cp + 1) % len(subhulls[i])))

                    clear(ax)
                    plot_points(S, ax, c="xkcd:light grey", wait=0)
                    mark_points(subhulls[i], ax,
                                c=colors[i % len(colors)], wait=0)
                    link_points(subhulls[i], ax,
                                c=colors[i % len(colors)], wait=0)
                    link_points([subhulls[i][0], subhulls[i][-1]],
                                ax, c=colors[i % len(colors)], wait=0)
                    mark_point(subhulls[ch][cp], ax, c="tab:green", wait=wait)
                    mark_points(alg.to_points([q[-1]], subhulls),
                                ax, c="tab:orange", wait=wait)
            else:
                q.append((i, rtangent_animated(
                    subhulls[i], subhulls[ch][cp], i, S, ax, wait)))

        clear(ax)
        plot_points(S, ax, c="tab:grey", wait=0)
        for (i, subhull) in enumerate(subhulls):
            mark_points(subhull, ax, c=colors[i %
                        len(colors)], s=100, wait=0)
            link_points(subhull, ax, c=colors[i % len(colors)], wait=0)
            link_points([subhull[0], subhull[-1]], ax,
                        c=colors[i % len(colors)], wait=0)
        mark_points(alg.to_points(P, subhulls), ax, c="tab:green", wait=0)
        link_points(alg.to_points(P, subhulls), ax, c="g", wait=0)
        mark_points(alg.to_points(P[-1:], subhulls), ax, c="tab:blue", wait=0)
        mark_points(alg.to_points(q, subhulls), ax, c="tab:orange", wait=wait)

        clear(ax)
        plot_points(S, ax, c="xkcd:light grey", wait=0)
        plot_points(alg.to_points(q, subhulls), ax, c="tab:grey", wait=0)
        mark_points(alg.to_points(P, subhulls), ax, c="tab:green", wait=0)
        link_points(alg.to_points(P, subhulls), ax, c="g", wait=wait)

        # append point with max angle from q, use step of jarvis march
        (eh, ep) = q[0]
        for (ph, pp) in q:
            (ch, cp) = P[-1]

            clear(ax)
            plot_points(S, ax, c="xkcd:light grey", wait=0)
            plot_points(alg.to_points(q, subhulls), ax, c="tab:grey", wait=0)
            mark_points(alg.to_points(P, subhulls), ax, c="tab:green", wait=0)
            link_points(alg.to_points(P, subhulls), ax, c="g", wait=0)
            mark_point(subhulls[ph][pp], ax, c="tab:blue", wait=0)
            draw_line(subhulls[ch][cp], subhulls[eh][ep], ax, c="m", wait=0)
            link_points([subhulls[ch][cp], subhulls[eh][ep]],
                        ax, c="y", wait=0)
            mark_point(subhulls[eh][ep], ax, c="tab:orange", wait=wait)

            if (subhulls[eh][ep] == subhulls[ch][cp]) or (sidedness(DLine(subhulls[ch][cp], subhulls[eh][ep]), subhulls[ph][pp]) < 0):
                mark_point(subhulls[ph][pp], ax, c="tab:olive", wait=wait)
                eh = ph
                ep = pp
            else:
                mark_point(subhulls[ph][pp], ax, c="tab:red", wait=wait)
        P.append((eh, ep))

        if P[-1] == P[0]:
            return alg.to_points(P, subhulls)

    clear(ax)
    plot_points(S, ax, c="tab:grey", wait=0)
    mark_points(alg.to_points(P, subhulls), ax, c="tab:red", wait=0)
    link_points(alg.to_points(P, subhulls), ax, c="r", wait=wait)

    return []  # "incomplete"


def chan_animated(S: List[Point], wait: float = wait) -> List[Point]:
    (fig, ax) = new_plot()

    for t in range(1, len(S)):
        print(f"~~~~Step: {t}~~~~~~~~~")
        m = min(len(S), pow(2, pow(2, t)))
        L = chan_step_animated(S, m, m, ax, wait)

        clear(ax)
        plot_points(S, ax, c="tab:grey", wait=0)

        if L != []:
            mark_points(L, ax, c="tab:green", wait=0)
            link_points(L, ax, c="g", wait=wait)
            plt.close(fig)
            return L[0:-1]
        pause(wait)

    plt.close(fig)

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
    data = CreateCircleDataset(15, 8)
    print(jarvis_animated(S, 0.2))
