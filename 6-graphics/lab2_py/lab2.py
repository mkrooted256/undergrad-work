import numpy as np
import matplotlib.pyplot as plt

W = 1
B = 0

def build_simple_line(x1, x2, y1, y2):
    if x1 != x2 and y1 != y2:
        raise ValueError("Simple line must be parallel to X or Y axis")

    if x1 == x2:
        y1, y2 = min(y1, y2), max(y1,y2)
        return list(np.stack([np.full(y2 - y1 + 1, x1), np.arange(y1, y2 + 1)]).T)

    x1, x2 = min(x1, x2), max(x1,x2)
    return list(np.stack([np.arange(x1, x2 + 1), np.full(x2 - x1 + 1, y1)]).T)


def build_line_integer_bresenham(x1, y1, x2, y2):
    if x1 == x2 or y1 == y2:
        return build_simple_line(x1, x2, y1, y2)

    dx = np.abs(x2-x1)
    dy = np.abs(y2-y1)
    sx = 1 if x2 > x1 else -1
    sy = 1 if y2 > y1 else -1
    line = []


    if dx > dy:
        # possible gaps in x
        D = (dy << 1) - dx
        y = y1

        for x in range(x1, x2+sx, sx):
            line.append((x,y))
            while D >= 0:
                y += sy
                D -= dx << 1
            D += dy << 1
    else:
        # possible gaps in y
        if x2 < x1:
            step = -1
        D = (dx << 1) - dy
        x = x1

        for y in range(y1, y2+sy, sy):
            line.append((x,y))
            while D >= 0:
                x += sx
                D -= dy << 1
            D += dx << 1

    return line

def f2p_from_xywh(w, h, dx, dy, w0, h0):
    kx, ky = w/dx, h/dy
    def f2p(points):
        return (points * np.array([[kx], [ky]]) + np.array([[w0],[h0]])).astype(int)
    return f2p

def build_bresenham_polygon(xs, ys, f2p= lambda x: x):
    curve = []
    xs, ys = f2p(np.stack([xs, ys]))

    for i in range(1,len(xs)):
        curve += build_line_integer_bresenham(xs[i-1], ys[i-1], xs[i], ys[i])
    
    return curve


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

