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


def build_line_0(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return build_simple_line(x1, x2, y1, y2)
    dir = np.array([x2 - x1, y2 - y1])
    dir = dir / np.linalg.norm(dir)
    # print("direction:", dir)

    p = np.array([x1 + 0.0, y1 + 0.0])
    line = [p.astype(int)]

    while p[0] <= x2:
        p += dir
        pfloor = p.astype(int)
        if (pfloor != line[-1]).any():
            line.append(pfloor)

    return line


def build_line_1(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return build_simple_line(x1, x2, y1, y2)

    dir = np.array([x2 - x1, y2 - y1])
    if dir[0] > dir[1]:
        # possible gaps in x
        k = dir[1] / dir[0]
        xs = np.arange(x1, x2 + 1)
        ys = np.linspace(y1, y2, (x2 - x1 + 1), endpoint=True).astype(int)
    else:
        # possible gaps in y
        k = dir[0] / dir[1]
        ys = np.arange(y1, y2 + 1)
        xs = np.linspace(x1, x2, (y2 - y1 + 1), endpoint=True).astype(int)

    return np.stack([xs, ys]).T


def build_line_textbook(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return build_simple_line(x1, x2, y1, y2)

    dir = np.array([x2 - x1, y2 - y1])
    if dir[0] > dir[1]:
        # possible gaps in x
        k = dir[1] / dir[0]
        xs = np.arange(x1, x2 + 1)
        ys = np.linspace(y1, y2, (x2 - x1 + 1), endpoint=True)
        ys = (ys + 0.5).astype(int)
    else:
        # possible gaps in y
        k = dir[0] / dir[1]
        ys = np.arange(y1, y2 + 1)
        xs = np.linspace(x1, x2, (y2 - y1 + 1), endpoint=True)
        xs = (xs + 0.5).astype(int)

    return np.stack([xs, ys]).T


def build_line_integer_bresenham(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return build_simple_line(x1, x2, y1, y2)

    dx = x2-x1
    dy = y2-y1
    line = []

    if dx > dy:
        # possible gaps in x
        D = (dy << 1) - dx
        y = y1

        for x in range(x1, x2+1):
            line.append((x,y))
            if D > 0:
                y += 1
                D -= dx << 1
            D += dy << 1
    else:
        # possible gaps in y
        D = (dx << 1) - dy
        x = x1

        for y in range(y1, y2+1):
            line.append((x,y))
            if D > 0:
                x += 1
                D -= dy << 1
            D += dx << 1

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
        # print(p)
        canvas[p[0], p[1]] = color
    return canvas


def show(canvas, *args, **kwargs):
    return plt.imshow(canvas.T, interpolation='none', origin='lower', *args, **kwargs)
