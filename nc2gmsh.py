#!/usr/bin/env python

import numpy as np
import netCDF4 as NC
import pylab as plt

from argparse import ArgumentParser
parser = ArgumentParser()
parser.description = ""
parser.add_argument("FILE", nargs=1)
parser.add_argument("-o", dest="output", default="dem.geo")
parser.add_argument("-m", dest="min_size", type=float, default=1.0)
parser.add_argument("-M", dest="max_size", type=float, default=10.0)
options = parser.parse_args()

nc = NC.Dataset(options.FILE[0])

usurf = np.squeeze(nc.variables['usurf'][:])
thk = np.squeeze(nc.variables['thk'][:])

# convert to km:
x = nc.variables['x'][:] / 1000.0
y = nc.variables['y'][:] / 1000.0

width = x.max() - x.min()
height = y.max() - y.min()
x_min = x.min()
y_min = y.min()

output = open(options.output, mode="w")

output.write("""
lc = %f;
w  = %f;
h  = %f;
Point(1) = {0.0, 0.0, 0.0, lc};
Point(2) = {w,   0.0, 0.0, lc}; 
Point(3) = {w,   h,   0.0, lc};
Point(4) = {0.0, h,   0.0, lc};
Line(1) = {3,2};
Line(2) = {2,1};
Line(3) = {1,4};
Line(4) = {4,3};

Line Loop(5) = {1,2,3,4}; Plane Surface(6) = {5};
""" % (options.max_size, width, height))

point_counter = 10
node_list = []

def print_zero_contour(output_file, x, y, variable):
    global point_counter, node_list
    for c in plt.contour(x, y, variable, levels=[0]).collections:
        for p in c.get_paths():
            for v in p.vertices:
                x,y = v
                output.write("Point(%d) = {%f, %f, 0.0, %f};\n" % (point_counter, x - x_min, y - y_min, options.max_size))
                node_list.append(point_counter)
                point_counter += 1

print_zero_contour(output, x, y, usurf)
print_zero_contour(output, x, y, thk)

# define the attractor field
output.write("""
Field[1] = Attractor;
Field[1].NodesList = {%s};
""" % ",".join(map(lambda(x): str(x), node_list)))

output.write("""
Field[2] = Threshold;
Field[2].IField = 1;
Field[2].LcMin = %f;
Field[2].LcMax = %f;
Field[2].DistMin = 2.0*%f;
Field[2].DistMax = 20.0*%f;

Background Field = 2;
""" % (options.min_size, options.max_size,
       options.min_size, options.min_size))

output.close()

nc.close()
