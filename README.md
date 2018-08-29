# IshiharaMC
Ishihara Test plates generated using Monte Carlo procedures

It uses a circle intersection algorithm, Jordan's curve theorem, and Monte Carlo placement to create an Ishihara test (Ishihara plate). The image to be created into an Ishihara plate must be an array of points in cartesian coordinates ordered such that the shape is generated in a clockwise fashion.  It is assumed that the points are joined by straight lines, and not spline curves (which greatly complicates the mathematics).  It is often easiest to increase the number of points in order to best represent the curves, which can usually be done with a vector graphics software (inkscape, etc.).

example code:
```python
import logo, scipy
angles = scipy.linspace(0,scipy.pi*2,4)[:3] #don't make the last and first points the same
v = .9
shape1 = scipy.array([v*scipy.cos(angles),v*scipy.sin(angles)]).T
angles += scipy.pi/3
shape2 = scipy.array([v*scipy.cos(angles),v*scipy.sin(angles)]).T
inp = (shape1,shape2)
output = scipy.array(logo.createPlate(inp))
idx1 = scipy.logical_xor(logo.circinPoly(inp[0],output),logo.circinPoly(inp[1],output))
idx2 = scipy.logical_and(logo.circinPoly(inp[0],output),logo.circinPoly(inp[1],output))
```

To do simple plotting:
```python
import matplotlib.pyplot as plt
plt.subplot(121)
logo.plotIshi(output,color='g')
logo.plotIshi(output[idx1],color='b')
logo.plotIshi(output[idx2],color='r')
plt.subplot(122)
logo.plotIshi(output)
plt.show() 
```

This should make a 6 pointed star

There is some functionality for setting the paint scheme, but generally logic based off the various objects should be known.
Depending on the color scheme, it could be 2 sets of 2 colors, 2 sets of 3 colors, etc.
