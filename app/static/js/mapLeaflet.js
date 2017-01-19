var map;
var markerCluster;
var markerList;


function mouseOverEvent(dataAntennas) {
    return function (e) {

        if (dataAntennas["Total"] === 0) {
            $("#infoGraph").show();
            $("#infoGraph").html(
                "<br> <div class='text-center'> <b> No hay información disponible para mostrar </b> </div> </br>");
        }
        else {
            $("#infoGraph").show();
            $("#infoGraph").html(
                "<div id='antennaChart'></div>" +
                "<div class='alert alert-success'> " +
                "<strong>Operador para esta antena: </strong>" + dataAntennas["carrier"] + "<br>" +
                "<strong>Cantidad de eventos registrados: </strong>" + dataAntennas["Total"] +
                "</div>");
            var chart = c3.generate({
                bindto: '#antennaChart',
                data: {
                    columns: [
                        ['2G', dataAntennas["2G"]],
                        ['3G', dataAntennas["3G"]],
                        ['4G', dataAntennas["4G"]],
                        ['Otras', dataAntennas["Otras"]]
                    ],
                    type: 'pie',
                    onclick: function (d, i) {
                        console.log("onclick", d, i);
                    },
                    onmouseover: function (d, i) {
                        console.log("onmouseover", d, i);
                    },
                    onmouseout: function (d, i) {
                        console.log("onmouseout", d, i);
                    },
                },
                legend: {
                    item: {
                        onclick: function () {
                        }
                    }
                },
                title: {
                    text: "Cantidad de eventos por tipo de red"
                }
            })
        }
    };
}

$(document).ready(function initmap() {
    map = L.map('map');
    var Santiago = [-33.447487, -70.673676];
    map.setView(Santiago, 9);
    // add an OpenStreetMap tile layer
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        noWrap: true,
        minZoom: 4,
        maxZoom: 16,
        attribution: '&amp;copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    markerCluster = L.markerClusterGroup();
    markerList = [];

    customMarker = L.Marker.extend({
        options: {
            carrier: 'Place your carrier here'
        }
    });

    var carrier = '0';

    map.spin(true);
    var jqxhr = $.getJSON($SCRIPT_ROOT + "/getGsmCount", {
        carrier: carrier,
    }, function () {
    })
        .done(function (response) {

            $("#info").html(
                "<div class='alert alert-info'> " +
                "<strong>Cantidad de antenas del carrier seleccionado: </strong>" + response.totalAntennas + "</div>"
            );

            $.each(response.antennasData, function (id, data) {
                var marker = new customMarker(L.latLng(data.lat, data.lon),
                    {
                        carrier: data['carrier']
                    }).on('mouseover', mouseOverEvent(data));
                marker.bindPopup(
                    "<b>Operador: </b>" + data['carrier'] +
                    "<br>" +
                    "<b>Cantidad de eventos: </b>" + data['Total']
                );
                marker.on('mouseover', function (e) {
                    marker.openPopup();
                });
                marker.on('mouseout', function (e) {
                    marker.closePopup();
                });
                markerList.push(marker);
            });
            markerCluster.addLayers(markerList);
            map.addLayer(markerCluster);

            var group = L.featureGroup(markerList);
            map.setMaxBounds(group.getBounds().pad(0.1));

            map.spin(false);

        });
});

$(document).ready(function () {
    markerCluster.on('clustermouseover', function (c) {

        var markers = c.layer.getAllChildMarkers();
        var carrierDist = {}

        for (var i = 0; i < markers.length; i++) {
            var marker = markers[i];

            if (marker.options['carrier'] in carrierDist)
                carrierDist[marker.options['carrier']] += 1;
            else
                carrierDist[marker.options['carrier']] = 1;
        }

        var text = "";
        $.each(carrierDist, function(k,v){
            text += "<li>" + k + " : " + v + "</li>"
        })

        var popup = L.popup()
            .setLatLng(c.layer.getLatLng())
            .setContent('<b>Cantidad de antenas por operador en el cluster: </b>' + '<br>' + text)
            .openOn(map);

        $("#infoGraph").show();
        $("#infoGraph").html(
            "<div id='antennaChart'></div>"
        );
        var chart = c3.generate({
            bindto: '#antennaChart',
            data: {
                json: carrierDist,
                type: 'pie',
                onclick: function (d, i) {
                    console.log("onclick", d, i);
                },
                onmouseover: function (d, i) {
                    console.log("onmouseover", d, i);
                },
                onmouseout: function (d, i) {
                    console.log("onmouseout", d, i);
                },
            },
            legend: {
                item: {
                    onclick: function () {
                    }
                }
            },
            title: {
                text: 'Cantidad de antenas por operador en el cluster'
            }
        })
    }).on('clustermouseout', function (c) {
        map.closePopup();
    }).on('clusterclick', function (c) {
        map.closePopup();
        $("#infoGraph").hide();
    })
})

$(document).ready(function () {
    $('#sel1').on('change', function (e) {

        $('#infoGraph').hide();

        var carrier = this.value;

        markerCluster.clearLayers();
        var markerList = [];

        customMarker = L.Marker.extend({
            options: {
                carrier: 'Place your carrier here'
            }
        });

        map.spin(true);
        var jqxhr = $.getJSON($SCRIPT_ROOT + "/getGsmCount", {
            carrier: carrier,
        }, function () {
        })
            .done(function (response) {

                $("#info").html(
                    "<div class='alert alert-info'> <strong>Cantidad de antenas del carrier seleccionado: </strong>" + response.totalAntennas + "</div>"
                );

                $.each(response.antennasData, function (id, data) {
                    var marker = new customMarker(
                        L.latLng(data.lat, data.lon),
                        {carrier: data['carrier']}
                    ).on('mouseover', mouseOverEvent(data));
                    marker.bindPopup(
                        "<b>Operador: </b>" + data['carrier'] +
                        "<br>" +
                        "<b>Cantidad de eventos: </b>" + data['Total']
                    );
                    marker.on('mouseover', function (e) {
                        marker.openPopup();
                    });
                    marker.on('mouseout', function (e) {
                        marker.closePopup();
                    });
                    markerList.push(marker);
                });
                markerCluster.addLayers(markerList);
                map.addLayer(markerCluster);

                map.spin(false);
            });
    });
});

