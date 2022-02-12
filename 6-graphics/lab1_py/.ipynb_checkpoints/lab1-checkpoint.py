import numpy as np
import matplotlib.pyplot as plt

W = 1
B = 0


def build_simple_line(x1, x2, y1, y2):
    if x1 != x2 and y1 != y2:
        raise ValueError("Simple line must be parallel to X or Y axis")

    if x1 == x2:
        return np.stack([np.full(y2 - y1 + 1, x1), np.arange(y1, y2 + 1)]).T

    return np.stack([np.arange(x1, x2 + 1), np.full(x2 - x1 + 1, y1)]).T


def build_line_1(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return build_simple_line(x1, x2, y1, y2)
    dir = np.array([x2 - x1, y2 - y1])
    dir = dir / np.linalg.norm(dir)

    p = np.array([x1,y1])
    line = [p]
    
    while p[0] <= x2:
        p = np.floor(p+dir)
        if p != line[-1]:
            line.append(p)

    return line


def rect(canvas, color=0, x1=0, y1=0, x2=None, y2=None):
    if x2 is None:
        x2 = canvas.shape[0]
    if y2 is None:
        y2 = canvas.shape[1]

    canvas[x1:x2 + 1, y1:y2 + 1] = color
    return canvas


def draw(canvas, points, color=1):
    for p in points:
        canvas[p] = color
    return canvas


def show(canvas):
    return plt.imshow(canvas)
