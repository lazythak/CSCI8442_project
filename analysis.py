from algorithms import *
from animation_api import *
import random
import math
import pickle
import time
import json
import matplotlib.pyplot as plt


# Synthetic dataset creation

def CreateCircleDataset(n, h):
    # Creates a synthetic dataset of n points where h points lie on the circle and n-h inside the circle
    # This dataset will be output sensitive if h<<n
    # This dataset will NOT be output sensitive if h=n
    S = []
    scale = math.sqrt(1)
    for i in range(h):
        x = -1+2*random.random()
        y = -1+2*random.random()
        mag = math.sqrt(x**2 + y**2)
        S.append(Point(x*scale/mag, y*scale/mag))
    for i in range(n-h):
        r = 0.99*math.sqrt(random.random())
        angle = random.random()
        x = r*math.cos(2*math.pi*angle)
        y = r*math.sin(2*math.pi*angle)
        S.append(Point(x, y))

    return S


def CreateEvenCircleDataset(n: int) -> List[Point]:
    """Creates a dataset of n points, spaced evenly around the unit circle
    Worst case data set for jarvis march

    Args:
        n (int): The number of points to generate

    Returns:
        List[Point]: The dataset around the unit circle
    """
    out = []

    theta = math.pi*2/n
    for i in range(0, n):
        out.append(Point(math.cos(theta * i), math.sin(theta * i)))

    return out


def CreateQHWorstCase(n: int) -> List[Point]:
    """Creates a dataset with n points that meets the worst case for quickhull

    Args:
        n (int): The number of points to generate

    Returns:
        List[Point]: The dataset produced
    """
    out = [Point(1, 0)]

    theta = math.pi
    for _ in range(1, n):
        out.append(Point(math.cos(theta), math.sin(theta)))
        if theta == 0:
            print("ZERO THETA")
            return out
        theta = theta/2

    return out


def CreateAndrewWorstCase(n: int) -> List[Point]:
    """Creates a dataset with n points that meets the worst case for andrew's algorithm.
    To do this, it places points with an upwards curve, and then places the final point below the leftmost point.
    There is no constant bound on the location of points that all points will be within.

    Args:
        n (int): The number of points to generate

    Returns:
        List[Point]: The dataset generated
    """

    out = [Point.origin()]
    for i in range(1, n-1):
        out.append(Point(i, math.pow(i, 1.1)))
    out.append(Point(n, -1))
    return out


def LimitH(S: List[Point]) -> List[Point]:
    """Limits the output size of the input to 3. Requires that S be within the unit disk

    Args:
        S (List[Point]): The input dataset, contained within the unit disk

    Returns:
        List[Point]: An output dataset, consisting of all points in S, bounded by a triangle
    """
    out = S.copy()
    out.append(Point(-10, -10))
    out.append(Point(0, 10))
    out.append(Point(10, -10))
    return out


# Real-world datasets

def btbDataset():
    # Real Dataset 1: This dataset contains the locations of the farms where bovine tuberculosis was detected along with the
    # years in which it was detected and the "spoligotype" of the tuberculosis
    S = []
    S9, S12, S15, S20 = [], [], [], []
    with open("btb.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        eval('S'+L[2][i]['spoligotype']+'.append(Point(L[0][i],L[1][i]))')

    (fig, ax) = new_plot()
    plot_points(S9, ax, c="g", wait=0, label='spoligotype: 9')
    plot_points(S12, ax, c="b", wait=0, label='spoligotype: 12')
    plot_points(S15, ax, c="r", wait=0, label='spoligotype: 15')
    plot_points(S20, ax, c="k", wait=0, label='spoligotype: 20')
    plt.title("Bovine Tuberculosis Dataset")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.legend(loc="upper left")
    plt.show()

    return S9+S12+S15+S20


def beiDataset():
    # Real Dataset 2: Location of 3605 trees in a tropical rain-forest
    S = []
    with open("bei.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        S.append(Point(L[0][i], L[1][i]))

    (fig, ax) = new_plot()
    plot_points(S, ax, c="g", wait=0)
    plt.title("Beilschmiedia data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()

    return S


def mucosaDataset():
    # Real Dataset 3: Location of two types of cells in the gastric mucosa of a rat
    SECL, Sother = [], []
    with open("mucosa.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        eval('S'+L[2][i]+'.append(Point(L[0][i],L[1][i]))')

    (fig, ax) = new_plot()
    plot_points(SECL, ax, c="g", wait=0, label='ECL')
    plot_points(Sother, ax, c="b", wait=0, label='other')
    plt.title("Mucosa data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.legend()
    plt.show()

    return SECL+Sother


def gorillaDataset():
    # Real Dataset 3: Location of nesting sites of Gorillas in National park in Cameron
    S = []
    with open("gorillas.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        S.append(Point(L[0][i], L[1][i]))

    (fig, ax) = new_plot()
    plot_points(S, ax, c="g", wait=0)

    plt.title("Gorilla data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()

    return S


def nbfiresDataset():
    # Real Dataset 3: Records of forest fires provided by New Brunsvick Department of Natural Resources of the fires between 1987
    #                   and 2003
    S = []
    with open("nbfires.json") as f:
        L = json.load(f)
    for i in range(len(L[0])):
        S.append(Point(L[0][i], L[1][i]))

    (fig, ax) = new_plot()
    plot_points(S, ax, c="g", wait=0)

    plt.title("NBfires data")
    plt.xlabel("x-coordinate")
    plt.ylabel("y-coordinate")
    plt.show()

    return S


# Dataset save/load

def saveDataset(filename, data):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle)


def loadDataset(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data


# Algorithm analysis

def timeFuncs(algs, S: List[Point], process=True, n=1_000_000):
    """Calls all algorithms in algs on the dataset S for n times, and averages the time taken

    Args:
        algs (_type_): A list of function objects to call
        S (List[Point]): The dataset to run the functions on
        process (bool, optional): Use cpu time. When false, uses wall time. Defaults to True.
        n (_type_, optional): The number of times to run each algorithm. Defaults to 1_000_000.

    Returns:
        Liat[float]: The average times for each algorithm provided, in the order of the algorithms in algs
    """

    import timeit
    env = globals()
    env['S'] = S
    out = []
    timer = timeit.default_timer
    if process:
        timer = time.process_time
    for alg in algs:
        out.append(timeit.timeit(lambda: alg(S),
                   number=n, timer=timer, globals=env)/n)
    return out


all_algs = [jarvis, andrew, chan, quickhull, divideConquer_unsorted]


if __name__ == '__main__':

    # whichAlgorithm = ['divideConquer_unsorted', 'jarvis', 'andrew', 'quickhull', 'chan']
    # T = CalculateAvgTime(whichAlgorithm, 1000, 3, 1)
    # print(T)

    # Example of using save and load functionality
    # S = CreateCircleDataset(10000,100)
    # saveDataset('myData', S)
    # SS = loadDataset('myData')
    # scttr(SS)

    # S = mucosaDataset()
    S = nbfiresDataset()
