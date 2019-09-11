# ExLog
It is a reading web application. 
You can sign up/ sign in like you do in a regular web-app. 
It shows you the latest, trending articles based on your choice of interest. 
You can serach for a particular type of article by choosing the interest.
Update your profile picture, update your interest and read the best articles.
Note: make sure you're running Ex-Log over https
Usage
Download all the files to your computer
In your command shell cd to the directory where requirements.txt is located
run: pip install -r requirements.txt
Then install the dependencies in the local node_modules folder
inside package.json directory run: npm install
Then You have to run three servers: scrapserver, linkpreview, flask server
/scrapserver/node index.js
/linkpreview/node index.js
flask run
