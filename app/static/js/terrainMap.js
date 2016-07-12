var TerrainMap = function(containerId, jsonUrl) {

  this.containerId = containerId;
  this.jsonUrl = jsonUrl;

  this.map = L.map("googleMap").setView([-33.456765, -70.662067], 5);
  L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
  }).addTo(this.map);
  self = this;
  this.featureMap = [];
  this.lineObservers = [];

  var lineStyle = {fillOpacity: 0.3, color: '#ff0000'};
  var HighlightLineStyle = {fillOpacity: 0.3, color: '#000000'};
  mapReference = this;
  this.geoJsonLayer = L.geoJson(null,{
    onEachFeature : function(feature, layer){
      self.featureMap.push({feature:feature, layer:layer});
      if (feature.properties.hasOwnProperty("feat_id")){
        layer.on({
          "click": function (event){
                  // Notify observers
            for(var i = 0; i < mapReference.lineObservers.length ; i++){
              mapReference.lineObservers[i](feature);
            }

          },
          "mouseover": function (event){
            layer.setStyle(HighlightLineStyle);
            popupContent = "Id: " + feature.properties["feat_id"] + "<br>";
            popupContent += "Nombre: " + feature.properties["feat_name"] + "<br>";
            popupContent += "Tipo: " + feature.properties["feat_type"] + "<br>";
            layer.bindPopup(popupContent).openPopup();
          },
          "mouseout": function (event){
            layer.setStyle(lineStyle);
            layer.closePopup();
          }

        })
      }
    },
    style: function(feature){
      if (feature.properties.hasOwnProperty("commune_id")){
        return {fillOpacity: 0.3,  color: '#7d1e49', fillColor: '#ba6a8f'}
      }
      else if (feature.properties.hasOwnProperty("feat_id")){
        return lineStyle
      }
      else{
        return {fillOpacity: 0.2, color: '#4d8d7c', fillColor: '#c1ead6'}
      }
    }}
  ).addTo(this.map);
}


TerrainMap.prototype.loadMap = function() {
  var mapReference = this;
  d3.json(this.jsonUrl, function(json) {

    mapReference.overlay.onAdd = function() {
      mapReference.mouseTargetLayer = d3.select(this.getPanes().overlayMouseTarget)
        .append("div")
        .attr("height", "100%")
        .attr("width", "100%")
        .attr("class", "nodes");
      mapReference.overlayLayer = d3.select(this.getPanes().overlayLayer)
        .append("div")
        .attr("height", "100%")
        .attr("width", "100%")
        .attr("class", "nodes");
    };

    mapReference.overlay.draw = function() {
      var radius = 7;
      var projection = this.getProjection(),
        padding = 10;


      var node_coord = {};

      var marker = mapReference.mouseTargetLayer.selectAll("svg")
        .data(json.nodes)
        .each(transform) // update existing markers
        .enter().append("svg:svg")
        .each(transform)
        .attr("class", "marker");
      marker.append("svg:circle")
        .attr("r", radius)
        .attr("cx", padding)
        .attr("cy", padding)
        .on("mouseover",f_mouseover);
      function f_mouseover(d){
          d3.select(this).style("fill", "magenta")
      }
      marker.append("svg:text")
        .attr("x", padding + 7)
        .attr("y", padding)
        .attr("dy", ".37em")
        .text(function(d) { return d.id; });

      var markerLink = mapReference.overlayLayer.selectAll(".links")
        .data(json.links)
        .each(pathTransform) // update existing markers
        .enter().append("svg:svg")
        .attr("class", "links")
        .each(pathTransform);

      function pathTransform(d) {
          var t, b, l, r, w, h, currentSvg;
          $(this).empty(); // get rid of the old lines (cannot use d3 .remove() because i cannot use selectors after ... )

          dsrc = new google.maps.LatLng(node_coord[d.source-1 + "," + 1], node_coord[d.source-1 + "," + 0]);
          dtrg = new google.maps.LatLng(node_coord[d.target-1 + "," + 1], node_coord[d.target-1 + "," + 0]);
          d1 = projection.fromLatLngToDivPixel(dsrc);
          d2 = projection.fromLatLngToDivPixel(dtrg);
          line_top = Math.min(d1.y, d2.y)
          bottom = Math.max(d1.y, d2.y)
          right = Math.max(d1.x, d2.x)
          left = Math.min(d1.x, d2.x)
          r = radius/2
          currentSvg = d3.select(this)
            .style("left", left  + "px")
            .style("top", line_top - r  + "px")
            .style("width", (right - left - r) + "px")
            .style("height", (bottom - line_top - r) + "px");
          // drawing the diagonal lines inside the svg elements. We could use 2 cases instead of four but maybe you will need to orient your graph (so you can use some arrows)
          if (( d1.y < d2.y) && ( d1.x < d2.x)) {
              currentSvg.append("svg:line")
                .style("stroke-width", 1)
                .style("stroke", "black")
                .attr("y1", 0)
                .attr("x1", 0)
                .attr("x2", right-left)
                .attr("y2", bottom-line_top);
          }
          else if ((d1.x > d2.x) && (d1.y > d2.y)){
              currentSvg.append("svg:line")
                .style("stroke-width", 1)
                .style("stroke", "black")
                .attr("y1", 0)
                .attr("x1", 0)
                .attr("x2", right-left)
                .attr("y2", bottom-line_top);
          }
          else if (( d1.y < d2.y) && ( d1.x > d2.x)){
              currentSvg.append("svg:line")
                .style("stroke-width", 1)
                .style("stroke", "black")
                .attr("y1", 0)
                .attr("x2", 0)
                .attr("x1", right-left)
                .attr("y2", bottom-line_top);
          }
          else if ((d1.x < d2.x) && (d1.y > d2.y)){
              currentSvg.append("svg:line")
                .style("stroke-width", 1)
                .style("stroke", "black")
                .attr("y1", 0)
                .attr("x2", 0)
                .attr("x1", right-left)
                .attr("y2", bottom-line_top);
          }
          else {console.log("something is wrong!!!");}

          return currentSvg;
      }

      function transform(d,i) {
          node_coord[i + "," + 0] = d.lng;
          node_coord[i + "," + 1] = d.lat;

          d = new google.maps.LatLng(d.lat, d.lng);
          d = projection.fromLatLngToDivPixel(d);

          return d3.select(this)
            .style("left", (d.x - padding) + "px")
            .style("top", (d.y - padding) + "px");
      }
    };
    mapReference.overlay.setMap(mapReference.map);
  });
};

TerrainMap.prototype.panTo = function(lat, lng) {
    this.map.panTo([lat, lng]);
};

TerrainMap.prototype.zoomToBounds = function (left, right, top, bottom) {
    southWest = L.latLng(left, top),
    northEast = L.latLng(right, bottom),
    bounds = L.latLngBounds(southWest, northEast);
    this.map.fitBounds(bounds);
};

TerrainMap.prototype.addGeoJsonFeature = function (feature) {
    this.geoJsonLayer.addData(feature);
};
TerrainMap.prototype.removeGeoJsonFeature = function (feature) {
    for (var i = 0; i < this.featureMap.length; i++) {
      if (this.featureMap[i].feature == feature){
        layer = this.featureMap[i].layer;
        this.geoJsonLayer.removeLayer(layer);
        this.featureMap.splice(i, 1);
      }
    }
};
TerrainMap.prototype.removeAllGeoJsonFeatures = function () {
    this.featureMap = [];
    this.geoJsonLayer.clearLayers();
};
TerrainMap.prototype.removeGeoJsonFeatures = function (f) {
  i = this.featureMap.length;
  while (i--){
    if (f(this.featureMap[i].feature)){
      this.removeGeoJsonFeature(this.featureMap[i].feature);
    }
  }
};

TerrainMap.prototype.registerLineSelectedObserver = function (f) {
  this.lineObservers.push(f);
};
