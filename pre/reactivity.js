function getLocation(callback) {
    navigator.geolocation.getCurrentPosition(function (position) {
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        var alt = position.altitude;

        callback({ lat: lat, lng: lng, alt: alt });
    });
}

function initMap() {
    var hostname = $(location).attr('hostname');
    var username = $(location).attr('pathname').split("/").slice(-1);
    var port = $(location).attr('port');

    var myLatLng = {lat: -24.488141, lng: 15.800189};

    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 11,
        center: myLatLng,
        mapTypeId: google.maps.MapTypeId.TERRAIN
    });

    var markers = {};
    var latest = null;

    function getMarker(point) {
        var name = point.name;
        var icon = "http://maps.google.com/mapfiles/ms/icons/red-dot.png"

        if (name == username) {
            icon = "http://maps.google.com/mapfiles/ms/icons/green-dot.png";
        }

        if (!(name in markers)) {
            var marker = marker = new google.maps.Marker({
                map: map,
                title: name,
                icon: icon,
                animation: google.maps.Animation.DROP
            });
            markers[name] = marker;
        } else {
            var marker = markers[name];
        }

        return marker;
    }

    var url = "ws://" + hostname + ":" + port + "/ws/" +  username;
    console.log(url);
    var ws = new WebSocket(url);

    ws.onopen = function () {
        /*
        window.setInterval(function () {
            getLocation(function(pos) {
                ws.send(JSON.stringify(pos));
            });
        }, 50);
        */
    }

    ws.onmessage = function(msg) {
        var point = JSON.parse(msg.data);

        var marker = getMarker(point);
        marker.setPosition(point);

        if (point.name == username) {
            map.setCenter(point);
        }
    }
}
