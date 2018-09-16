from os import listdir
from asdf3 import split
from PIL import Image
from sys import argv

threshold = 185

filebase = argv[1] if len(argv) > 1 else 'training/split'
failed = 0
passed = 0

try:
    for filename in listdir(filebase):
        if filename.find('bw') != -1:
            continue
        filepath = '%s/%s' % (filebase, filename)
        print('splitting:', filename)
        i = Image.open(filepath)
        i = i.convert('L').point(lambda p: 0 if p < threshold else 255, '1')
        i.save(filepath.replace('.png', '.bw.png'))
        chunks = split(i)
        if len(chunks) != 26:
            failed += 1
            print('we fucked boiz')
            print(len(chunks))
        else:
            for j, chunk in enumerate(chunks):
                chunk.save(('%s_out/%s' % (filebase, filename)).replace('.png', '.split%03d.png' % j))
            passed += 1
finally:
    print('Passed: %d/%d (%.2f%%)' % (passed, passed+failed, passed/(passed+failed)))

