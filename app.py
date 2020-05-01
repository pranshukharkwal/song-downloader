from flask import Flask, render_template, flash, redirect, url_for, session, request, logging , send_file
from flask_mysqldb import MySQL
from functools import wraps
import requests
from bs4 import BeautifulSoup
from pytube import YouTube
import urllib.parse
import os
import time
import atexit
from apscheduler.schedulers.background import BackgroundScheduler

def clear():
    print("Clear running")
    for i in os.listdir():
        if os.path.splitext(i)[1] == '.mp3' or os.path.splitext(i)[1] == '.mp4':
            os.remove(i)

scheduler = BackgroundScheduler()
scheduler.add_job(func=clear,trigger="interval",hours = 1)
atexit.register(lambda: scheduler.shutdown())
scheduler.start()

app = Flask(__name__)
app.secret_key='secret123'

data = dict()

def downloader(query):
    q_encode = urllib.parse.quote(query)
    URL = "https://www.youtube.com/results?search_query=" + q_encode
    r = requests.get(URL)
    soup = BeautifulSoup(r.content , 'html5lib')

    for video in soup.findAll('div' , attrs={'class' : 'yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix'}):
        if video.find('span' , attrs={'class' : 'yt-badge yt-badge-live'}):
            continue
        else:
            yid = video.get('data-context-item-id')
            link = 'https://youtube.com/watch?v=' + yid
            yt = YouTube(link)
            if yt.length <= 900:
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download()
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                data['url'] = video.default_filename[:-4] + '.mp3'
                data['title'] = video.default_filename[:-4]
                data['image'] = yt.thumbnail_url
                data['rating'] = yt.rating
                data['length'] = yt.length

                try:
                    os.rename(out_file, new_file)
                except:
                    pass
                return data
                break
            else:
                continue


@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        data = downloader(query)
        return render_template('home.html' , data = data)
    else:
        return render_template('home.html')

@app.route('/api/getdata', methods=['POST'])
def rest_api():
    data = request.get_json();
    result = downloader(data['name'])
    #print(result)
    return result  #Process Done

@app.route('/api/check', methods=['GET'])
def restapi_chech():
    return 'API is Working!'



@app.route('/<path>')
def download_file(path):
    return send_file(path , as_attachment = True)


if __name__ == '__main__':
    app.run(debug = True)
