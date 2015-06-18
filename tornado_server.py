import logging
import signal
import base64

import cv2

import tornado.web
import tornado.websocket
from tornado.ioloop import PeriodicCallback, IOLoop

import settings

cap = cv2.VideoCapture(0)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/ws", SocketHandler),
        ]
        tornado.web.Application.__init__(self, handlers)


class SocketHandler(tornado.websocket.WebSocketHandler):
    writer = None

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def fetch_data(self):
        """
        Sends data to the client.
        """
        global cap
        success, frame = cap.read()

        if not success:
            print 'No success reading'
            return

        # 1280 720
        frame = frame[0:720, 175:1105]
        
        cnt = cv2.imencode('.png', frame)[1]
        b64 = base64.encodestring(cnt)
        image_el = "<img src='data:image/png;base64,"+b64 +"'>"

        try:
            self.write_message(image_el)
        except Exception as err:
            logging.error("Error sending message: {}".format(err), exc_info=True)
            logging.info('Closing writer')
            self.writer.stop()
            self.close()
        

    def open(self):
        # set the interval depending on the frames per second set in settings
        interval = 1000 / settings.FRAMES_PER_SECOND
        self.writer = PeriodicCallback(self.fetch_data, interval)
        self.writer.start()

    def data_received(self, chunk):
        pass

    def on_message(self, message):
        if message == 'close':
            logging.info('Closing connection')
            self.writer.stop()
            self.close()


def on_shutdown():
    global cap
    print('Shutting down')
    cap.release()
    tornado.ioloop.IOLoop.instance().stop()


if __name__ == '__main__':
    app = Application()
    app.listen('8888')
    io_loop = IOLoop.current()
    signal.signal(signal.SIGINT, lambda sig, frame: io_loop.add_callback_from_signal(on_shutdown))
    io_loop.start()
