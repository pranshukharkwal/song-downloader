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

# For the youtube apis
from googleapiclient.discovery import build

api_key = "AIzaSyC7afHlX2KCUytDiW2uJC71L3TuHtbz3Bw"
# End of the youtube apis

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
app.config['MYSQL_HOST'] = 'remotemysql.com'
app.config['MYSQL_USER'] = 'JJFKCXD3CC'
app.config['MYSQL_PASSWORD'] = 'us8bg5jdXp'
app.config['MYSQL_DB'] = 'JJFKCXD3CC'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

data = dict()

def download_by_url(yturl):

    data = {}

    try:
        yt = YouTube(yturl)
        cur = mysql.connection.cursor()
        if cur.execute("select * from songs where song = %s" , (yt.title,)) > 0:
            cur.execute("update songs set count = count + 1 where song = %s;" , (yt.title,))
        else:
            cur.execute("insert into songs(song) values(%s)",(yt.title,))
        mysql.connection.commit()
        cur.close()
    except:
        data['error'] = "Invalid Youtube Url!"
        return data

    if yt.length <= 900:

        vid_url = yt.streams.filter()[0].url
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download()
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'

        data['url'] = 'https://la-musica.herokuapp.com/'+video.default_filename[:-4] + '.mp3'
        data['vid_url'] = vid_url
        data['title'] = video.default_filename[:-4]
        data['image'] = yt.thumbnail_url
        data['rating'] = yt.rating
        data['length'] = yt.length

        try:
            os.rename(out_file, new_file)
        except:
            pass

    else:
        data['error'] = "Length exceeds 900 seconds"
        data['length'] = yt.length
    return data


def downloader(query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    print(type(youtube))

    req = youtube.search().list(part="snippet", q=query, type="video")

    print(type(req))

    res = req.execute()

    y_items = res['items'] # This is a list of dictionaries

    # Now try for all the results
    for row in y_items:
    # print(res['items'][0]['id']['videoId']) # This gives the videoId
        sharedVideoUrl = 'https://youtu.be/' + row['id']['videoId']
        print("sharedVideoUrl ", sharedVideoUrl)

        data = download_by_url(sharedVideoUrl) # The url, it is giving is correct

        if 'error' in data:
            continue

        # print(data)
        return data
    return data

    # URL = "https://www.youtube.com/results?search_query=" + q_encode
    # r = requests.get(URL)
    # soup = BeautifulSoup(r.content , 'html5lib')

    # for video in soup.findAll('div' , attrs={'class' : 'yt-lockup yt-lockup-tile yt-lockup-video vve-check clearfix'}):
    #     if video.find('span' , attrs={'class' : 'yt-badge yt-badge-live'}):
    #         continue
    #     else:
    #         yid = video.get('data-context-item-id')
    #         link = 'https://youtube.com/watch?v=' + yid
    #         print(link)
    #         yt = YouTube(link)
    #         cur = mysql.connection.cursor()
    #         if cur.execute("select * from songs where song = %s" , (yt.title,)) > 0:
    #             cur.execute("update songs set count = count + 1 where song = %s;" , (yt.title,))
    #         else:
    #             cur.execute("insert into songs(song) values(%s)",(yt.title,))
    #         mysql.connection.commit()
    #         cur.close()

    #         if yt.length <= 900:

    #             vid_url = yt.streams.filter(only_audio=True)[0].url
    #             video = yt.streams.filter(only_audio=True).first()
    #             out_file = video.download()
    #             base, ext = os.path.splitext(out_file)
    #             new_file = base + '.mp3'

    #             data['url'] = video.default_filename[:-4] + '.mp3'
    #             data['vid_url'] = vid_url
    #             data['title'] = video.default_filename[:-4]
    #             data['image'] = yt.thumbnail_url
    #             data['rating'] = yt.rating
    #             data['length'] = yt.length

    #             try:
    #                 os.rename(out_file, new_file)
    #             except:
    #                 pass
    #             return data
    #             break
    #         else:
    #             continue

@app.route('/' , methods=['GET' , 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        data = downloader(query)
        # return 'checking'
        return render_template('home.html' , data = data)
    else:
        return render_template('home.html')

@app.route('/api/getdata', methods=['POST'])
def rest_api():
    data = request.get_json();
    result = downloader(data['name'])
    result['url']='https://la-musica.herokuapp.com/'+result['url']
    #print(result)
    return result  #Process Done

@app.route('/api/getytlink', methods=['POST'])
def test_api2():
    data = request.get_json();
    result = download_by_url(data['yturl'])
    #print(result)
    return result # Take care of error also

@app.route('/api/getdownloads', methods=['GET'])
def rest_api3():
    cur = mysql.connection.cursor()
    songslst = []
    cur.execute("SELECT * from songs")
    for x in cur.fetchall():
        songslst.append(x)

    #print(songslst)

    data = { "list": songslst }
    #songslst is the list of song names in String
    return data

@app.route('/api/check', methods=['GET'])
def restapi_chech():
    return 'API is Working!'

@app.route('/<path>')
def download_file(path):
    return send_file(path , as_attachment = True)


if __name__ == '__main__':
    app.run(debug = True)
