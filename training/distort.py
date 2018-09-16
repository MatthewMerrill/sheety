from shutil import copyfile
from os import listdir, makedirs
import numpy as np
from subprocess import call
from sys import argv

durs = [ 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
pits = [ 2, 1, 0, 1, 2, 2, 2, 1, 1, 1, 2, 3, 3, 2, 1, 0, 1, 2, 2, 2, 2, 1, 1, 2, 1, 0]

filebase = argv[1] if len(argv) > 1 else 'training/split_out'

for f in listdir(filebase):
    dig = int(f[int(f.find('t'))+1:-4])
    dig = durs[dig % 26]
    makedirs('%s_data/durations/%d' % (filebase, dig), exist_ok=True)
    copyfile('%s/%s' % (filebase, f),
            '%s_data/durations/%d/%s' % (filebase, dig, f))

for f in listdir(filebase):
    dig = int(f[int(f.find('t'))+1:-4])
    dig = pits[dig % 26]
    makedirs('%s_data/pitches/%d' % (filebase, dig), exist_ok=True)
    copyfile('%s/%s' % (filebase, f),
            '%s_data/pitches/%d/%s' % (filebase, dig, f))
"""
for f in listdir('training/mattchunks/'):
    dig = int(f[5:-4]) % 12
    makedirs('training/chunky/pitches/%d' % dig, exist_ok=True)
    copyfile('training/mattchunks/%s' % f,
            'training/chunky/pitches/%d/%s' % (dig, f))
"""
