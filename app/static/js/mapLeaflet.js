var map;
var markerCluster;
var markerList;

$(document).ready(function initmap() {
    map = L.map('map');
    var Santiago = [-33.447487, -70.673676];
    map.setView(Santiago, 9);

    // add an OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 16,
        attribution: '&amp;copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    markerCluster = L.markerClusterGroup();
    markerList = [];

    var carrier = '0';

    var jqxhr = $.getJSON($SCRIPT_ROOT + "/getGsmCount", {
        carrier: carrier,
    }, function () {
    })
        .done(function (response) {
            $.each(response, function (id, location) {
                var marker = L.marker(L.latLng(location.lat, location.lon));
                markerList.push(marker);
            });
            markerCluster.addLayers(markerList);
            map.addLayer(markerCluster);
        });
});

$(document).ready(function () {
    $('#sel1').on('change', function (e) {
        var carrier = this.value;

        markerCluster.clearLayers();
        var markerList = [];

        var jqxhr = $.getJSON($SCRIPT_ROOT + "/getGsmCount", {
            carrier: carrier,
        }, function () {
        })
            .done(function (response) {
                $.each(response, function (id, location) {
                    var marker = L.marker(L.latLng(location.lat, location.lon));
                    markerList.push(marker);
                });
                markerCluster.addLayers(markerList);
                map.addLayer(markerCluster);
            });
    });
});
