# Security cam

- Tornado server sending base64 encoded frames, captured using OpenCV, over a
websoket to connected clients.
- Flask web app serving some html with JavaScript which connects through the
websocket to the Tornado server and renders the images.

## Setup

- You'll need Python 2 and OpenCV installed globally.
- Install python requirements: `pip install -r requirements.txt`
- If you're using virtualenv, copy the relevant OpenCV files to the virtualenv libs path:

```
cp /usr/local/lib/python2.7/site-packages/cv* env/lib/python2.7/site-packages
```

- Run the tornado server: `python tornado_server.py`
- Run the flask server: `python flask_server.py`

Go to `http://0.0.0.0:5000/` and you might see yourself if you have a webcam.

## Settings

You can set the amount of frames per second you want to have in your streaming. Because
at the moment each frame is sent over websocket, I wouldn't suggest setting it higher
than 10, otherwise you'll get some serious delay.