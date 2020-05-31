
# La Musica - Song Downloader
La musica is a one-click song downloading webapp, built using the Flask framework, on the top of Python's Pytube Library. 
The application provides fast and accurate results, is free from ads, and literally takes just one click. 
Android variant of the webapp can be found here - [Musin](https://github.com/Signior-X/musin)

## How to run the project on local machine?
To run the project on your local machine, you need to have Python installed on your machine, and should also have "Pip" which is python's package manager.

Follow these steps to run the project on your local machine.

 - Clone the repositary, or download it as zip and extract it. 
 - Open your terminal and write 
 
`pip install -r requirements.txt`
- Navigate to the directory where you have downloaded the repositary with the command

`cd <address-to-the-directory>`
- Now type the command to create the server

`python app.py` 
- Open your browser, and type <localhost:5000> in the url bar, and the website will load
NOTE : The port may differ on your device, when you run app.py, you will see which port is alloted to the app, so now open the website in that port. 

## Contribution guide
Want to contribute to the project? Here is how you can help us improve the application, and add more features. 
You can contribute to the project,
1) By finding bugs, and telling us about them, and then you may even fix those bugs. 
2) By thinking of new features which can be added to the app(and telling us), and even working on those new features. 

If you have any such bug/feature you would like us to know about, all you need to do, is [raise an issue](https://github.com/pranshukharkwal/song-downloader/issues). After that, we can discuss more about the issue, and then maybe you can work on solving it. 

### How to solve issues?
Follow these steps, to start working on any issue of your choice. It is recommened to inform in the comments, before working on any issue, so that multiple people do not work on the same issue. 

 - Fork the repositary : [https://github.com/pranshukharkwal/song-downloader](https://github.com/pranshukharkwal/song-downloader)
 - Open the terminal/git bash, and clone the repositary by typing 

`git clone https://github.com/pranshukharkwal/song-downloader`
 - Create a new branch (preferably with the name of the bug/feature you want to add) and move to the branch by typing

`git branch <bug/feature name>`

`git checkout <big/feature name>`
 - Now make changes to the code
 - Add the files, and commit the changes by typing

`git add -A`

`git commit -m "Commit message here"` (Please write a meaning commit message)
 - Add more features if you want to, then add and commit them in the same way.
 - Once you are done, push the changes to branch with the command

 `git push -u origin <branch-name>`
 - Open the repositary in Github, and create  a Pull Request

## Important functions

There are the two main functions, which handle two types of downloading queries.

 - downloader(name) -> This takes name as parameter and search on youtube
   and download the songs available
 - download_by_url(url) -> This takes the Youtube URL as the input and
   gives the data of video and the download link

## API Documentation
If you are a developer, and you use some other language other than Python, you might not be able to use the Pytube library. We have created an API for this project, so that you can download the files using our server, no matter in which language you code in.

BASE URL : http://la-musica.herokuapp.com/api/ + methods

There are three kinds of methods which you can use. Let's see how to use them. 

### Method to check if the API is working or not
 - Method - check
 - Type - GET
 - URL - http://la-musica.herokuapp.com/api/check
 - Response - "API is working!" on successful calls
 
### Method to get song links using queries/song-name
 - Method - getdata
 - Type - POST
 - URL - http://la-musica.herokuapp.com/api/getdata
 - Send query data in JSON format

> `{"name":"Song Name"}`
 - Response - (For sucessful calls)

> `data = { 
> "url" : "Link to download/stream the song", 
> "image" : "Link to the thumbnail",
> 	"title" : "Title of the song",
>  "length" : "Song length in seconds",
>  "rating" : "Song ratings" 
>  }`
 
 ### Method to get song download links using Youtube link
 - Method - getytlink
 - Type - POST
 - URL - http://la-musica.herokuapp.com/api/getytlink
 - Send query data in JSON format
> `{"ytlink":"Song Link"}`
 - Response - (For sucessful calls)
> `data = { 
> "url" : "Link to download/stream the song", 
> "vid_url" : "The video url for downloading it",
> "image" : "Link to the thumbnail",
> 	"title" : "Title of the song",
>  "length" : "Song length in seconds",
>  "rating" : "Song ratings" 
>  }`
								

If you create something using the API created above, do let us know and we would happy to list it here. 
    

        
