var clusterMarkers = [];
var markers = [];
var size;
var idToName;
var map;
var lastZoom;

function initMap() {
    var Santiago = {lat: -33.447487, lng: -70.673676};

    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 7.5,
        center: Santiago,
    });

    //google.maps.event.addListener(map, 'idle', getMarkers);
}


/* function getMarkers(){
    var url = $SCRIPT_ROOT+"/getGsmCount";
    var carrier = $('#sel1').val();
    var zoom = map.getZoom();
    var jqxhr = $.getJSON(url, {carrier : carrier, zoom : zoom, lastZoom : lastZoom},function() {})
        .done(function(response) {
            data = response.data;
            size = data.length;
            for (var i = 0; i < size; i++) {
                var marker = new google.maps.Marker({
                position: {lat: data[i].lat, lng: data[i].lon},
                icon: "http://chart.apis.google.com/chart?chst=d_map_pin_letter&chld="+data.quantity+"|FE6256|000000",
                map: map,
              });
            }
            lastZoom = zoom;
        });
} */
