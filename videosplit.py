from os import listdir
from asdf3 import split
from PIL import Image
from sys import argv

def split_frames(filesbase, note_count=None):
    threshold = 185
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
            if note_count is not None and len(chunks) != note_count:
                failed += 1
                print('we goofed boiz')
                print(note_count, len(chunks))
            else:
                for j, (pos, chunk) in enumerate(chunks):
                    chunk.save(('%s_out/%d_%s' % (filebase, len(chunks), filename)).replace('.png', '_split_%03d.png' % j))
                passed += 1
    finally:
        print('Passed: %d/%d (%.2f%%)' % (passed, passed+failed, passed/(passed+failed)))

if __name__ == '__main__':
    filebase = argv[1] if len(argv) > 1 else 'training/split'
    split_frames(filebase, note_count=26))


