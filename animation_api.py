import matplotlib.pyplot as plt
import matplotlib.figure as fgr
import matplotlib.axes as axes
import matplotlib.lines
import matplotlib as mpl
from typing import List, Tuple
from primitives import *

WAIT = 1.5

colors = ["tab:purple", "tab:pink", "tab:cyan", "tab:brown", 'k']


def new_plot() -> Tuple[fgr.Figure, axes.Axes]:
    """Wrapper around plt.subplots

    Returns:
        Tuple[fgr.Figure, axes.Axes]: Tuple of the figure and the axes on which drawings will be made.
    """
    return plt.subplots()


def plot_points(S: List[Point], ax: axes.Axes, c=None, wait=WAIT):
    """Plots the given points at a small size

    Args:
        S (List[Point]): The points to plot
        ax (axes.Axes): The axes on which to plot
        c (_type_, optional): The color with which to draw the points. Defaults to None.
        wait (float, optional): Time to wait after drawing points. Defaults to WAIT.
    """
    xcoord = []
    ycoord = []
    for p in S:
        xcoord.append(p.x)
        ycoord.append(p.y)
    ax.scatter(xcoord, ycoord, color=c)
    pause(wait)


def mark_point(p: Point, ax: axes.Axes, s=200, c=None, wait=WAIT):
    """Draws a specific point at specified size and in specified color

    Args:
        p (Point): The point to draw
        ax (axes.Axes): The axes on which to draw the point
        s (int, optional): The size of the point. Defaults to 200.
        c (_type_, optional): The color to draw the point. Defaults to None.
        wait (float, optional): Time to wait after drawing the point. Defaults to WAIT.
    """
    ax.scatter(p.x, p.y, s=s, color=c)
    pause(wait)


def mark_points(S: List[Point], ax: axes.Axes, s=200, c=None, wait=WAIT):
    """Calls mark_points on all points in S, with no delay between

    Args:
        S (List[Point]): Points to draw
        ax (axes.Axes): Axes on which to draw points
        s (int, optional): Size with which to draw points. Defaults to 200.
        c (_type_, optional): Color with which to draw points. Defaults to None.
        wait (float, optional): Time to wait after drawing all points is complete. Defaults to WAIT.
    """
    for p in S:
        mark_point(p, ax, s=s, c=c, wait=0)
    pause(wait)


def link_points(S: List[Point], ax: axes.Axes, c=None, wait=WAIT) -> List[matplotlib.lines.Line2D]:
    """Draws lines between adjacent points in S

    Args:
        S (List[Point]): Points to link with lines
        ax (axes.Axes): Axes on which to draw the points
        c (_type_, optional): Color to draw lines in. Defaults to None.
        wait (float, optional): Time to wait after drawing all lines. Defaults to WAIT.

    Returns:
        List[matplotlib.lines.Line2D]: List of all lines created
    """

    lines = []
    for i in range(1, len(S)):
        lines.append(ax.plot([S[i].x, S[i-1].x], [S[i].y, S[i-1].y], c=c))
    pause(wait)
    return lines


def draw_line(p1: Point, p2: Point, ax: axes.Axes, c=None, wait=WAIT):
    """Draws infinite line between points p1 and p2. If p1 and p2 are identical, draws no line
       but still waits.

    Args:
        p1 (Point): Point 1 on line
        p2 (Point): Point 2 on line
        ax (axes.Axes): Axes to draw line on
        c (_type_, optional): Color of line to draw. Defaults to None.
        wait (float, optional): Time to wait after drawing lines. Defaults to WAIT.
    """
    if p1 != p2:
        ax.axline((p1.x, p1.y), (p2.x, p2.y), color=c)
    pause(wait)


def clear(ax: axes.Axes):
    """Wrapper around Axes.clear()

    Args:
        ax (axes.Axes): Axes to clear drawings from
    """
    ax.clear()


def pause(wait: float):
    """Wrapper around plt.pause() with different handling of 0 wait. Waits of 0 lead to no delay

    Args:
        wait (float): Time to pause drawing for
    """
    if wait != 0:
        plt.pause(wait)
