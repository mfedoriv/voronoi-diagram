import random
import colorsys
import math
from PIL import Image, ImageDraw


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        # brighter colors
        h_col, s_col, l_col = random.random(), 0.5 + random.random() / 2.0, 0.7 + random.random() / 5.0
        self.r, self.g, self.b = [int(256 * i) for i in colorsys.hls_to_rgb(h_col, l_col, s_col)]

        self.decay_func = [0, 0, 1]  # f = 1/(r^2)
        self.power = 1

    def get_distance(self, x, y):
        return math.hypot(self.x - x, self.y - y)

    def get_decay(self, x, y):
        r = self.get_distance(x, y)
        decay = 0
        for i in range(len(self.decay_func)):
            decay = decay + (self.decay_func[i] * r ** i)

        if decay == 0:
            return 0
        else:
            return self.power/decay


def get_manual_coord():

    points = [[85, 33],
              [6, 54],
              [47, 24]]

    points_list = []
    for i in points:
        print(f'{i[0]} {i[1]}\n')
        points_list.append(Point(i[0], i[1]))
    return points_list


def get_random_coord(imgx, imgy, num_points):
    points = []
    for i in range(num_points):
        points.append(Point(random.randrange(imgx), random.randrange(imgy)))
    return points


def get_hex_coord(imgx, imgy, size):
    points_list = []
    x = 0  # offset x
    y = 0  # offset y
    w = size * 2
    w_spacing = w * 3 / 4
    h = math.sqrt(3) * size  # sqrt(3) = sin(60°)
    i = 0

    while y < imgy + size:
        while x < imgx + size:
            points_list.append(Point(round(x, 5), round(y, 5)))
            x = x + w_spacing * 2
        if i % 2 == 0:
            x = w_spacing
        else:
            x = 0
        y = y + h / 2
        i = i + 1

    return points_list


def generate_voronoi_diagram(width, height, num_points, d_threshhold, type_coord, hex_size):
    image = Image.new("RGB", (width, height))
    putpixel = image.putpixel
    draw = ImageDraw.Draw(image)  # for drawing

    imgx, imgy = image.size

    points = []
    if type_coord == 'rand':
        points = get_random_coord(imgx, imgy, num_points)
    elif type_coord == 'hex':
        points = get_hex_coord(imgx, imgy, hex_size)
    elif type_coord == 'manual':
        points = get_manual_coord()
    else:
        raise Exception('Type can be \'rand\' or \'hex\'')

    print(f'Number of cells: {len(points)}\n')
    # ----------------------------------------------
    # points[0].decay_func = [0, 0, 3]
    # points[1].power = 5
    # ----------------------------------------------

    for y in range(imgy):
        for x in range(imgx):
            decay_max = 0

            j = -1
            for i in range(len(points)):
                d = points[i].get_decay(x, y)
                if d > decay_max:
                    decay_max = d
                    j = i
            if decay_max < d_threshhold:
                putpixel((x, y), (0, 0, 0))
            else:
                putpixel((x, y), (points[j].r, points[j].g, points[j].b))

    # draw Points
    p_size = 1
    for i in range(len(points)):
        draw.ellipse((points[i].x - p_size, points[i].y - p_size, points[i].x + p_size, points[i].y + p_size),
                     fill=(0, 0, 0), outline=(0, 0, 0))
        # putpixel((nx[i], ny[i]), (0, 0, 0))

    image.save("VoronoiDiagram.png", "PNG")
    image.show()
