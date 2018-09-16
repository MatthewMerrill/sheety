import numpy as np
import math
from PIL import Image

def find_lines(line):
    lines = []
    y = 0
    while y < len(line):
        while y < len(line) and not line[y]: y += 1
        start = y
        while y < len(line) and line[y]: y += 1
        end = y
        if end - start == 0:
            break
        #if end - start == 1: continue
        lines.append(end - start)
    return lines

def seems_like_a_note_line(line, mean, stdev):
    lines = find_lines(line)
    if len(lines) == 0:
        return False
    if len(lines) != 5:
        return True
    #import ipdb;ipdb.set_trace()
    lines = np.array(lines)
    mean = int(lines.mean())
    #stdev = int(round(lines.std()))
    if any(abs(l - mean) > 1.5*stdev for l in lines):
        return True
    return False

SACRED_X = 36
SACRED_Y = 104
SACRED_SIZE = (SACRED_X, SACRED_Y)

#i = Image.open('test.png').convert('1', image=Image.NONE)
def split(i):
    def getline(x):
        return [0 if p == 255 else 1 for p in i.crop((x, 0, x+1, i.height)).getdata()]

    def calculate_bu(line):
        y = 0
        while y < i.height and not line[y]: y += 1
        toptop = y
        while y < i.height and line[y]: y += 1
        topbottom = y
        while y < i.height and not line[y]: y += 1
        bottomtop = y
        while y < i.height and line[y]: y += 1
        bottombottom = y
        midtop = (toptop + topbottom) // 2
        midbottom = (bottomtop + bottombottom) // 2
        return midbottom - midtop

    # find 5 lines
    x = 0
    while x < i.width and len(find_lines(getline(x))) < 5:
        x += 1
    first_5 = x
    
    while True:
        #print(x)
        line = getline(x)

        # get top and bottom of staff
        first_bar = line.index(1)
        last_bar = len(line)-1 - line[::-1].index(1)

        # find mean and standard deviation of bar line height
        lines = np.array(find_lines(line))
        mean = math.ceil(lines.mean())
        stdev = math.ceil(lines.std())
        #print(lines, mean, stdev)

        if any(abs(l - mean) > 2*stdev for l in lines):
            break
        x += 1
    
    stdev_sample_location = (first_5 + x) // 2
    lines = np.array(find_lines(getline(stdev_sample_location)))
    mean = math.ceil(lines.mean())
    stdev = math.ceil(lines.std())
    bu = calculate_bu(getline(stdev_sample_location))
    #print(stdev_sample_location, lines, mean, stdev, bu)

    def seems_like_a_note(x):
        return seems_like_a_note_line(getline(x), mean, stdev)

    note_x = []
    x = 0
    while x < i.width:
        while x < i.width and not seems_like_a_note(x):
            x += 1
        start = x
        while x < i.width and seems_like_a_note(x):
            x += 1
        end = x
        if start == end: # like at the end of the line
            break
        else:
            note_x.append((start, end))
    # merge:
    merge_idx = 1
    while merge_idx < len(note_x):
        start = note_x[merge_idx][0]
        if start - note_x[merge_idx-1][1] < bu:
            note_x[merge_idx-1] = (note_x[merge_idx-1][0], end)
            del note_x[merge_idx]
        else:
            merge_idx += 1
    # drop
    note_x = filter(lambda note: note[1] - note[0] < bu//2, note_x)
    chunks = []
    for start, end in note_x:
        center = (start + end) // 2
        #start = int(center - 1.5*bu)
        #end = int(center + 1.5*bu)
        #chunk = i.crop((start, first_bar-bu*2, end, last_bar+bu*2))
        chunk = i.crop((start, 0, end, i.height))
        #chunk = chunk.resize(SACRED_SIZE)
        chunks.append(chunk)
    return chunks

#split(i)
