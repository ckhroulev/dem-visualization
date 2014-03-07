#!/usr/bin/env python

import numpy as np

from argparse import ArgumentParser
parser = ArgumentParser()
parser.description = ""
parser.add_argument("FILE", nargs=1)
parser.add_argument("-o", dest="output", default="dem.obj")
options = parser.parse_args()

def read_vertexes(input):
    result = []
    for line in input:
        if line.strip() == "$EndNodes":
            return np.array(result)
        numbers = map(lambda(x): float(x), line.strip().split(" "))
        if len(numbers) == 4:
            result.append(numbers[1:3])

def read_faces(input):
    result = []
    for line in input:
        if line.strip() == "$EndElements":
            return np.array(result, dtype='i4')
        numbers = map(lambda(x): int(x), line.strip().split(" "))
        if len(numbers) > 1:
            if numbers[1] == 2:
                n_ids = numbers[2]
                result.append(numbers[2+n_ids+1:])

def read_mesh(input):
    vertexes = []
    faces = []
    for line in input:
        if line.strip() == "$Nodes":
            vertexes = read_vertexes(input)
        elif line.strip() == "$Elements":
            faces = read_faces(input)
        else:
            continue

    return vertexes, faces

input = open(options.FILE[0])
v,f = read_mesh(input)
input.close()

output = open(options.output, mode="w")

for vertex in v:
    vertex[1] *= -1                               # flip the y sign
    output.write("v %f 0.0 %f\n" % tuple(vertex)) # flip y and z

for face in f:
    a, b, c = face
    output.write("f %d %d %d\n" % (a, c, b)) # flip node order

output.close()


