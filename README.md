# Second mandatory assignment: Re:activity - A reactive bike activity computer

In this assignment you will make a near real-time reactive bike computer. The overall idea is that you will have a bike computer that is always online. The computer connects and streams its current position to a the **Re:activity** cloud service. The **Re:activity** cloud service will react to the incoming data, and produce insights from the stream of events that it will feed back to the client.

The **Re:activity** cloud service may also produce insights from the data produced by riders cycling nearby yourself.

![WebClient](./webclient.png)

The `pre` folder contains an example server and test client:

* `server.py` An example **Re:activity** server that supports multiple (test) clients using web sockets.
* `testclient` A test client that will replay data from the gpx files in the data folder.

The `pre/data` folder contains:
* Test GPX data files from 12 real cyclist from the [Tour d'Afrique](http://tdaglobalcycling.com/tour-dafrique) 2017, stage 109, Sesriem - Betta (137 km) going through the Namib desert.

To use the example code you will need to signup for a Google Maps API key and add it to `server.py`.

In first terminal:
`> python3 server.py`

In second terminal:
`> python3 testclient.py`

To use a web client, point your browser to:
[http//localhost:8080](http//localhost:8080)

To follow a particular cyclist:
[http//localhost:8080/users/dag](http//localhost:8080/users/dag)

# What we expect from you

In this assingments we expect that you use [RxPY](https://github.com/ReactiveX/RxPY) to transform the stream of GEO events into streams of insights such as:

* Current speed (km/h)
* Max speed (km/h)
* Moving average speed for the last minute (km/h)
* Time to destination (-25.3825800,16.4237190), based on avg speed .
* Time to sunset. Cycling in Africa after dark is very dangerous (cars and wild animals), so you better reach the destination before the sun goes down. https://sunrise-sunset.org/api. Note that you may not use this API in a manner that exceeds reasonable request volume.

**NOTE:** All analytics code must be unit-tested. Analytics code that deals with time must be unit-tested in virtual time.

## Notifications

* Rider detection (you are passing/or being passed by someone)
* [Lunch](http://tdaglobalcycling.com/2013/04/the-lunch-truck/) or [coke-stop](http://tdaglobalcycling.com/2015/03/i-really-want-a-coke-stop/) detection. Other riders have stopped at this place.

## Trending People

* Produce a people model (collection of people) that are the most relevant to to a given rider. This is the people you cycle the most together with, or pass on your way.

# Hand-in

The usual:

* Code in `src/`
* Report in `doc/`

# Bonus points

* Make a cool dashboard on the web-page that displays the produced insights and notifications for a given rider.
* Sunset notification. Speed up to reach destination before dark
* Make something cool.

# Resources on reactive programming

* RxPY, https://github.com/ReactiveX/RxPY
* Aioreactive, https://github.com/dbrattli/aioreactive
* ReactiveX introduction, http://reactivex.io/intro.html
* Introduction to Rx (online book), http://www.introtorx.com/
* RxJava wiki, https://github.com/ReactiveX/RxJava/wiki
* Rx Virtual Time, https://channel9.msdn.com/Shows/Going+Deep/Wes-Dyer-and-Jeffrey-Van-Gogh-Inside-Rx-Virtual-Time
* Channel 9, Rx, https://channel9.msdn.com/Tags/rx
* NamibRand, http://www.info-namibia.com/activities-and-places-of-interest/sossusvlei/namibrand-nature-reserve
