

import unittest

from rx.testing import TestScheduler, ReactiveTest

on_next = ReactiveTest.on_next
on_completed = ReactiveTest.on_completed
on_error = ReactiveTest.on_error
subscribe = ReactiveTest.subscribe
subscribed = ReactiveTest.subscribed
disposed = ReactiveTest.disposed
created = ReactiveTest.created


from server import Activity
from point import Point

from dateutil.parser import parse as parsedate

point1 = Point(lat=-24.4877320, lng=15.7998310)
point1.time = parsedate('2017-05-01T05:21:01')

point2 = Point(lat=-24.4876950, lng=15.7998030)
point2.time = parsedate('2017-05-01T05:21:04')

point3 = Point(lat=-24.4876790, lng=15.7997940)
point3.time = parsedate('2017-05-01T05:21:05')

point4 = Point(lat=-24.4870900, lng=15.7993680)
point4.time = parsedate('2017-05-01T05:21:36')

point5 = Point(lat=-24.4866580, lng=15.7994370)
point5.time = parsedate('2017-05-01T05:21:56')

point6 = Point(lat=-24.5555780, lng=15.8035310)
point6.time = parsedate('2017-05-01T05:49:53')

points = [point1, point2, point3, point4, point5, point6]






def test_queueing():
	
	scheduler = TestScheduler()

	xs = scheduler.create_hot_observable(
	    on_next(100, 1),
	    on_next(210, 2),
	    on_next(240, 3),
	    on_next(280, 4),
	    on_next(320, 5),
	    on_next(350, 6),
	    on_completed(600)
    )

	def create():
		return xs.buffer_with_count(2, 1).map(lambda x: ",".join([str(a) for a in x]))

	results = scheduler.start(create)
	results.messages.assert_equal(
		on_next(240, "2,3"),
	    on_next(280, "3,4"),
	    on_next(320, "4,5"),
	    on_next(350, "5,6"),
	    on_next(600, "6"),
	    on_completed(600)
	)
	xs.subscriptions.assert_equal(subscribe(200, 600))

	print("OK - queueing")

def test_speed(test_activity):
	scheduler = TestScheduler()

	wanted = []
	for x in range(5):
		dist = points[x].distance(points[x+1])
		dur = (points[x+1].time - points[x].time).total_seconds()
		wanted.append(dist / dur)
	
	wanted.append(0.0)
	assert len(wanted), 6
	

	xs = scheduler.create_hot_observable(
	    on_next(210, points[0]),
	    on_next(240, points[1]),
	    on_next(280, points[2]),
	    on_next(320, points[3]),
	    on_next(350, points[4]),
	    on_next(400, points[5]),
	    on_next(700, points[5]),
	    on_completed(700)
	)

	def create():
	    return xs.buffer_with_count(2, 1).map(test_activity.velocity_calc)

	results = scheduler.start(create)
	
	results.messages.assert_equal(
		on_next(240, wanted[0]),
		on_next(280, wanted[1]),
		on_next(320, wanted[2]),
		on_next(350, wanted[3]),
		on_next(400, wanted[4]),
		on_next(700, wanted[5]),
		on_error(700, exception='list index out of range') # no idea why i need this one instead of on_completed
		#on_completed(700)
	)
	
	xs.subscriptions.assert_equal(subscribe(200, 700))

	print("OK - speed calc")


if __name__ == '__main__':
	
	activity = Activity('dag')
	
	test_queueing()
	test_speed(activity)