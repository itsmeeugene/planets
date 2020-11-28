from math import sqrt, sin, cos, atan, pi
import datetime
import os
import matplotlib.pyplot as plt
import imageio


class Object:
    def __init__(self, m, x, y, vx, vy):
        self.m = m
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def recalculate(self, a_x=0.0, a_y=0.0):
        self.x += self.vx * step + a_x * step ** 2 / 2
        self.y += self.vy * step + a_y * step ** 2 / 2

    def alpha(self, p):   # угол между горизонтом и радиус-вектором, направленным к спутнику
        ang = pi + atan((self.y - p.y) / (self.x - p.x))
        if self.x > p.x:
            ang += pi
        return ang

    def beta(self):     # угол между вектором скорости и горизонтом
        if self.vx == 0:
            return pi / 2
        else:
            return abs(atan(self.vy / self.vx))


def dist(p1, p2):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


G = 6.67 * 10 ** -11
m1, m2 = 100, 5.9722 * 10 ** 24
vx1, vy1 = 0, 18000
vx2, vy2 = 0, 5000
x1, y1 = -6371000, 0
x2, y2 = 0, 0

planet1 = Object(m1, x1, y1, vx1, vy1)
planet2 = Object(m2, x2, y2, vx2, vy2)
coords = []  # сохраняем траекторию

t = 0
step = 50
n = 150
name = "photos_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

r = dist(planet1, planet2)
F = G * planet1.m * planet2.m / r ** 2


for i in range(n):
    e = planet1.m * (planet1.vx ** 2 + planet1.vy ** 2) / 2 - F * r
    r = dist(planet1, planet2)
    F = G * planet1.m * planet2.m / r ** 2
    v = sqrt(2 * e / planet1.m + 2 * G * planet2.m / r)
    alpha = planet1.alpha(planet2)
    a = F / planet1.m
    beta = planet1.beta()
    # angle = pi / 2 - alpha + beta  # угол между вектором скорости и нормалью

    # planet1.vn = v * cos(pi - angle)
    # planet1.vr = v * sin(angle - pi)

    ay = -a * sin(pi - alpha)
    ax = a * cos(pi - alpha)

    planet1.recalculate(ax, ay)
    r1 = dist(planet1, planet2)
    v = sqrt(2 * e / planet1.m + 2 * G * planet2.m / r1)

    if abs(planet1.vx) < abs(planet1.vy):
        planet1.vx += ax * step
        if planet1.vy < 0:
            planet1.vy = -sqrt(v * v - planet1.vx ** 2)
        else:
            planet1.vy = sqrt(v * v - planet1.vx ** 2)
    else:
        planet1.vy += ay * step
        if planet1.vx < 0:
            planet1.vx = -sqrt(v * v - planet1.vy ** 2)
        else:
            planet1.vx = sqrt(v * v - planet1.vy ** 2)

    planet2.recalculate()

    print("v = ", v, "vx = ", planet1.vx, "vy = ", planet1.vy, "ax = ", ax, "ay = ", ay, "alpha = ", alpha, "e = ", e)

    coords.append((planet1.x, planet1.y))

    current = os.getcwd()
    if not os.path.exists("{}/{}".format(current, name)):
        os.makedirs("{}/{}".format(current, name))
    # plt.axis([-10000000, 10000000, -3000000, 50000000])

    left, width = .25, .5
    bottom, height = .25, .5
    right = left + width
    top = bottom + height

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_aspect(2)
    ax.text(right, top, '               e = {}'.format(round(e)),
            horizontalalignment='left',
            verticalalignment='top',
            transform=ax.transAxes)
    plt.scatter(planet1.x, planet1.y, 100)
    plt.scatter(planet2.x, planet2.y, 1000)
    for coord in coords:
        plt.scatter(coord[0], coord[1], 1, c='black')

    plt.savefig("{}/{}/{}.png".format(current, name, i), format="png", dpi=72)
    plt.close()


with imageio.get_writer('{}/{}/satellite.gif'.format(current, name), mode='I') as writer:
    for i in range(n):
        filename = str(i) + ".png"
        image = imageio.imread('{}/{}/{}'.format(current, name, filename))
        writer.append_data(image)

