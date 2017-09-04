import os
from datetime import datetime

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler, StaticFileHandler, Application, url
from tornado.httputil import url_concat
from tornado.escape import json_decode, json_encode
from tornado import ioloop

from rx import Observer, Observable
from rx.subjects import Subject
from rx.concurrency import IOLoopScheduler

scheduler = IOLoopScheduler()

activities = {}  # type: Dict[str, Activity]
API_KEY = ""


class Activity(Observer):
    def __init__(self, name):
        self._stream = Subject()
        self._name = name

        self.clients = []

    def on_next(self, msg):
        self._stream.on_next(msg)

    def on_error(self, ex):
        self._stream.on_error(ex)

    def on_completed(self):
        self._stream.on_completed()

    @property
    def stream(self):
        # A simple identity analysis
        return self._stream.select(lambda x: x)


class WSHandler(WebSocketHandler):
    def __init__(self, *args):
        super().__init__(*args)

        self._subscription = None

    def open(self, user):
        print("WebSocket opened by: ", user)

        activity = activities.get(user)
        if not activity:
            activity = Activity(user)
            activities[user] = activity

        def on_error(ex):
            print(ex)

        self._subscription = activity.stream.select(json_encode).subscribe(self.write_message, on_error)

    def on_message(self, data):
        msg = json_decode(data)

        # Notify all activities
        for activity in activities.values():
            activity.on_next(msg)

    def on_close(self):
        print("WebSocket closed")

        self._subscription.dispose()


class MainHandler(RequestHandler):
    def get(self, user="anonymous"):
        self.render("index.html", api_key=API_KEY)


def main():
    if API_KEY == "":
        print("You need a Google maps API key: https://developers.google.com/maps/documentation/javascript/get-api-key")
        return

    port = os.environ.get("PORT", 8080)
    app = Application([
        url(r"/", MainHandler),
        (r"/users/(.*)", MainHandler),
        (r'/static/(.*)', StaticFileHandler, {'path': "."}),
        (r'/ws/(.*)', WSHandler)
    ])

    print("Starting server at port: %s" % port)
    app.listen(port)
    ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()