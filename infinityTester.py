from subprocess import Popen, PIPE
from random import randint

j = 0
while j<10000:
    up = randint(-1000,1000)
    left = randint(-1000,1000)
    down = randint(-1000,up)
    right = randint(left,1000)
    points = []
    for i in range(randint(0, 50)):
        points.append((randint(-1000,1000),randint(-1000,1000)))

    with open("a", "w") as f:
        f.write("%d" % len(points))
        for point in points:
            f.write(" %d %d" % (point[0],point[1]))
    with open("b", "w") as f:
        f.write("%d %d %d %d" % (right,up,left,down))

    p = Popen(['python3', 'ConvexShape.py', 'a', 'b', 'DEBUG'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output1, err = p.communicate()

    p = Popen(['java', '-jar', 'Assignment1b.jar', 'b', 'a'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output2, err = p.communicate()

    if abs(float(output1) - float(output2)) > 0.00001:
        print("excepted %f got %f" % (float(output1), float(output2)))
        print("(%s\n %d %d %d %d)" % (str(points), right, up, left,down))
        break

    print(j)
    j+=1


