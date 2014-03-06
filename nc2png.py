#!/usr/bin/env python

from PIL import Image
import numpy as np
import netCDF4 as NC
import pylab as plt

from argparse import ArgumentParser
parser = ArgumentParser()
parser.description = ""
parser.add_argument("FILE", nargs=1)
parser.add_argument("-o", dest="output", default="dem.png")
parser.add_argument("-t", dest="texture", action="store_true", help="create a texture instead of a DEM")
parser.add_argument("-f", dest="flip", action="store_true", help="flip up/down")
parser.add_argument("-l", dest="log", action="store_true", help="use log scale")
parser.add_argument("--clip_max", dest="clip_max", default=None, type=float)
parser.add_argument("--clip_min", dest="clip_min", default=None, type=float)
parser.add_argument("-v", dest="variable", default="usurf")
parser.add_argument("-m", dest="mask", default=None, type=int)
options = parser.parse_args()

nc = NC.Dataset(options.FILE[0])

data = np.ma.array(nc.variables[options.variable][:], dtype=np.float32).filled(0)
data = np.squeeze(data)

if options.flip:
    data = np.flipud(data)

if options.clip_max is not None:
    data = np.minimum(data, options.clip_max)

if options.clip_min is not None:
    data = np.maximum(data, options.clip_min)

if options.mask:
    data = np.array(data == options.mask, dtype=np.float32)

def normalize(data):
    data_min = data.min()
    data_max = data.max()
    return (data - data_min) / float(data_max - data_min)

def array_to_16bit_grayscale(data):
    data_normalized = normalize(data)
    return Image.fromarray(data_normalized * (256**2 - 1)).convert("I")

def array_to_image(data, cmap, log10=False):
    if log10:
        eps = 1
        data_min = data.min()
        data_normalized = normalize(np.log10(data - data_min + eps))
    else:        
        data_normalized = normalize(data)
    return Image.fromarray(cmap(data_normalized, bytes=True))

if options.texture:
    array_to_image(data, plt.cm.Spectral, log10=options.log).save(options.output)
else:
    array_to_16bit_grayscale(data).save(options.output)

