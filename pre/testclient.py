import time
import glob
from datetime import timedelta

from tornado.escape import json_encode
from tornado import ioloop
from tornado import gen
from tornado.websocket import websocket_connect

from rx.concurrency import HistoricalScheduler

from gpx import GpxFile


scheduler = HistoricalScheduler()
running = True


class WSClient:
    def __init__(self, user):
        self.user = user

    def on_message(self, msg):
        global running
        print("on_message", msg)
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


def main():
    global running
    start = None

    def action(scheduler, state):
        ws, point = state

        ws.write({"lat": point.latitude, "lng": point.longitude, "alt": point.altitude, "name": point.name})

    print("Parsing GPS files")
    for filename in glob.glob("data/*.gpx"):
        print(filename)
        username = filename.split("/")[1].split(".")[0]
        ws = WSClient(username)
        ioloop.IOLoop.current().run_sync(ws.connect)

        gpx = GpxFile(filename)

        for point in gpx:
            if not start or start.time > point.time:
                start = point

            point.name = username
            scheduler.schedule_absolute(point.time, action, state=(ws, point))

    print("Starting at: ", start.time, start)
    scheduler.advance_to(start.time)

    while running:
        time.sleep(0.1)
        scheduler.advance_by(timedelta(seconds=20))


if __name__ == '__main__':
    main()
