var clusterMarkers = [];
var markers = [];
var size;
var idToName;
var map;
var lastZoom;
var global;
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
    var jqxhr = $.getJSON(url, {carrier: carrier, zoom: zoom, lastZoom: lastZoom}, function () {
    })
        .done(function (response) {
            data = response.regions;
            global = response.dataRegion[1];
            $.each(data, function (key, data) {
                visualization = new NetworkVisualization(response.dataRegion[key])
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
                marker.addListener('mouseover', function () {
                    global = this.visualization.getColorChart();
                    $("#info").html(
                        "<h3>Información de la región</h3>" +
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
            lastZoom = zoom;
        });
}

//