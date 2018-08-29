# IshiharaMC
Ishihara Test plates generated using Monte Carlo procedures

It uses a circle intersection algorithm, Jordan's curve theorem, and Monte Carlo placement to create an Ishihara test (Ishihara plate). The image to be created into an Ishihara plate must be an array of points in cartesian coordinates ordered such that the shape is generated in a clockwise fashion.  It is assumed that the points are joined by straight lines, and not spline curves (which greatly complicates the mathematics).  It is often easiest to increase the number of points in order to best represent the curves, which can usually be done with a vector graphics software (inkscape, etc.).

example code:
```python
import logo, scipy, matplotlib.pyplot as plt
angles = scipy.linspace(0,scipy.pi*2,3)
v = .6
shape1 = scipy.array([v*scipy.cos(angles),v*scipy.sin(angles)]).T
angles += scipy.pi/3
shape2 = scipy.array([v*scipy.cos(angles),v*scipy.sin(angles)]).T
input = (shape1,shape2)
output = scipy.array(logo.createPlate(input))
idx = scipy.logical_xor(logo.circinPoly(input[0],output),logo.circinPoly(input[1],output))
logo.plotIshi(output)
logo.plotIshi(output[idx],color='k')
plt.show() 
'''

This should make a 6 pointed star
Text
