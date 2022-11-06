import matplotlib.pyplot as plt
import matplotlib.figure as fgr
import matplotlib.axes as axes
import matplotlib.lines
import matplotlib as mpl
from typing import List, Tuple
from primitives import *

WAIT = 1.5


def new_plot() -> Tuple[fgr.Figure, axes.Axes]:
    return plt.subplots()


def plot_points(S: List[Point], ax: axes.Axes, c=None, wait=WAIT):
    xcoord = []
    ycoord = []
    for p in S:
        xcoord.append(p.x)
        ycoord.append(p.y)
    ax.scatter(xcoord, ycoord, color=c)
    pause(wait)


def mark_point(p: Point, ax: axes.Axes, s=200, c=None, wait=WAIT):
    ax.scatter(p.x, p.y, s=s, color=c)
    pause(wait)


def mark_points(S: List[Point], ax: axes.Axes, s=200, c=None, wait=WAIT):
    for p in S:
        mark_point(p, ax, s=s, c=c, wait=0)
    pause(wait)


def link_points(S: List[Point], ax: axes.Axes, c=None, wait=WAIT) -> \
        List[matplotlib.lines.Line2D]:

    lines = []
    for i in range(1, len(S)):
        lines.append(ax.plot([S[i].x, S[i-1].x], [S[i].y, S[i-1].y], c=c))
    pause(wait)
    return lines


def clear(ax: axes.Axes):
    ax.clear()


def pause(wait):
    if wait != 0:
        plt.pause(wait)
