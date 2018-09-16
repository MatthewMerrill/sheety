from flask import Flask, Response, request
import requests
from asdf3 import split

from subprocess import call
from os import remove, makedirs
from shutil import rmtree


app = Flask(__name__)


@app.route('/')
def Index():
    return 'memes'


def Reset():
    remove('webappupload.webm')
    rmtree('webappupload/')


@app.route("/video")
def Video():
    with open('webappupload.webm', 'w') as upload:
        upload.write(request.data)
    makedirs('webappupload/frames')
    makedirs('webappupload/frames_out')

    call(['ffmpeg', '-y', '-i', 'webappupload.webm', '"webappupload/frames/video_%04d.png"'])
    
    filebase = 'webappupload/frames'
    for filename in listdir(filebase):
        if filename.find('bw') != -1:
            continue
        filepath = '%s/%s' % (filebase, filename)
        print('splitting:', filename)
        i = Image.open(filepath)
        i = i.convert('L').point(lambda p: 0 if p < threshold else 255, '1')
        i.save(filepath.replace('.png', '.bw.png'))
        chunks = split(i)


    videosplit.split_frames('webappupload/frames')
    

