from subprocess import Popen, PIPE

tests = [([(-37, -25), (30, -39), (-24, -15), (50, -25), (-43, 33), (46, 24), (16, 9), (-46, -19), (-50, 47), (-50, 2),
           (-1, 11), (30, -17), (33, 9), (50, -3), (27, -50), (-47, -42), (37, -23), (21, 6), (49, -30)],(46, 24, -32, -13), 2886),
         ([(-1,2),(2,-1),(2,2)],(4,4,0,0), 3.5),
         ([(1, 1), (1, 2), (2, 2), (2, 3)], (4, 4, 0, 0),  1),
         ([(2, 2), (3, 3), (4, 2), (3, 0)], (4, 4, 0, 0),  3 ),
         ([(1, 3), (3, 2), (3, 5), (2, 5)], (4, 4, 0, 0),  2.75),
         ([(0, 1), (3, 0), (4, 2), (2, 4)], (4, 4, 0, 0),  8.5),
         ([(1, 1), (2, 0), (3, 2), (4, 1), (5, -1)], (4, 4, 0, 0),  4),
         ([(3, 2), (-1, 6), (-1, -2)], (4, 4, 0, 0),  8),
         ([(1, 2), (5, 6), (5, -2)], (4, 4, 0, 0),  8),
         ([(2, 1), (-3, 5), (7, 5)], (4, 4, 0, 0),  8.8),
         ([(2, 3), (-3, -1), (7, -1)], (4, 4, 0, 0),  8.8),
         ([(-1, 2), (2, -1), (5, -1), (5, 5), (-1, 5)], (4, 4, 0, 0),  15.5),
         ([(-1, -1), (2, -1), (5, 2), (5, 5), (-1, 5)], (4, 4, 0, 0), 15.5),
         ([(-1, -1), (5, -1), (5, 2), (2, 5), (-1, 5)], (4, 4, 0, 0), 15.5),
         ([(-1, -1), (-1, 2), (2, 5), (5, 5), (5, -1)], (4, 4, 0, 0), 15.5),
         ([(4, 1), (4, 3), (5, 3), (5, 1)], (4, 4, 0, 0), 0.0),
         ([(0, 0), (0, 4), (4, 4), (4, 0)], (4, 4, 0, 0), 16.0),
         ([(-1, 0), (-1, 4), (4, 4), (4, 0)], (4, 4, 0, 0), 16.0),
         ([(-1, -1), (-1, 5), (4, 5), (4, -1)], (4, 4, 0, 0), 16.0),
         ([(5, 0), (5, 4), (-1, 0), (-1, 4)], (4, 4, 0, 0), 16.0),
         ([(-1, -1), (3, -1), (5, 1), (5, 3), (3, 5), (-1, 5)], (4, 4, 0, 0), 16.0),
         ([(2, -1), (5, 2), (2, 5), (-1, 2)], (4, 4, 0, 0), 14.0),
         ([(2, -1), (5, 5), (5, 5), (-1, 2)], (4, 4, 0, 0), 11.0),
         ([(-1, -1), (-1, 5), (5, 5), (5, -1)], (4, 4, 0, 0), 16.0),
         ([(-1, -1), (3, -1), (5, 1), (5, 5), (-1, 5)], (4, 4, 0, 0), 16.0),]


def run_tests(tests):
    for test in tests:
        with open("a", "w") as f:
            f.write("%d" % len(test[0]))
            for point in test[0]:
                f.write(" %d %d" % (point[0],point[1]))
        with open("b", "w") as f:
            f.write("%d %d %d %d" % (test[1][0],test[1][1],test[1][2],test[1][3]))

        p = Popen(['python3', 'ConvexShape.py', 'b', 'a', 'DEBUG'], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        output, err = p.communicate()
        if abs(float(output) - float(test[2])) > 0.00001:
            print("excepted %f got %f" % (test[2], float(output)))
            print("(%s,%s,%f)," % (str(test[0]), str(test[1]), test[2]))
            return
        else:
            print("pass")

run_tests(tests)

