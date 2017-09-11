## Second mandatory assignment:
# Re:activity - A reactive bike computer

In this assignment you will make a near real-time reactive bike computer. The overall idea is that you will have a bike computer that is always online. The computer connects over the mobile network (3G) and streams its current position to a the **Re:activity** cloud service. The **Re:activity** cloud service will react to the incoming data, and enrich the stream with insights that it will feed back to the client.

The **Re:activity** cloud service also receives data from other riders, and can also produce insights based on the data produced by these other riders.

![WebClient](./pre/img/webclient.png)

The `pre` folder contains an example server and test client. Please note that this code have only been tested with Python 3.5+:

* `server.py` An example **Re:activity** server that supports multiple (test) clients using web sockets.
* `testclient` A test client that will replay data from the gpx files in the data folder.

The `pre/data` folder contains:
* Test GPX data files from 12 real cyclist from the [Tour d'Afrique](http://tdaglobalcycling.com/tour-dafrique) 2017, stage 109, Sesriem - Betta (137 km) going through the Namib desert. You can replay this data using `testclient.py`.

To use the example code you will need to signup for a Google Maps API key and add it to `server.py`. You also need to install some required libraries:

```bash
> pip3 install rx
> pip3 install tornado
> pip3 install jinja2
> pip3 install python-dateutil
> pip3 install geopy
```

In first terminal:
```bash
> python3 server.py
```

In second terminal:
```bash
> python3 testclient.py
```

To use a web client, point your browser to:
[http//localhost:8080](http//localhost:8080)

To follow a particular cyclist:
[http//localhost:8080/users/dag](http//localhost:8080/users/dag)

**NOTE:** If you cannot get the example code to work, and you get the "SecurityError: The operation is insecure" on Firefox (console), then make sure you reopen a new window or tab, and that you are not reusing an existing one.

# What we expect from you

In this assingments we expect that you use [RxPY](https://github.com/ReactiveX/RxPY) to transform the stream of GEO events into streams of insights such as:

* Current speed (km/h)
* Max speed (km/h)
* Moving average speed for the last 5 minutes, with timeshift of 1 minute (km/h)
* Time to destination (-25.3825800,16.4237190), based on avg speed.
* Time to sunset. Cycling in Africa after dark is very dangerous (cars and wild animals), so you better reach the destination before the sun goes down. https://sunrise-sunset.org/api. Note that you may not use this API in a manner that exceeds reasonable request volume.
* Use Google reverse geocoding API to lookup names for points of interrest (POI). Such places may be start, stops along the way, destination etc.

**NOTE:** All analytics code must be unit-tested. Analytics code that deals with time must be unit-tested in virtual time.

## Notifications

* Rider detection (you are passing/or being passed by someone)
* [Lunch](http://tdaglobalcycling.com/2013/04/the-lunch-truck/) or [coke-stop](http://tdaglobalcycling.com/2015/03/i-really-want-a-coke-stop/) detection. Other riders have stopped at this place. Give a notification to the user when he/she is approaching.

## Friends

* Produce a TopN people model (ordered collection of people) that are the most relevant to to a given rider. This is the people you cycle the most together with, or pass on your way.

# Hand-in

The usual:

* Code in `src/`
* Report in `doc/`

### Deadline

The final Hand-in must be pushed to your own repository in the classroom prior to:

* October 4. 23:00

# Bonus points

* Make a dashboard on the web-page that displays produced insights and notifications for a given rider.
* Display a notification to other riders if a rider breaks the laws of cycling physics (been picked up by a car)
* Sunset notification to make a rider speed up to reach destination before dark
* Explain if the produced insights are hot or cold based on when a client connects to the server (hint: will all clients see the same view for a given rider?).
* Move parts of the solution client-side using RxJS.
* Make something cool.

# Resources on reactive programming

* RxPY, https://github.com/ReactiveX/RxPY
* Aioreactive, https://github.com/dbrattli/aioreactive
* ReactiveX introduction, http://reactivex.io/intro.html
* Introduction to Rx (online book), http://www.introtorx.com/
* RxJava wiki, https://github.com/ReactiveX/RxJava/wiki
* Rx Virtual Time, https://channel9.msdn.com/Shows/Going+Deep/Wes-Dyer-and-Jeffrey-Van-Gogh-Inside-Rx-Virtual-Time
* Channel 9, Rx, https://channel9.msdn.com/Tags/rx
* Hot and Cold Observables, http://davesexton.com/blog/post/Hot-and-Cold-Observables.aspx, http://www.introtorx.com/content/v1.0.10621.0/14_HotAndColdObservables.html

### Happy Rx hacking!

![NamibRand](./pre/img/namibrand.jpg)

* NamibRand, http://www.info-namibia.com/activities-and-places-of-interest/sossusvlei/namibrand-nature-reserve
