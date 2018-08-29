# IshiharaMC
Ishihara Test plates generated using Monte Carlo procedures

It uses a circle intersection algorithm, Jordan's curve theorem, and Monte Carlo placement to create an Ishihara test (Ishihara plate). The image to be created into an Ishihara plate must be an array of points in cartesian coordinates ordered such that the shape is generated in a clockwise fashion.  It is assumed that the points are joined by straight lines, and not spline curves (which greatly complicates the mathematics).  It is often easiest to increase the number of points in order to best represent the curves, which can usually be done with a vector graphics software (inkscape, etc.).
