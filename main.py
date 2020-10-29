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

    def recalculate(self, a_x, a_y):
        self.x += self.vx * step + a_x * step ** 2 / 2
        self.y += self.vy * step + a_y * step ** 2 / 2

    def alpha(self, p):
        ang = atan((self.y - p.y) / (self.x - p.x))
        if self.x > p.x:
            ang += pi
        return abs(ang)

    def beta(self):
        if self.vx == 0:
            return pi / 2
        else:
            return abs(atan(self.vy / self.vx))


def dist(p1, p2):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


G = 6.67 * 10 ** -11
m1, m2, vx1, vy1, vx2, vy2, x1, y1, x2, y2 = 100, 5.9722 * 10 ** 24, 0, 7844, 0, 0, -6371000, 0, 0, 0
planet1 = Object(m1, x1, y1, vx1, vy1)
planet2 = Object(m2, x2, y2, vx2, vy2)

t = 0
step = 20
n = 50
name = "photos_" + str(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

r = dist(planet1, planet2)
F = G * planet1.m * planet2.m / r ** 2
e = planet1.m * (planet1.vx ** 2 + planet1.vy ** 2) / 2 - F * r

for i in range(n):
    r = dist(planet1, planet2)
    F = G * planet1.m * planet2.m / r ** 2
    e = planet1.m * (planet1.vx ** 2 + planet1.vy ** 2) / 2 - F * r
    v = sqrt(2 * e / planet1.m + 2 * G * planet2.m / r)
    alpha = planet1.alpha(planet2)
    a = F / planet1.m
    beta = planet1.beta()
    angle = beta - pi / 2 + alpha
    planet1.vn = v * cos(angle)
    planet1.vr = v * sin(angle)
    ay = a * sin(alpha)
    ax = a * cos(alpha)
    planet1.recalculate(ax, ay)
    r1 = dist(planet1, planet2)

    v = sqrt(2 * e / planet1.m + 2 * G * planet2.m / r1)
    planet1.vn = planet1.vn * r / r1
    planet1.vr = sqrt(v ** 2 - planet1.vn ** 2)
    alpha = planet1.alpha(planet2)
    planet1.vx = planet1.vr * cos(alpha) + planet1.vn * sin(alpha)
    planet1.vy = planet1.vr * sin(alpha) + planet1.vn * cos(alpha)

    current = os.getcwd()
    if not os.path.exists("{}\{}".format(current, name)):
        os.makedirs("{}\{}".format(current, name))
    plt.axis([-10000000, 10000000, -10000000, 10000000])
    plt.scatter(planet1.x, planet1.y, 100)
    plt.scatter(planet2.x, planet2.y, 2000)

    plt.savefig("{}\{}\{}.png".format(current, name, i), format="png", dpi=72)
    plt.close()


with imageio.get_writer('{}\{}\satellite.gif'.format(current, name), mode='I') as writer:
    for i in range(n):
        filename = str(i) + ".png"
        image = imageio.imread('{}\{}\{}'.format(current, name, filename))
        writer.append_data(image)