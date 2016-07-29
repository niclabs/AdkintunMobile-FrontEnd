var clusterMarkers = [];
var markers = [];
var size;
var idToName;
var map;
var lastZoom;
var markers = [];

function initMap() {
    var Santiago = {lat: -33.447487, lng: -70.673676};
    map = new google.maps.Map(document.getElementById('map'), {
        center: Santiago,
        zoom: 7
    });
    google.maps.event.addListener(map, 'idle', getMarkers);
}


function getMarkers() {
    var url = $SCRIPT_ROOT + "/getGsmCount";
    var carrier = $('#sel1').val();
    var zoom = map.getZoom();
    var jqxhr = $.getJSON(url, {carrier: carrier, zoom: zoom, lastZoom: lastZoom}, function (response) {
        if (response.action == "change") {
            deleteMarkers();
            locations = response.locations;
            $.each(locations, function (key, data) {
                visualization = new NetworkVisualization(response.data[key]);
                var marker = new google.maps.Marker({
                    position: {lat: data.lat, lng: data.lon},
                    visualization: visualization,
                    name: data.name,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10,
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
                    $body.addClass("loading");
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
            });
        }
        lastZoom = zoom;
    })
        .done(function () {
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