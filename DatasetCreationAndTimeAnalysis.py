from Algorithm import *
import random
import math
import pickle
import time
import numpy as np

# def CreateSyntheticCircleDataset(n):
#     # Creates a synthetic dataset of n points where all the points lie on the circle
#     # This dataset will NOT be output sensitive
#     S = []
#     for i in range(n):
#         x = -1+2*random.random()
#         y = -1+2*random.random()
#         mag = math.sqrt(x**2 + y**2)
#         S.append(Point(x/mag, y/mag))
#     return S

def CreateCircleDataset(n, h):
    # Creates a synthetic dataset of n points where h points lie on the circle and n-h inside the circle
    # This dataset will be output sensitive if h<<n
    # This dataset will NOT be output sensitive if h=n
    S = []
    for i in range(h):
        x = -1+2*random.random()
        y = -1+2*random.random()
        mag = math.sqrt(x**2 + y**2)
        S.append(Point(x/mag, y/mag))
    for i in range(n-h):
        r = 0.99*math.sqrt(random.random())
        angle = random.random()
        x = r*math.cos(2*math.pi*angle)
        y = r*math.sin(2*math.pi*angle)
        S.append(Point(x,y))


    return S


def saveDataset(filename, data):
    with open(filename, 'wb') as handle:
        pickle.dump(data, handle)

def loadDataset(filename):
    with open(filename, 'rb') as handle:
        data = pickle.load(handle)
    return data


def CalculateAvgTime(whichAlgorithm,n,h,max_iter):
    # whichAlgorithm is a list of name of algorithm functions which we want to do time analysis for
    # h: number of points on the the circle of radius 1
    # n-h: number of points strictly inside the circle of radius 1
    # max_iter: number of iterations to average over


    T = np.zeros((len(whichAlgorithm), max_iter))

    for i in range(max_iter):
        S = CreateCircleDataset(n, h)
        print('iter = ', i)
        for j in range(len(whichAlgorithm)):
            start = time.time()
            eval(whichAlgorithm[j]+'(S)')
            end = time.time()
            T[j,i] = end-start


    return np.mean(T,axis=1)


if __name__ == '__main__':

    whichAlgorithm = ['divideConquer0', 'jarvis', 'andrew', 'quickhull']
    T = CalculateAvgTime(whichAlgorithm, 100000,3,10)
    print(T)


    # Example of using save and load functionality
    # S = CreateCircleDataset(10000,100)
    # saveDataset('myData', S)
    # SS = loadDataset('myData')
    # scttr(SS)


