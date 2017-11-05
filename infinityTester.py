from subprocess import Popen, PIPE
from random import randint

j = 0
bound =10
while j<10000:
    up = randint(-bound,bound)
    left = randint(-bound,bound)
    down = randint(-bound,up)
    right = randint(left,bound)
    points = []
    for i in range(randint(0, 20)):
        points.append((randint(-bound,bound),randint(-bound,bound)))

    with open("a", "w") as f:
        f.write("%d" % len(points))
        for point in points:
            f.write(" %d %d" % (point[0],point[1]))
    with open("b", "w") as f:
        f.write("%d %d %d %d" % (right,up,left,down))

    p = Popen(['python3', 'ConvexShape.py', 'b', 'a'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output1, err = p.communicate() #0

    p = Popen(['java', '-jar', 'Assignment1b.jar', 'b', 'a'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output2, err = p.communicate() #2886


    try:
        if abs(float(output1) - float(output2)) > 0.00001:
            print("excepted %f got %f" % (float(output1), float(output2)))
            print("(%s\n %d %d %d %d)" % (str(points), right, up, left,down))
            break
    except:
        print("(%s\n %d %d %d %d)" % (str(points), right, up, left, down))
        print("%d %s %s" % (j, output1, output2))
        break
    j+=1

print("end")


