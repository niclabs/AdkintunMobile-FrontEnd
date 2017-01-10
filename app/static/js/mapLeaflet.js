$(document).ready(function initmap() {
    var map = L.map('map');
    var Santiago = [-33.447487, -70.673676];
    map.setView(Santiago, 9);

    // add an OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        maxZoom: 16,
        attribution: '&amp;copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    var markers = L.markerClusterGroup();

    var markerList = [];

    var jqxhr = $.getJSON($SCRIPT_ROOT + "/getGsmCount", {}, function () {
    })
        .done(function (response) {
            $.each(response, function (id, location) {
                var marker = L.marker(L.latLng(location.lat, location.lon));
                markerList.push(marker);
            });
            markers.addLayers(markerList);
            map.addLayer(markers);
        });
});
