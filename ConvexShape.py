import matplotlib.pyplot as plt
import sys  # command args

DEBUG = True
infinitimal = 0.000001
class point:
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def __eq__(self, other):
        if(other == None):
            return False
        return abs(self.x - other.x) < infinitimal and abs(self.y - other.y) < infinitimal
    def __hash__(self):
        return hash((self.x,self.y))


class line:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def inside(self, point):
        return 0 <= point.x - min(self.start.x, self.end.x) <= max(self.start.x, self.end.x) - min(self.start.x, self.end.x) and \
               0 <= point.y - min(self.start.y, self.end.y) <= max(self.start.y, self.end.y) - min(self.start.y, self.end.y)


class convex:
    def __init__(self, points):
        self._points = points
        self.lines =  [line(v,w) for v,w in zip(self._points[:-1],self._points[1:])]
        self.points = points[:-1]
    def __len__(self):
        return len(self.points)

class rect:
    def __init__(self, up, down, left, right):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        if down >= up or left >= right:
            print("0.0")
            exit()
        self.corners = [point(left,down),point(right,down),point(right,up),point(left,up)]
        self.lines = [line(v,w) for v,w in zip(self.corners[:-1],self.corners[1:])]
        self.lines.append(line(self.corners[-1],self.corners[0]))
        self.c = convex(self.corners + [self.corners[0]])

    def inside(self, point):
        return self.left <= point.x <= self.right and self.down <= point.y <= self.up

def plotter(points , c,  r, intersection):
    scatter_points = [(point.x, point.y) for point in points]
    plt.scatter(*zip(*scatter_points), s=10)
    for line in c.lines:
        plt.plot((line.start.x,line.end.x), (line.start.y,line.end.y), linewidth = 1, marker='', color='r')

    for line in r.lines:
        plt.plot((line.start.x, line.end.x), (line.start.y, line.end.y), linewidth=1, marker='', color='g')

    scatter_intersection = [(point.x, point.y) for point in intersection.points]
    plt.fill(*zip(*scatter_intersection), 'k', alpha=0.3)
    plt.show()


def orientation(l, p):
    return (l.end.x - l.start.x)*(p.y - l.start.y) - (p.x - l.start.x)*(l.end.y - l.start.y)


def get_convex_hull(points):
    points.sort(key=lambda tup: (tup.x,tup.y))
    lower_convex_points = points[0:2]
    upper_convex_points = points[0:2]

    for p in points[2:]:
        if p == lower_convex_points[-1]:
            continue
        while len(lower_convex_points) > 1 and orientation(line(lower_convex_points[-2],lower_convex_points[-1]), p) <= 0:
            lower_convex_points.pop()
        lower_convex_points.append(p)

        while len(upper_convex_points) > 1 and orientation(line(upper_convex_points[-2],upper_convex_points[-1]), p) >= 0:
            upper_convex_points.pop()
        upper_convex_points.append(p)

    return convex(lower_convex_points + upper_convex_points[-2::-1])


def get_convex_size(c):
    return 0.5 * sum(l.start.x*l.end.y - l.start.y*l.end.x for l in c.lines)


def get_convexes_intersection(c, r):
    intersection = []
    for l in c.lines:
        points = rect_line_intersection(r,l)
        if not r.inside(l.start) and len(points)>0 and len(intersection)>0:
            intersection += connect_points_via_rect_corners(r, line(intersection[-1], points[0]))
        intersection += points

    if len(intersection) < 2:
        r_inters = [lines_intersection(convex_line,rect_line,False) for convex_line in c.lines for rect_line in r.lines]
        r_inters = [p for p in r_inters if p != None]
        if  any(p for p in r_inters if p.y == r.up and p.x <= r.left) and any(p for p in r_inters if p.y == r.up and p.x >= r.right) and \
            any(p for p in r_inters if p.y == r.down and p.x <= r.left) and any(p for p in r_inters if p.y == r.down and p.x >= r.right) and \
            any(p for p in r_inters if p.x == r.left and p.y <= r.down) and any(p for p in r_inters if p.x == r.left and p.y >= r.up) and \
            any(p for p in r_inters if p.x == r.right and p.y <= r.down) and any(p for p in r_inters if p.x == r.right and p.y >= r.up):
            return r.c
        return convex([])

    points = rect_line_intersection(r, c.lines[0])
    if len(points) > 0 and points[0] == intersection[0] and r.inside(c.points[0]):
        intersection.append(points[0])
        return convex(intersection)
    printer("continue")
    printer(intersection)
    if intersection[0] != intersection[-1]:
        intersection += connect_points_via_rect_corners(r, line(intersection[-1], intersection[0]))
        intersection.append(intersection[0])

    return convex(intersection)

def dot(p1, p2):
    return p1.x * p2.x + p1.y * p2.y

def det(p1, p2):
    return p1.x * p2.y - p1.y * p2.x

def angle(lineA, lineB):
    lA = point(lineA.start.x-lineA.end.x, lineA.start.y-lineA.end.y)
    lB = point(lineB.start.x-lineB.end.x, lineB.start.y-lineB.end.y)

    return dot(lA, lB)/(dot(lA, lA)**0.5)/(dot(lB, lB)**0.5)

def connect_points_via_rect_corners(r, l):
    relevant_corners = [corner for corner in r.corners if orientation(l,corner) < 0]
    assert len(relevant_corners) < 4

    relevant_corners.sort(key=lambda point: angle(l,line(l.end,point)))
    return relevant_corners

def lines_intersection(line1, line2, in_line_2 = True):
    xdiff = point(line1.start.x - line1.end.x, line2.start.x - line2.end.x)
    ydiff = point(line1.start.y - line1.end.y, line2.start.y - line2.end.y)

    div = det(xdiff, ydiff)
    if div == 0:
       return None

    d = point(det(line1.start,line1.end), det(line2.start,line2.end))
    intersection = point(det(d, xdiff) / div, det(d, ydiff) / div)

    if line1.inside(intersection) and ((not in_line_2) or line2.inside(intersection)):
        return intersection

    return None


def rect_line_intersection(r, l):
    intersection = [lines_intersection(l,rect_line) for rect_line in r.lines]
    intersection = list(set([intersect for intersect in intersection if intersect is not None and intersect != l.start]))
    intersection.sort(key=lambda p: (p.x - l.start.x)**2 + (p.y-l.start.y) ** 2)
    if r.inside(l.end) and l.end not in intersection:
        intersection.append(l.end)
    return intersection


def read_points():
    with open(sys.argv[1]) as f:
        numbers = [int(x) for x in next(f).split()]
        assert len(numbers) == numbers[0] * 2 + 1
        return [point(x,y) for x,y in zip(numbers[1::2],numbers[2::2])]

def read_rect():
    with open(sys.argv[2]) as f:
        right,up,left,down = [int(x) for x in next(f).split()]
        return rect(up,down,left,right)

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
r = read_rect()


convex_hull = get_convex_hull(points)
if len(convex_hull) < 3:
    print(0.0)
    exit()

printer(convex_hull)
intersection = get_convexes_intersection(convex_hull, r)
printer(intersection)
result = get_convex_size(intersection)
print(result)
if(DEBUG):
    create_test(result)
    plotter(points,convex_hull, r, intersection)
