var clusterMarkers = [];
var markers = [];
var size;
var idToName;
var map;
var lastZoom;
var lastCarrier;
var markers = [];
var mc;
function initMap() {
    var Santiago = {lat: -33.447487, lng: -70.673676};
    map = new google.maps.Map(document.getElementById('map'), {
        center: Santiago,
        zoom: 7
    });
    var mcOptions = {maxZoom: 15, imagePath: 'static/img/clusterer/m'};
    mc = new MarkerClusterer(map, [], mcOptions);
    google.maps.event.addListener(map, 'idle', getMarkers);
}


function getMarkers() {
    var url = $SCRIPT_ROOT + "/getGsmCount";
    var carrier = $('#sel1').val();
    var zoom = map.getZoom();
    var bounds = map.getBounds();
    var sw = bounds.getSouthWest();
    var ne = bounds.getNorthEast();
    var mapBounds = {
        "ne" : {
            "lat" : ne.lat(),
            "lon" : ne.lng()
        },
        "sw" : {
            "lat" : sw.lat(),
            "lon" : sw.lng()
        }
    }
    var jqxhr = $.getJSON(url, {
        carrier: carrier,
        zoom: zoom,
        lastZoom: lastZoom,
        lastCarrier: lastCarrier,
        mapBounds: JSON.stringify(mapBounds),
    }, function () {
    })
        .done(function (response) {
            if (response.action != "notChange"){
                mc.clearMarkers();
                deleteMarkers();
                locations = response.locations;
            }
            if (response.action == "change") {
                $.each(locations, function (key, data) {
                    visualization = new NetworkVisualization(response.data[key]);
                    var marker = new google.maps.Marker({
                        position: {lat: data.lat, lng: data.lon},
                        visualization: visualization,
                        name: data.name,
                        icon: {
                            path: google.maps.SymbolPath.CIRCLE,
                            scale: getScale(zoom),
                            fillOpacity: 0.4,
                            strokeOpacity: 0.4,
                            strokeColor: visualization.getColorMarker(),
                            fillColor: visualization.getColorMarker(),
                        },
                        map: map,
                        quantity: data.quantity,
                    });
                    markers.push(marker);
                    marker.addListener('mouseover', function () {
                        $("#info").html(
                            "<h3>Información de la " + response.type + "</h3>" +
                            "<h4>" + this.name + "</h4>" +
                            "<br> <b>Cantidad de eventos</b>: " + this.quantity +
                            "<div id = 'chart'></div>"
                        )
                        ;
                        var chart = c3.generate({
                            data: {
                                colors: this.visualization.getColorChart(),
                                columns: this.visualization.getDataChart(),
                                type: 'pie',
                            }
                        });
                    });
                    marker.addListener('click', function () {
                        this.setMap(null);
                        map.setCenter(this.position);
                        zoomAndUpdate();
                    });
                });
            }
            else if (response.action == "cluster") {
                $.each(locations, function (index, data) {
                    var marker = new google.maps.Marker({
                        position: {lat: data.lat, lng: data.lon},
                    });
                    mc.addMarker(marker);
                });
            }
            else if (zoom != lastZoom) {
                $.each(markers, function (index, marker) {
                    marker.icon.scale = getScale(zoom);
                });
            }
            lastZoom = zoom;
        });
}

// Sets the map on all markers in the array.
function setMapOnAll(map) {
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(map);
    }
}

// Removes the markers from the map, but keeps them in the array.
function clearMarkers() {
    setMapOnAll(null);
}

// Shows any markers currently in the array.
function showMarkers() {
    setMapOnAll(map);
}

// Deletes all markers in the array by removing references to them.
function deleteMarkers() {
    clearMarkers();
    markers = [];
}

function getScale(zoom) {
    if (zoom > 9) {
        return zoom / 2;
    }
    else {
        return 1.2 * zoom;
    }
}

function zoomAndUpdate() {
    var zoom = map.getZoom();
    if (zoom <= 8) {
        map.setZoom(11);
    }
    else if (zoom <= 11){
        map.setZoom(14);
    }
    getMarkers();
}