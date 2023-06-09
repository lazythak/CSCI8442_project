import math


class Point:
    """Defines a point in 2d space

    Returns:
        Point: Point in 2d space
    """
    x: float = 0
    y: float = 0

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    @staticmethod
    def origin() -> 'Point':
        """returns the origin

        Returns:
            Point: The origin point, (0,0)
        """
        return Point(0, 0)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"({self.x},{self.y})"


class LineSeg:
    """A line segment or vector

    Returns:
        LineSeg: A line segment or vector, with p1 at root and p2 at tip
    """
    p1: Point = Point(0, 0)
    p2: Point = Point(0, 0)

    def __init__(self, p1: Point, p2: Point):
        """Creates a new LineSeg from two points

        Args:
            p1 (Point): The first point, used as the root when treated as a vector
            p2 (Point): The second point, used as the tip when treated as a vector
        """
        self.p1 = p1
        self.p2 = p2

    def cross(self, other: 'LineSeg') -> float:
        """Computes the cross product of the inputs, computed relocating them to be rooted at the origin

        Args:
            other (LineSeg): The second vector in the cross product

        Returns:
            float: The cross product of the inputs
        """
        P: Point = self.p2 - self.p1
        Q: Point = other.p2 - other.p1

        return (P.x * Q.y - P.y * Q.x)


class DLine:
    """Directed Line
    """
    p1: Point
    p2: Point

    def __init__(self, p1: Point, p2: Point):
        """Creates a new directed line through the provided points

        Args:
            p1 (Point): The first point the line passes through
            p2 (Point): The second point the line passes through
        """
        self.p1 = p1
        self.p2 = p2


def turn(p: Point, q: Point, r: Point) -> float:
    """Computes if the points p, q, and r, in order turn left, continue straight, or turn right, at q

    Args:
        p (Point): The first point
        q (Point): The turn point
        r (Point): The final point

    Returns:
        float: The turn value.
               Positive for left
               Zero for straight
               Negative for right
    """
    return LineSeg(p, q).cross(LineSeg(q, r))


def turn_i(p: Point, q: Point, r: Point) -> int:
    """Computes if the points p, q, and r, in order turn left, continue straight, or turn right, at q

    Args:
        p (Point): The first point
        q (Point): The turn point
        r (Point): The final point

    Returns:
        int: The turn value.
               -1 for left
               0 for straight
               +1 for right
    """
    v = turn(p, q, r)
    if v < 0:
        return -1
    elif v > 0:
        return 1
    else:
        return 0


def sidedness(line: DLine, r: Point) -> float:
    """Computes if r is the left, right, or on the directed line line

    Args:
        line (DLine): Directed line to compute sidedness with respect to
        r (Point): Point to compute sidedness for

    Returns:
        float: The sidedness.
               Positive for left
               Zero for on the line
               Negative for right
    """
    return LineSeg(line.p1, line.p2).cross(LineSeg(line.p1, r))


def sidedness_i(line: DLine, r: Point) -> int:
    """Computes if r is to the left, right, or on the directed line

    Args:
        line (DLine): Directed line to compute sidedness with respect to
        r (Point): Point to compute sidedness for

    Returns:
        int: +1 for Left, 0 for Colinear, -1 for Right
    """

    v = sidedness(line, r)
    if v < 0:
        return -1
    elif v > 0:
        return 1
    else:
        return 0


def intersection(seg1: LineSeg, seg2: LineSeg) -> bool:
    """Computes if two line segments intersect.
    An endpoint of one segment lying on the other does not count as intersection

    Args:
        seg1 (LineSeg): first segment
        seg2 (LineSeg): second segment

    Returns:
        bool: true if they intersect, false otherwise
    """
    line1 = DLine(seg1.p1, seg1.p2)
    line2 = DLine(seg2.p1, seg2.p2)
    return ((sidedness(line1, seg2.p1) < 0) != (sidedness(line1, seg2.p2) < 0)) \
        and ((sidedness(line2, seg1.p1) < 0) != (sidedness(line2, seg1.p2) < 0))


def area(p: Point, q: Point, r: Point) -> float:
    """Computes the area of the triangle defined by pqr

    Args:
        p (Point): First triangle point
        q (Point): Second triangle point
        r (Point): Third triangle point

    Returns:
        float: Area of triangle pqr
    """
    return 0.5 * math.fabs(LineSeg(p, q).cross(LineSeg(p, r)))


def angular_orientation(p: Point, q: Point) -> float:
    """Calculates angular direction of p relative to q about the origin

    Args:
        p (Point): Point to measure angular orientation to
        q (Point): Point to measure angular orientation from

    Returns:
        float: >0 if p is ccw from q. =0 if p is colinear with q. <0 if p is cw from q.
    """
    return angular_about_point(Point.origin(), p, q)


def angular_about_point(c: Point, p: Point, q: Point) -> float:
    """Calculates angular direction of p relative to q about the point c

    Args:
        c (Point): Center point to find angular orientation relative to
        p (Point): Point to measure angular orientation to
        q (Point): Point to measure angular orientation from

    Returns:
        float: >0 if p is ccw from q. =0 if p is colinear with q. <0 if p is cw from q.
    """
    return LineSeg(c, q).cross(LineSeg(c, p))


def tangency(p: Point, v: Point, u: Point, r: Point) -> bool:
    """Determines if pv is tangent to the convex polygon containing the turn rvu.

    rvu must not be colinear

    Args:
        p (Point): Exterior Point
        v (Point): Point of potential tangency
        u (Point): Point adjacent to v
        r (Point): Point adjacent to v

    Returns:
        bool: Tangency
    """
    line = DLine(p, v)
    return (sidedness(line, u) < 0) == (sidedness(line, r) < 0)


s = Point(1, 2)
a = Point(0, 1)
b = Point(1, 0)
c = Point(1, 4)
d = Point(2, 0)
e = Point(2, 3)
S1 = [d, b, a, c, s, e]
l1 = LineSeg(a, Point.origin())
l2 = LineSeg(Point(2, 2), Point(-2, 2))

S2 = [Point(0, 0), Point(1.12312, 2.4123), Point(3, 0), Point(
    0.124896, 0.9864231), Point(0, 3), Point(3, 3), Point(1, 2), Point(2, 1), ]

S3 = [Point(0, 0), Point(1.12312, 2.4123), Point(3, 1), Point(
    0.124896, 0.9864231), Point(1, 3), Point(3, 3), Point(1, 2), Point(2, 1), ]

S4 = [Point(-1, 0), Point(0, 1), Point(-1/math.sqrt(2), -
                                       1/math.sqrt(2)), Point(0, -1), Point(1, 0)]
