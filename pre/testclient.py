import os
import time
import glob
from datetime import timedelta, datetime

from tornado.escape import json_encode
from tornado import ioloop
from tornado import gen
from tornado.websocket import websocket_connect

from rx.concurrency import HistoricalScheduler

from point import Point


scheduler = HistoricalScheduler(initial_clock=datetime.fromtimestamp(86400))
running = True


class WSClient:
    def __init__(self, user):
        self.user = user

    def on_message(self, msg):
        global running
        #print("on_message", msg)
        if msg is None:
            running = False

    def write(self, msg):
        data = json_encode(msg)
        self.conn.write_message(data)

    @gen.coroutine
    def connect(self):
        url = "ws://localhost:8080/ws/%s" % self.user
        print("Connecting to: ", url)
        self.conn = yield websocket_connect(url, on_message_callback=self.on_message)


    def close(self):
        self.conn.close()


@gen.coroutine
def main():
    global running
    start = None

    def action(scheduler, state):
        ws, point = state

        ws.write({"lat": point.lat, "lng": point.lng, "time": point.time.isoformat(), "alt": point.alt, "user": point.user})

    wss = []

    print("Parsing GPS files")
    for filename in glob.glob(os.path.join("data", "*.gpx")):
        username = filename.split(os.sep)[1].split(".")[0]
        ws = WSClient(username)
        wss.append(ws)  # Connect later

        points = Point.from_gpxfile(filename)

        for point in points:
            if not start or start.time > point.time:
                start = point

            point.user = username
            scheduler.schedule_absolute(point.time, action, state=(ws, point))

    print("Starting at: ", start.time, start)

    # Connect all clients after server set to virtual time
    for ws in wss:
        yield ws.connect()

    scheduler.advance_to(start.time)
    while running:
        yield gen.sleep(0.1)
        scheduler.advance_by(timedelta(seconds=20))

        ws.write({"time": scheduler.now.isoformat()})

        if not scheduler.queue.peek():
            break


if __name__ == '__main__':
    ioloop.IOLoop.current().run_sync(main)
