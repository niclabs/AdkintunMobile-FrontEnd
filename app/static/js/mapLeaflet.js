var map;
var markerCluster;
var markerList;

function mouseOverEvent(dataAntennas) {
    return function (e) {
        console.log(JSON.stringify(dataAntennas, null, 4));
        console.log(dataAntennas);

        if (dataAntennas.Total === 0) {
            $("#infoGraph").html(
                "<br> <div class='text-center'> <b> No hay información disponible para mostrar </b> </div> </br>");
        }
        else {
            $("#infoGraph").html(
                "<div class='alert alert-success'> <strong>Cantidad de eventos para esta antena: </strong>" + dataAntennas.Total + "</div>" +
                "<div id='antennaChart'></div>");
            var chart = c3.generate({
                bindto: '#antennaChart',
                data: {
                    columns: [
                        ['2G', dataAntennas["2G"]],
                        ['3G', dataAntennas["3G"]],
                        ['4G', dataAntennas["4G"]],
                        ['Otras', dataAntennas.Otras]
                    ],
                    type: 'donut',
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
                donut: {
                    title: "Distribución de redes"
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

    var carrier = '0';

    var jqxhr = $.getJSON($SCRIPT_ROOT + "/getGsmCount", {
        carrier: carrier,
    }, function () {
    })
        .done(function (response) {

            $("#info").html(
                "<div class='alert alert-info'> <strong>Cantidad de antenas del carrier seleccionado: </strong>" + response.totalAntennas + "</div>"
            );

            $.each(response.antennasData, function (id, data) {
                var marker = L.marker(L.latLng(data.lat, data.lon)).on('mouseover', mouseOverEvent(data));
                markerList.push(marker);
            });
            markerCluster.addLayers(markerList);
            map.addLayer(markerCluster);

            var group = L.featureGroup(markerList);
            map.setMaxBounds(group.getBounds().pad(0.1));
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

                $("#info").html(
                    "<div class='alert alert-info'> <strong>Cantidad de antenas del carrier seleccionado: </strong>" + response.totalAntennas + "</div>"
                );

                $.each(response.antennasData, function (id, data) {
                    var marker = L.marker(L.latLng(data.lat, data.lon)).on('mouseover', mouseOverEvent(data));
                    markerList.push(marker);
                });
                markerCluster.addLayers(markerList);
                map.addLayer(markerCluster);
            });
    });
});

