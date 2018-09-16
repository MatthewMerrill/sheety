from shutil import copyfile
from os import listdir, makedirs
import numpy as np
from subprocess import call

durs = [ 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
pits = [ 2, 1, 0, 1, 2, 2, 2, 1, 1, 1, 2, 3, 3, 2, 1, 0, 1, 2, 2, 2, 2, 1, 1, 2, 1, 0]

for f in listdir('training/declassified/'):
    dig = int(f[int(f.find('.'))+1:-4])
    dig = durs[dig % 26]
    makedirs('training/declassified_data/durations/%d' % dig, exist_ok=True)
    copyfile('training/declassified/%s' % f,
            'training/declassified_data/durations/%d/%s' % (dig, f))

for f in listdir('training/declassified/'):
    dig = int(f[int(f.find('.'))+1:-4])
    dig = pits[dig % 26]
    makedirs('training/declassified_data/pitches/%d' % dig, exist_ok=True)
    copyfile('training/declassified/%s' % f,
            'training/declassified_data/pitches/%d/%s' % (dig, f))
"""
for f in listdir('training/mattchunks/'):
    dig = int(f[5:-4]) % 12
    makedirs('training/chunky/pitches/%d' % dig, exist_ok=True)
    copyfile('training/mattchunks/%s' % f,
            'training/chunky/pitches/%d/%s' % (dig, f))
"""
