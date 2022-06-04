import matplotlib.pyplot as plt
import numpy as np
from random import random as rand
import pickle

#beast = pickle.load(open('beast2.p','rb'))

diamond = [np.array([[.5,0],[0,.5],[-.5,0],[0,-.5]])]

color1 = np.array([43.,172.,142.])/255 # hex 2bac90
color2 = np.array([242.,111.,41.])/255 # hex f26f29

r = []
g = []
r += [np.array([193.,21.,45.])/255] #c1152d
r += [np.array([226.,100.,78.])/255] #e2644e
g += [np.array([0.,141.,55.])/255] #008d37
g += [np.array([124.,188.,74.])/255] #7cbc4a


################################################
#              Monte-Carlo Routines            #
################################################


def genCirc(l=1., s=[.03,.06], n=3):
    """ place a circle of fractional radius s[0] to s[1]
    of l at n different sizes within l """

    temp = (s[1] - s[0])*np.ceil(n*rand())/n+s[0]
    return l*rand(), 2*np.pi*rand(), l*temp

def genIshi(num=1e4, l=1., s=[.03,.06], n=3, output=[],slim=.01):
    leng = len(output)
    for i in range(int(num)):
        valid = True
        j = 0
        test = genCirc(l=l, s=s, n=n) #get a random circle in range
        if test[0]+test[2] < l: # the edge of the new circle doesnt exceed large
            inpx = test[0]*np.cos(test[1])
            inpy = test[0]*np.sin(test[1])
            while valid:
                if j == leng: # test while loop across current set of circles
                    output += [[inpx,
                                inpy,
                                test[2]]] # add circle to list   
                    valid = False
                    leng += 1
                elif np.sqrt((output[j][0]-inpx)**2 + (output[j][1]-inpy)**2) < output[j][2]+test[2]+l*slim:
                    valid = False
                else:
                    j+=1

    return output    

def shapeIshi(shapes,num=1e4, l=1., s=[.03,.06], n=3, output=[],slim=.01):
    leng = len(output)
    for i in range(int(num)):
        valid = True
        j = 0
        test = genCirc(l=l, s=s, n=n) #get a random circle in range
        if test[0]+test[2] < l: # the edge of the new circle doesnt exceed large
            inpx = test[0]*np.cos(test[1])
            inpy = test[0]*np.sin(test[1])
            while valid:
                if j == leng: # test while loop across current set of circles
                    for k in shapes: # test circle to see if it intersects interior shape
                        valid = valid and shapeTest(k,np.array([inpx,inpy,test[2]]))
                            
                    if valid:
                        output += [[inpx,
                                    inpy,
                                    test[2]]] # add circle to list   
                        leng += 1
                            #plt.gca().add_artist(plt.Circle((inpx,inpy),test[2],fill=False,color='b'))
                            #plotShape(k)
                            #plotIshi(output)
                    valid = False

                elif np.sqrt((output[j][0]-inpx)**2 + (output[j][1]-inpy)**2) < output[j][2]+test[2]+l*slim:
                    valid = False
                else:
                    j+=1

    return output    


################################################
#                Staging Routines              #
################################################

def test(l=1.):
    output = genIshi(l=l,s=[.03,.06])
    print('step1')
    output = genIshi(num=2e4,l=l,s=[.02,.05],output=output)
    print('step2')
    output = genIshi(num=5e4,l=l,s=[.01,.04],output=output)
    print('step3')
    output = genIshi(num=1e5,l=l,s=[.0,.03],output=output)
    print('step4')
    return output

def test2(l=1.):
    output = shapeIshi(diamond,l=l,s=[.03,.06])
    print('step1')
    output = shapeIshi(diamond,num=2e4,l=l,s=[.02,.05],output=output)
    print('step2')
    output = shapeIshi(diamond,num=5e4,l=l,s=[.01,.04],output=output)
    print('step3')
    output = shapeIshi(diamond,num=1e5,l=l,s=[.0,.03],output=output)
    print('step4')    
    return output

def test3(l=1.):
    output = shapeIshi(beast,num=2e4,l=l,s=[.03,.06])
    print('step1')
    output = shapeIshi(beast,num=4e4,l=l,s=[.02,.05],output=output)
    print('step2')
    output = shapeIshi(beast,num=1e5,l=l,s=[.01,.04],output=output)
    print('step3')
    output = shapeIshi(beast,num=2e5,l=l,s=[.0,.03],output=output)
    print('step4')    
    return output

def createPlate(shape,l=1.,s=[[.03,.06],[.02,.05],[.01,.04],[.0,.03]],num=[1e4,2e4,5e4,1e5]):
    """ generates circles for an ishihara plate (inside a circle)


    Given an array of numpy/np arrays of X,Y coordinates describing a 2D polygon,
    it will randomly place circles of 


    Args:
        shape (Array-like): Array of cartesian-coordinates of the vertices of the polygon.
                            It is a list of numpy/np arrays, so that polygons may vary
                            in number of vertices with general shape: (polygon,coordinates,2).
                            X-coordinates for polygon i: (i,:,0)
                            Y-coordinates for polygon i: (i,:,1)

    Kwargs:
        l (float): Used to scale the size of the circle to encompass all polygons
        s (n x 2 array): is fractional size of the random circle to place (compare to large)
        num (n array): is the number of tries to attempt, later steps require more tries

    Returns:
        output (list): list of 3 elements which is the cartesian coordinates and size of circle

    """

    output = []
    
    for i in range(len(num)):
        print('step '+str(i+1)+' of '+str(len(num)))
        output = shapeIshi(shape,l=l,s=s[i],num=num[i],output=output) 
    return output

################################################
#               Plotting Routines              #
################################################

def plotShape(shape):
    plt.plot(shape[...,0],shape[...,1],'b')

    #plt.plot(np.concatenate((shapes[0],shapes[0][-1])),
    #         np.concatenate((shapes[1],shapes[1][-1])),':k')

def plotIshi(stuff, color=None):
    fig = plt.gca()
    if color is None:
        for i in stuff:
            temp = plt.Circle((i[0],i[1]),
                              i[2],
                              color='k',
                              fill=False)
            
            plt.gca().add_artist(temp)
    else:
        for i in stuff:
            temp = plt.Circle((i[0],i[1]),
                              i[2],
                              color=color,
                              fill=True)
            
            plt.gca().add_artist(temp)

            
    plt.axis([-1,1,-1,1])
    plt.gca().set_aspect('equal')

def plotIshiRG(stuff, color=r):
    fig = plt.gca()

    for i in stuff:
        val = int(round(rand()))
        temp = plt.Circle((i[0],i[1]),
                          i[2],
                          color=color[val],
                          fill=True)
            
        plt.gca().add_artist(temp)

            
    plt.axis([-1,1,-1,1])
    plt.gca().set_aspect('equal')
    plt.axis('off')
    #ax = plt.Axes(plt.gcf(), [0., 0., 1., 1.])
    #ax.set_axis_off()
    


################################################
#               Testing Routines               #
################################################
    
    
def circTest(pt1,pt2,circ,r):
    #print(pt1,pt2,circ,r)
    vec1 = pt2-pt1
    vec2 = circ-pt1
    A = np.sum(vec1**2)
    B = -2*np.sum(vec1*vec2)
    C = np.sum(vec2**2) - r**2
    temp = (B/(2*A))**2-(C/A) 

    if temp < 0: #line does not intersect circle at any point along line
        return False
    elif C < 0 or np.sum((circ-pt2)**2)-r**2 < 0:# one or both the endpoints are within the circle
        return True
    elif (-B/(2*A) - np.sqrt(temp) < 1 and -B/(2*A) - np.sqrt(temp) > 0) or (-B/(2*A) + np.sqrt(temp) < 1 and -B/(2*A) + np.sqrt(temp) > 0): #line intersects circle between bounds
        return True
    else:
        return False # line intersects, but not between pt1 to pt2

def shapeTest(pts,circ):
    for i in range(len(pts)): #while still a valid circle
        if circTest(pts[i],pts[i-1],circ[:2],circ[2]): #intersects a line
            return False
    
    return True # has gone through lines of shape with no intersections

def circinPoly(shape,ishi):
    # interface with inPolygon (Thanks John!!!)
    temp = np.array(shape)
    output = len(ishi)*[False]
    for i in range(len(ishi)):
        output[i] = inPolygon(shape[...,0],shape[...,1],ishi[i][0],ishi[i][1])

    return np.array(output)

def inPolygon(polyx, polyy, pointx, pointy):
    """Function calculating whether a given point is within a 2D polygon.

    Given an array of X,Y coordinates describing a 2D polygon, checks whether a
    point given by x,y coordinates lies within the polygon. Operates via a
    ray-casting approach - the function projects a semi-infinite ray parallel to
    the positive horizontal axis, and counts how many edges of the polygon this
    ray intersects. For a simply-connected polygon, this determines whether the
    point is inside (even number of crossings) or outside (odd number of
    crossings) the polygon, by the Jordan Curve Theorem.

    Args:
        polyx (Array-like): Array of x-coordinates of the vertices of the polygon.
        polyy (Array-like): Array of y-coordinates of the vertices of the polygon.
        pointx (Int or float): x-coordinate of test point.
        pointy (Int or float): y-coordinate of test point.

    Returns:
        result (Boolean): True/False result for whether the point is contained within the polygon.
    """
    #generator function for "lines" - pairs of (x,y) coords describing each edge of the polygon.
    def lines():
        p0x = polyx[-1]
        p0y = polyy[-1]
        p0 = (p0x,p0y)
        for i,x in enumerate(polyx):
            y = polyy[i]
            p1 = (x,y)
            yield p0,p1
            p0 = p1

    result = False
    for p0,p1 in lines():
        if ((p0[1] > pointy) != (p1[1] > pointy)) and (pointx < ((p1[0]-p0[0])*(pointy-p0[1])/(p1[1]-p0[1]) + p0[0])):
                result = not result

    return result
