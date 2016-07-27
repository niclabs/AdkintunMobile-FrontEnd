var clusterMarkers = [];
var markers = [];
var size;
var idToName;
var map;
var lastZoom;
var test;
function initMap() {
    var Santiago = {lat: -33.447487, lng: -70.673676};
    map = new google.maps.Map(document.getElementById('map'), {
    center: Santiago,
    zoom: 7
    });
    google.maps.event.addListener(map, 'idle', getMarkers);
}


    function getMarkers(){
    var url = $SCRIPT_ROOT+"/getGsmCount";
    var carrier = $('#sel1').val();
    var zoom = map.getZoom();
    var jqxhr = $.getJSON(url, {carrier : carrier, zoom : zoom, lastZoom : lastZoom},function() {})
        .done(function(response) {
            data = response.regions;
            $.each(data, function( key, data ) {
                var marker = new google.maps.Marker({
                    position: {lat: data.lat, lng: data.lon},
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10,
                        fillOpacity: 0.6,
                        strokeOpacity: 0.6,
                        strokeColor: "#FF7F50",
                        fillColor: "#FF7F50"
                    },
                    map: map,
                    types: response.dataRegion[key],
                    quantity: data.quantity,
                });
                marker.addListener('mouseover', function() {
                    $("#info").html(
                  "<h3>Información de la región</h3>" +
                  "<br> <b>Cantidad de eventos</b>: " + this.quantity +
                  "<div id = 'chart'></div>");
                    var chart = c3.generate({
                        data: {
                            // iris data from R
                            columns: this.types,
                            type : 'pie',
                        }
                    });
                });

            });
            console.log(response.dataRegion[1]);
            lastZoom = zoom;
        });
}

//