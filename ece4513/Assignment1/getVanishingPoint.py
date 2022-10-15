import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import ginput

POINTS = [
    # x1, y1, x2, y2
    [1114.166666666667, 1125.5952380952383, 1441.7857142857147, 1140.8333333333337], 
    [1270.3571428571431, 1262.7380952380954, 1658.928571428572, 1266.5476190476193],
    [984.2142857142856, 1944.642857142857, 749.9285714285713, 1893.2142857142858],
    [607.0714285714284, 1978.9285714285716, 418.49999999999983, 1910.357142857143],
    [1380.8781512605042, 1124.4747899159665, 1362.7268907563025, 261.2815126050423],
    [166.76050420168065, 1346.3235294117649, 180.87815126050407,1094.2226890756303]
]

class Line:

    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

        # ax + by + c = 0
        self.a = y1-y2
        self.b = x2-x1
        self.c = x1*y2-y1*x2

        self.length = get_point_dis((x1, y1), (x2, y2))
        self.tip =  (x1, y1) if(y1 < y2) else (x2, y2)
        self.bottom = (x1, y1) if(y1 > y2) else (x2, y2)


    def plot_line(self):
        plt.plot([self.x1, self.x2], [self.y1, self.y2], 'b')

    def normailize(self):
        k = np.sqrt(self.a**2 + self.b**2)
        self.a = self.a/k
        self.b = self.b/k
        self.c = self.c/k

def get_point_dis(pt1:tuple, pt2:tuple):
    return np.sqrt((pt1[0]-pt2[0])**2 + (pt1[1]-pt2[1])**2)

def get_line_cross(line1:Line, line2:Line):

    c = np.array([line1.c, line2.c]).T
    A = np.array([
        [line1.a, line1.b],
        [line2.a, line2.b]])

    cross = -np.dot(np.linalg.inv(A), c)
    u, v = cross[0], cross[1]
    plt.scatter([u], [v])
    
    # plot a intersection
    if(get_point_dis((line1.x1, line1.y1), (u, v)) > get_point_dis((line1.x2, line1.y2), (u, v))):
        # choose closer x2, y2 and draw line from line1(x2, y2) to (u,v)
        plt.plot([line1.x2, u], [line1.y2, v])
    else:
        # choose closer x1, y1 and draw line from line1(x2, y2) to (u,v)
        plt.plot([line1.x1, u], [line1.y1, v])

    if(get_point_dis((line2.x1, line2.y1), (u, v)) > get_point_dis((line2.x2, line2.y2), (u, v))):
        # choose closer x2, y2 and draw line from line2(x2, y2) to (u,v)
        plt.plot([line2.x2, u], [line2.y2, v])
    else:
        # choose closer x1, y1 and draw line from line2(x2, y2) to (u,v)
        plt.plot([line2.x1, u], [line2.y1, v])
    
    return u, v

def get_horizon_line(pt1:tuple, pt2:tuple):

    hor_line = Line(pt1[0], pt1[1], pt2[0], pt2[1])
    hor_line.normailize()
    return hor_line

# a question
def getVanishingPoint(im, manul = True, POINTS = POINTS):

    lines = []
    vps = []
    plt.imshow(im)

    if(manul == True):

        while True:
            print(' ')
            print('Click first point or click the same point twice to stop')

            x1,y1 = ginput(1)[0]

            print("report x1 = {}, y1 = {}".format( x1, y1))
            
            print('Click second point')
            x2,y2 = ginput(1)[0]
            print("report x2 = {}, y2 = {}".format( x2, y2))

            new_line = Line(x1, y1, x2, y2)
            new_line.plot_line()
            lines.append(new_line)

            # click one place for twice to end
            length = np.sqrt((y2-y1)**2 + (x2-x1)**2)
            if length < 0.0001:
                break        
    
    else:
        for i in range(len(POINTS)):
            point = POINTS[i]
            x1 = point[0]
            y1 = point[1]
            x2 = point[2]
            y2 = point[3]
            new_line = Line(x1, y1, x2, y2)
            new_line.plot_line()
            lines.append(new_line)

    print('find VP')
    # insert code here to compute vp (3-d vector in homogeneous coordinates)

    # get intersection 
    for i in range(len(lines)//2):
        cross = get_line_cross(lines[2*i], lines[2*i+1])
        vps.append(cross)
        print("Vinishing Point %d: (%f, %f)" %(i+1, vps[i][0], vps[i][1]))

    # get vinishing line
    hori_line = get_horizon_line(vps[0], vps[1])

    # show the line info and draw the line
    hori_line.plot_line()
    print("The vinishing line is: %fx + %fy + %f = 0"%(hori_line.a, hori_line.b, hori_line.c))
    
    return vps

# b quesiton
# Our assumption on K: unit aspect ratio & no skew
# [[f, 0, u0],
# [0, f, v0],
# [0, 0,  1]]
def get_intrinsic(vps:list):

    if(len(vps) != 3):
        print("not enough vanishing points given...")
        return

    vp1, vp2, vp3 = vps[0], vps[1], vps[2]
    # solve the least square problem
    u1, v1 = vp1
    u2, v2 = vp2
    u3, v3 = vp3
    # config Ab = zeros
    A = np.array([
        [u1*u2+v1*v2, u1+u2, v1+v2, 1],
        [u3*u2+v3*v2, u3+u2, v3+v2, 1],
        [u1*u3+v1*v3, u1+u3, v1+v3, 1]])

    # solve the eigen vector and value of ATA
    w, v = np.linalg.eig(np.dot(A.T, A))

    # b is the eigen vector of the smallest eigen value
    i_min = w.argmin()
    b = v[i_min]
    print("Ab = 0 by least squred solution b = {}\n".format(b))

    # get f, u0, v0
    f = np.sqrt(1/b[0])
    u0 = np.sqrt(-np.square(f)*b[1])
    v0 = np.sqrt(-np.square(f)*b[2])

    print("intrinsic argument solved, f = {}, u0 = {}, v0 = {}\n".format(f, u0, v0))
    K = np.array([
        [f, 0, u0],
        [0, f, v0],
        [0, 0, 1]])
    return K

# c question
# get rotation
def get_rotationM(vps:list, K:np.ndarray):

    if(len(vps) != 3):
        print("not enough vanishing points given...")
        return

    vp1 = np.array([vps[0][0], vps[0][1], 1])
    vp2 = np.array([vps[1][0], vps[1][1], 1])
    vp3 = np.array([vps[2][0], vps[2][1], 1])
    
    r1 = np.dot(np.linalg.inv(K), vp1)
    r1 = r1/np.linalg.norm(r1, ord=2)
    r2 = np.dot(np.linalg.inv(K), vp2)
    r2 = r1/np.linalg.norm(r2, ord=2)
    r3 = np.dot(np.linalg.inv(K), vp3)
    r3 = r1/np.linalg.norm(r3, ord=2)

    R = np.array([r1, r2, r3])

    print("The rotation matirx R is\n",R)
    return R

# d question


if __name__ == "__main__":
    im = plt.imread('./kyoto_street.JPG')
    vps = getVanishingPoint(im, manul=False)
    K = get_intrinsic(vps)
    
    # set the vanishing point as the given order:[right:X, vertival:Y, left:Z]
    order_vps = [vps[0], vps[2], vps[1]]
    R = get_rotationM(order_vps, K)
    plt.show()
