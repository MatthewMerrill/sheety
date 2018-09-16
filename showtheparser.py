from PIL import Image
import json

from asdf3 import split

import training.durations as durations
import training.pitches as pitches

from os import environ, remove, makedirs, listdir

threshold = 185


def predict_duration(chunk):
    chunk.save('tmp.png')
    with open('tmp.png', 'rb') as ff:
        content = ff.read()
    return durations.get_prediction(content, environ['GCP_PROJECT'], environ['GCP_DURATION_MODEL'])


def predict_pitches(chunk):
    chunk.save('tmp.png')
    with open('tmp.png', 'rb') as ff:
        content = ff.read()
    return pitches.get_prediction(content, environ['GCP_PROJECT'], environ['GCP_PITCH_MODEL'])

pitch_mapping = {
        "a_0": 'C',
        "a_1": 'D',
        "a_2": 'E',
        "a_3": 'G',
}
duration_mapping = {
        "a_0": 'Quarter',
        "a_1": 'Half',
        "a_2": 'Full',
}

if __name__ == '__main__':
    filepath = 'webappupload/frames/theframe.png'
    print('splitting:', filepath)
    i = Image.open(filepath)
    i = i.convert('L').point(lambda p: 0 if p < threshold else 255, '1')
    i.save(filepath.replace('.png', '.bw.png'))
    chunks = split(i)

    print("Split into %d notes!" % len(chunks))

    for i in range(len(chunks[0])):
        try:
            chunks[i][1].save('webappupload/frames_out/frame%d.png' % i)
        except Exception as e:
            print(e)

    notes = []
    idx = 0
    for tup in chunks:
        idx += 1
        print("Predicting duration/pitch: %02d/%02d...        " % (idx, len(chunks)), end='')
        notes.append({
            "rect": tup[0], 
            "duration": predict_duration(tup[1]).payload[0].display_name,
            "pitch": predict_pitches(tup[1]).payload[0].display_name,
        })
        print("dur: %10s    pit: %10s" % (duration_mapping[notes[-1]['duration']], pitch_mapping[notes[-1]['pitch']]))

    import sys;print(json.dumps(notes), file=sys.stderr)

