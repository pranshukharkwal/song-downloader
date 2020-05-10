# song-downloader

# Functions
Fucnitons which help in downloading (Max length of songs is 15 minutes)
downloader() -> This takes name as parameter and search on youtube and download the songs available
download_by_url() -> This takes the Youtube URL as the input and gives the data of video and music url to download

# REST APIs
Added Rest APIs which gives the data of the songs

/api/getdata (POST)
-> This api takes the song name 'name' in the request body
-> Response
        If successful:
            data = {
                "url" : "The song url",
                "image" : "Thumbnail url of the song",
                "title" : "The title of the song",
                "length" : "The length in seconds of the Video",
                "rating" : "The song ratings on Youtube"
            }
    
/api/getytlink (POST)
-> This takes the youtube link 'ytlink' in the request body
-> Response 
        If successful:
            data = {
                "url" : "The song url",
                "vid_url" : "The video url for downloading it"
                "image" : "Thumbnail url of the song",
                "title" : "The title of the song",
                "length" : "The length in seconds of the Video",
                "rating" : "The song ratings on Youtube"
            }
        If unsuccessful
            data = {
                "error" : "Error Message"
                "length" : "if length error has come"  (Only in case of length >= 15 minutes)
            }
    
/api/check (GET)
-> This is just to check if the APIs are working or not
-> gives message 'API is working1' if successful
        
