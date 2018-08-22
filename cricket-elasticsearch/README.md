### cricket-elasticsearch:
This scripts assumes you have elasticsearch installed and setup.
To check that your elasticsearch server is up and running, use the bash wrapper to turn it on and run the game:
```
sh ES.sh
```

This is the biggest and most complicated thing I've done that isn't under NDA, I like it because it's a single script which is a self-contained network of interlocking functions, which are only able to generate data and outputs they can handle. It simulates the dart game 'Cricket', which was new to me, so I figured it out by watching this video: https://www.youtube.com/watch?v=odKhntmqiHw&t

It runs an elasticsearch server to record names of previous users, and wins and losses. When it first runs it auto-populates the server like an old-school arcade game, displaying a list of 'Top Three Cricket Masters' at the beginning, and then if you rack up the wins you can get on that list too. The server is persistent on your own machine, so you can close the python program and come back to find your old character data still there.
