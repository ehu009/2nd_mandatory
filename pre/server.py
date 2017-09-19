import os
import time
from dateutil.parser import parse as parsedate
from datetime import timedelta

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler, StaticFileHandler, Application, url
from tornado.escape import json_decode, json_encode
from tornado import ioloop

from rx import Observer
from rx.subjects import Subject
from rx.concurrency import IOLoopScheduler

from point import Point


destination = Point(-25.3825800, 16.4237190)

virtual_clock = parsedate("2017-05-01 05:00:00").timestamp()


def clock():
    return virtual_clock or time.time()


loop = ioloop.IOLoop(time_func=clock)
scheduler = IOLoopScheduler(loop)

activities = {}  # type: Dict[str, Activity]
API_KEY = ""


class Activity(Observer):
    def __init__(self, user):
        self._stream = Subject()
        self._user = user

    def on_next(self, msg):
        self._stream.on_next(msg)

    def on_error(self, ex):
        self._stream.on_error(ex)

    def on_completed(self):
        self._stream.on_completed()

    def distance_calc(self, point):
        return point.distance(destination)

    def combine_with_distance(self, me, dist_to_goal):
        me.dist_to_goal = dist_to_goal
        return me

    @property
    def stream(self):
        # A simple identity analysis
        me = self._stream.filter(lambda x: x.user == self._user)
        others = self._stream.filter(lambda x: x.user != self._user)

        distance = me.select(self.distance_calc).start_with(0)
        # distance.sample(timedelta(seconds=2000), scheduler=scheduler).subscribe(lambda x: print("Distance %d km" % (x / 1000)))

        # speed = me.buffer_with_count(2, 1).start_with(0).subscribe(print)
        # speed = me.window_with_count(2, 1).select_many(lambda x: x.to_iterable().)
        # speed = me.pairwise().start_with(0)

        me_with_distance = me.with_latest_from(distance, self.combine_with_distance)
        return me_with_distance.merge(others)


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

        self._subscription = activity.stream.select(lambda x: x.to_json()).subscribe(self.write_message, on_error)

    def on_message(self, data):
        global virtual_clock
        msg = Point.from_json(data)
        #print(msg)

        virtual_clock = msg.time.timestamp()

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

    try:
        ioloop.IOLoop.current().start()
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()
