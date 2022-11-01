from typing import List
from primitives import *
import matplotlib.pyplot as plt

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

def scttr(S: List[Point]):
    #Scatters all the points in S
    xcoord = []
    ycoord = []
    for p in S:
        xcoord.append(p.x)
        ycoord.append(p.y)
    plt.scatter(xcoord,ycoord)
    plt.draw()
    plt.pause(wait)

# def connect(p1, p2):
#     line = plt.plot([p1.x, p2.x], [p1.y,p2.y])  #Return this line to be able to remove it in future if required
#     plt.draw()
#     plt.pause(1)
#     return line

def connectPoints(S):
    #Connects list of points in order
    # List should have at least two points
    lines = []
    for i in range(1,len(S)):
        line = plt.plot([S[i].x, S[i-1].x], [S[i].y, S[i-1].y])  #Return this line to be able to remove it in future if required
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
        plt.scatter(p.x,p.y , s=200)
    plt.draw()
    plt.pause(wait)


def quickhull(S: List[Point]) -> List[Point]:
    scttr(S)
    P = []
    a = leftmost(S)
    b = rightmost(S)
    markPoints([a,b])
    connectPoints([a,b])
    S1 = []
    S2 = []
    for p in S:
        if sidedness_i(DLine(a,b),p) == -1:
            S1.append(p)
        elif sidedness_i(DLine(b,a),p) == -1:
            S2.append(p)
    P.append(a)
    DD = findquickhull(S1,a,b)
    if len(DD)>0:
        P = P+DD
    P.append(b)
    DD = findquickhull(S2, b, a)
    if len(DD) > 0:
        P = P+DD
    return P

def findquickhull(S: List[Point], a, b) -> List[Point]:
    P = []
    if len(S)==0:
        return []
    else:
        farthest = S[0]
        for p in S:
            if area(p,a,b) > area(farthest,a,b):
                farthest = p
        markPoints([farthest])
        connectPoints([a, farthest, b])
        S1 = []
        S2 = []
        for p in S:
            if sidedness_i(DLine(a,farthest),p) == -1:
                S1.append(p)
            elif sidedness_i(DLine(farthest,b),p) == -1:
                S2.append(p)

        DD = findquickhull(S1, a, farthest)


        if len(DD) > 0:
            P= P+DD
        P.append(farthest)
        DD = findquickhull(S2, farthest, b)
        if len(DD) > 0:
            P = P+DD
        return P

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




if __name__ == '__main__':
    S = [Point(-1,0), Point(0,1), Point(-1/math.sqrt(2),-1/math.sqrt(2)), Point(0,-1), Point(1,0), Point(0.2,-0.2), Point(-0.5,-0.2)]
    # scttr(S)
    # # line = connect(Point(-1,0), Point(0,1))
    # lines = connectPoints([Point(-1,0), Point(0,1), Point(-1/math.sqrt(2),-1/math.sqrt(2)), Point(0,-1), Point(1,0)])
    # removeLines(lines)
    # markPoints([Point(-1,0), Point(0,1)])


    quickhull(S)
    # jarvis(S)
