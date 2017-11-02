import matplotlib.pyplot as plt
import sys  # command args

DEBUG = True

def plotter(points , convex,  rect, intersection):
    plt.scatter(*zip(*points), s=10)
    for v, w in zip(convex[:-1], convex[1:]):
        plt.plot((v[0],w[0]), (v[1],w[1]), linewidth = 6, marker='', color='r')

    rect_convex = rect_corners(rect)
    rect_convex.append(rect_convex[0])
    for v, w in zip(rect_convex[:-1], rect_convex[1:]):
        plt.plot((v[0],w[0]), (v[1],w[1]), linewidth = 4, marker='', color='g')

    plt.fill(*zip(*intersection), 'k', alpha=0.3)
    plt.show()


def orientation(lineStart, lineEnd, point):
    return (lineEnd[0] - lineStart[0])*(point[1] - lineStart[1]) - (point[0] - lineStart[0])*(lineEnd[1] - lineStart[1])


def get_convex_hull(points):
    points.sort(key=lambda tup: (tup[0],tup[1]))
    lower_convex_points = points[0:2]
    upper_convex_points = points[0:2]

    for point in points[2:]:
        if point == lower_convex_points[-1]:
            continue
        while len(lower_convex_points) > 1 and orientation(lower_convex_points[-2],lower_convex_points[-1], point) < 0:
            lower_convex_points.pop()
        lower_convex_points.append(point)

        while len(upper_convex_points) > 1 and orientation(upper_convex_points[-2],upper_convex_points[-1], point) > 0:
            upper_convex_points.pop()
        upper_convex_points.append(point)

    return lower_convex_points + upper_convex_points[-2::-1]


def get_convex_size(convex):
    return 0.5 * sum(v[0]*w[1] - v[1]*w[0] for v, w in zip(convex[:-1], convex[1:]))


def get_convexes_intersection(convex, rect):
    intersection = []
    for v,w in zip(convex[:-1], convex[1:]):
        points = rect_line_intersection(rect,v,w)
        if not in_rect(rect, v) and len(points)>0 and len(intersection)>0:
            intersection += connect_points_via_rect_corners(rect, intersection[-1], points[0])
        intersection += points

    points = rect_line_intersection(rect, convex[0], convex[1])
    if len(points) > 0 and points[0] == intersection[0] and in_rect(rect, convex[0]):
        return intersection + [points[0]]
    printer("continue")
    printer(intersection)
    if intersection[0] != intersection[-1]:
        intersection += connect_points_via_rect_corners(rect, intersection[-1], intersection[0]) + [intersection[0]]

    return intersection

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(lineA, lineB):
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    return dot_prod/magA/magB

def connect_points_via_rect_corners(rect, start, end):
    relevant_corners = []
    for corner in rect_corners(rect) :
        if orientation(start, end, corner) < 0:
            pass

    relevant_corners = [corner for corner in rect_corners(rect) if orientation(start,end,corner) < 0]
    assert len(relevant_corners) < 4

    relevant_corners.sort(key=lambda point: ang((start,end),(end,point)))
    return relevant_corners


def rect_corners(rect):
    if rect_corners.corners == None:
        rect_corners.corners = [(rect["left"],rect["down"]),(rect["right"],rect["down"]),
                                (rect["right"],rect["up"]),(rect["left"],rect["up"])]
    return rect_corners.corners
rect_corners.corners = None


def rect_lines(rect):
    if rect_lines.lines == None:
        rect_lines.lines = [a for a in zip(rect_corners(rect), rect_corners(rect)[1:] + [rect_corners(rect)[0]])]
    return rect_lines.lines
rect_lines.lines = None


def in_rect(rect, point):
    return rect["left"] <= point[0] <= rect["right"] and rect["down"] <= point[1] <= rect["up"]


def lines_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1]) #Typo was here

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    def in_line(line, point):
        return  0 <= point[0] - min(line[0][0], line[1][0]) <= max(line[0][0], line[1][0]) - min(line[0][0], line[1][0]) and \
                 0 <= point[1] - min(line[0][1], line[1][1]) <= max(line[0][1], line[1][1]) - min(line[0][1], line[1][1])
    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    if in_line(line1, (x,y)) and in_line(line2,(x,y)):
        return (x, y)

    return None


def rect_line_intersection(rect, start_line, end_line):
    intersection = [lines_intersection((start_line,end_line),line) for line in rect_lines(rect)]
    intersection = [intersect for intersect in intersection if intersect is not None]
    intersection.sort(key=lambda p: (p[0] - start_line[0])**2 + (p[1]-start_line[1]) ** 2)
    if in_rect(rect,end_line) and end_line not in intersection:
        intersection.append(end_line)
    return intersection


def read_points():
    with open(sys.argv[1]) as f:
        numbers = [int(x) for x in next(f).split()]
        assert len(numbers) == numbers[0] * 2 + 1
        return [(x,y) for x,y in zip(numbers[1::2],numbers[2::2])]

def read_rect():
    with open(sys.argv[2]) as f:
        right,up,left,down = [int(x) for x in next(f).split()]
        return {"up":up,"right":right,"left":left,"down":down}

def printer(s):
    if(DEBUG):
        print(s)

def create_test(result):
    s = '(['
    with open('points.txt') as points:
        numbers = [int(x) for x in next(points).split()]
        s += ','.join(['(%d,%d)' % (x, y) for x, y in zip(numbers[1::2], numbers[2::2])])
    s += '],('
    with open('rect.txt') as rect:
        s += ','.join([x for x in next(rect).split()])

    s += '), %s),' % str(result)
    print(s)

if len(sys.argv) == 4 and sys.argv[3] == 'DEBUG':
    DEBUG = False

points = read_points()
rect = read_rect()
convex_hull = get_convex_hull(points)
printer(convex_hull)
intersection = get_convexes_intersection(convex_hull, rect)
printer(intersection)
result = get_convex_size(intersection)
print(result)
if(DEBUG):
    create_test(result)
    plotter(points,convex_hull, rect, intersection)
