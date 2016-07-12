var clusterMarkers = [];
function initMap() {
    var Santiago = {lat: 	-33.447487, lng: -70.673676};

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 8,
      center: Santiago,
    });
    var data = data_antennas;
    size = 5000;//data.antennas.length;
    markers = [];
    for (var i = 0; i < size; i++) {
      markers.push(
        new google.maps.Marker({
          position: {lat: data.antennas[i].lat, lng: data.antennas[i].lon},
          mnc: data.antennas[i].mnc,
          lac: data.antennas[i].lac,
          cid: data.antennas[i].cid
        }));

      markers[i].addListener('click', function() {
          $("#info").html(
          "<h3>Información de la antena</h3>" +
          "<br> <b>Operador</b>: " + mncToName[this.mnc] +
          "<br> <b>Latitud</b>: " + this.getPosition().lat() +
          "<br> <b>Longitud</b>: " + this.getPosition().lng() +
          "<br> <b>Lac</b>: " + this.lac +
          "<br> <b>Cid</b>: " + this.cid);
          var lat = this.getPosition().lat();
          var long = this.getPosition().lng();
      });
    }
    markers.sort(function(a,b){
      return a.position.lat() > b.position.lat() ? 1:-1;
    })
    options = {
      imagePath: "static/img/clusterer/m"
    };

    mc = new MarkerClusterer(map,clusterMarkers,options);
    /*$.getJSON("comunas.topojson",function(data){
      var geoJsonObject = topojson.feature(data, data.objects.comunas)
      map.data.addGeoJson(geoJsonObject);
    });
    var polygonmap = new PolygonMap("map","regiones.topojson","comunas.topojson");*/
    google.maps.event.addListener(map, 'idle', showMarkers);
  }
  function lowerBound(lat){
    var min = 0;
    var max = size-1;
    var mid = (min+max)>>1;
    var ans = 0;
    while(min<=max){
      mid = (min+max)>>1;
      if(markers[mid].position.lat()<=lat){
        ans = mid;
        min = mid+1;
      }
      else{
        max = mid-1;
      }
    }
    return ans;
  }
  function upperBound(lat){
    var min = 0;
    var max = size-1;
    var mid = (min+max)>>1;
    var ans = 0;
    while(min<=max){
      mid = (min+max)>>1;
      if(markers[mid].position.lat()>=lat){
        ans = mid;
        max = mid-1;
      }
      else{
        min = mid+1;
      }
    }
    return ans;
  }
  function showMarkers() {
    clusterMarkers = [];
    mc.clearMarkers();
    var bounds = map.getBounds();
    var ne = bounds.getNorthEast();
    var so = bounds.getSouthWest();
    var inicio = upperBound(so.lat());
    var final = lowerBound(ne.lat());
    if ($("#sel1" ).val()==-1){
      for (var i = inicio; i <= final; i++) {
        clusterMarkers.push(markers[i]);
      }
    }
    else{
      for (var i = inicio; i <= final; i++) {
        if(markers[i].mnc == $("#sel1" ).val()){
          clusterMarkers.push(markers[i]);
        }
      }
    }
    mc = new MarkerClusterer(map,clusterMarkers,options);
  }
