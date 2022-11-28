# Convex Hull Algorithms and Animations

This repository contains the code for the project for CSCI 8442 produced by Melissa Wenthin and Sarthak Jain. The project is a set of algorithms for computing the convex hull in 2D, along with synthetic and real-world datasets to run and test the algorithms on. Also included are animated versions of the algorithms, demonstrating how they function.

## Algorithms

The algorithms implemented are Chan's algorithm, Jarvis' algorithm, Andrew's algorithm, Divide and Conquer, and Quickhull, all of which function on python `List`s of `Point`s, where the `Point` type is defined within `primitives.py`. The algorithms are all defined within `algorithms.py`. The animated versions are located within `animated_algorithms.py`.

## Usage

These algorithms can be included in a project by importing `algorithms.py` and `primitives.py` into the file making use of them. `algorithms.py` is required to call the algorithms themselves, and `primitives.py` contains the definition of the `Point` type that is required to pass into each of the algorithms. The algorithms will return a `List` of `Point`s that contains the points on the convex hull, oriented in counterclockwise order.

To work with the project in an interactive environment, `terminal.py` is provided, which can be used to load all of the included files, types, and functions into the python interpreter. This can by done by starting the interpreter with `python -i terminal.py`.

## Animations

The animated versions of the algorithms have a similar type signature to the non-animated version, only adding an optional `wait` paramter that defines the time for each frame of the animation in seconds, defaulting to 1 second.

The colors used in the animations are made to be generally consistent in meaning across the various animations, though for some features that only exist in one algorithm, meanings may vary from the usual in the other algorithms. This primarily occurs in the divide and conquer algorithm.

Colors not mentioned below as applying to points are used to replace Green when Chan's algorithm is showing the subhulls it calculates. This also applies to the use of Andrew's algorithm to calculate those subhulls.

<br/>

### Point Colors

| Color              | Color Code          | Meaning                                                                                                                                                                               |
| :----------------- | :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dark Grey          | `'tab:grey'`        | Default point color                                                                                                                                                                   |
| Light Grey         | `'xkcd:light grey'` | Points not of interest or not available to current algorithm step                                                                                                                     |
| Green              | `'tab:green'`       | Points known to be on the hull                                                                                                                                                        |
| Orange             | `'tab:orange'`      | Candidate points. Not known to be on the hull, but current best known points or points under consideration                                                                            |
| Blue               | `'tab:blue'`        | Current point being examined by the algorithm                                                                                                                                         |
| Red                | `'tab:red'`         | Points that failed the current test. Occurs when point is on the wrong side of a line to be a new candidate point during a sidedness test, or when Chan's algorithm fails to converge |
| Olive/Yellow-Green | `'tab:olive'`       | Points that meet the current condition being checked for. Used to mark when the examined point will become the new candidate point in Jarvis march and Quickhull.                     |

<br/>

### Line Colors

| Color   | Color Code | Meaning                                                                                       |
| :------ | :--------- | :-------------------------------------------------------------------------------------------- |
| Black   | `'k'`      | Links points Candidates not known to be on the hull, or on the hull in that order             |
| Green   | `'g'`      | Links points known to be on the hull, in the marked order.                                    |
| Yellow  | `'y'`      | Links endpoint of candidate hull and new candidate point, marks potential edge to add to hull |
| Magenta | `'m'`      | Directed line in Sidedness tests                                                              |
| Red     | '`'r'`     | Hull segments when hull fails to converge                                                     |

<br/>

### Divide and Conquer Animation

The Divide and Conquer algorithm functions significantly differently than the other algorithms, so the color mappings used in the other algorithms don't apply well to it. Below are the colors and meanings used in Divide and Conquer

| Color      | Color Code              | Meaning                                                                                            |
| :--------- | :---------------------- | :------------------------------------------------------------------------------------------------- |
| Dark Grey  | `'tab:grey'`            | Default point color                                                                                |
| Light Grey | `'xkcd:light grey'`     | Points not of interest or not available to current algorithm step                                  |
| Blue       | `'xkcd:blue'`           | Left subhull in Divide and Conquer                                                                 |
| Purple     | `'xkcd:purple'`         | Right subhull in Divide and Conquer                                                                |
| Black      | `'k'`                   | Dividing line during Divide stage of Divide and Conquer                                            |
| Blue-Green | `'xkcd:blue green'`     | Combined hull after Merge stage of Divide and Conquer, Known upper and lower tangents when Merging |
| Yellow     | `'y'`                   | Candidate tangent when Merging in Divide and Conquer                                               |
| Green      | `'tab:green`' and `'g'` | Known correct hull points and edges between them                                                   |