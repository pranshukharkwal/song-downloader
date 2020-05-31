import pytube3
yt = YouTube('https://youtube.com/watch?v=HFX6AZ5bDDo')
video = yt.streams.filter(only_audio=True).first()
out_file = video.download()
print(out_file)
