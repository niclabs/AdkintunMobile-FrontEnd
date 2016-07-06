var clusterMarkers = [];
function initMap() {
    var Santiago = {lat: 	-33.447487, lng: -70.673676};

    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 8,
      center: Santiago,
    });
    var data = data_antennas;
    size = 5;//data.antennas.length;
    markers = [];
    for (var i = 0; i < size; i++) {
      var marker = new google.maps.Marker({
        position: {lat: data.antennas[i].lat, lng: data.antennas[i].lon},
      });
      marker.addListener('click', function() {
        document.write(marker.getPosition());
      });
      markers.push(marker);
    }
    markers.sort(function(a,b){
      return a.position.lat() > b.position.lat() ? 1:-1;
    })
    options = {
        imagePath: 'images/m'
      };

      mc = new MarkerClusterer(map,clusterMarkers,options);
    $.getJSON("comunas.json",function(data){
      var geoJsonObject = topojson.feature(data, data.objects.comunas)
      map.data.addGeoJson(geoJsonObject);
    });
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
      alert("dsa");
    }
    mc = new MarkerClusterer(map,clusterMarkers,options);
  }
