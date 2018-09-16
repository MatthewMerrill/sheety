from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
import requests
from asdf3 import split

from PIL import Image
import json

import training.durations as durations
import training.pitches as pitches

from subprocess import call
from os import environ, remove, makedirs, listdir
from shutil import rmtree


app = Flask(__name__)
CORS(app)


threshold = 185

@app.route('/')
def Index():
    return 'memes'


def Reset():
    #remove('webappupload.webm')
    #remove('webappupload.mp4')
    try:
        rmtree('webappupload/')
    except:
        pass


@app.route("/video", methods=['POST'])
def Video():
    Reset()
    #with open('webappupload.webm', 'wb') as upload:
    #    upload.write(request.files['video'])
    threshold = int(request.form['threshold'])
    request.files['video'].save('webappupload.webm')
    makedirs('webappupload/frames')
    makedirs('webappupload/frames_out')

    call(['ffmpeg', '-f', 'webm', '-y', '-i', 'webappupload.webm', '-filter:v', 'crop=in_w:in_h/2:0:0', 'webappupload.mp4'])
    call(['ffmpeg', '-r', '15', '-y', '-i', 'webappupload.mp4', 'webappupload/frames/video_%04d.png'])

    filebase = 'webappupload/frames'
    rects_by_count = {}
    framecount = 100
    for filename in listdir(filebase):
        if framecount <= 0:
            break
        framecount -= 1
        if filename.find('bw') != -1:
            continue
        filepath = '%s/%s' % (filebase, filename)
        print('splitting:', filename)
        i = Image.open(filepath)
        i = i.convert('L').point(lambda p: 0 if p < threshold else 255, '1')
        i.save(filepath.replace('.png', '.bw.png'))
        chunks = split(i)
        rects_by_count.setdefault(len(chunks), []).append(chunks)

    mode = []
    mode_key = -1
    mode_count = -1
    for key, value in rects_by_count.items():
        if key is 26 and len(value) > mode_count:
            mode = value
            mode_key = key
            mode_count = len(value)
        #print(key, value)
    print(mode)

    notes = []
    for tup in mode[0]:
        notes.append({
            "rect": tup[0], 
            "duration": predict_duration(tup[1]).payload[0].display_name,
            "pitch": predict_pitches(tup[1]).payload[0].display_name,
        })

    try:
        for i in range(len(mode[0])):
            chunk.save('webappupload/frames_out/frame%d.png' % i)
    except:
        pass

    print(notes)
    return notes

    
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



