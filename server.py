from flask import Flask, Response, request
import requests

app = Flask(__name__)

@app.route('/')
def Index():
    return 'memes'



