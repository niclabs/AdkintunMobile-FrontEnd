/**
  Represents a Polygon Map of a country's regions and communes
  @constructor
  @param {string} containerId - Id of the DOM object which will contain the map
  @param {string} regionsUrl - Location of the GeoJSON file with the country's regions
  @param {string} communesUrl - Location of the GeoJSON file with the country's communes
*/
var PolygonMap = function (containerId, regionsUrl, communesUrl) {
  this.containerId = containerId;
  this.regionsUrl = regionsUrl;
  this.communesUrl = communesUrl;

  this.regionSelectedObververs = []
  this.communeSelectedObververs = []

  var w = window,
  d = document,
  e = d.documentElement,
  g = d.getElementsByTagName('body')[0],
  x = w.innerWidth || e.clientWidth || g.clientWidth,
  y = w.innerHeight|| e.clientHeight|| g.clientHeight;

  // TODO Use the container's properties to define width and height
  this.screenWidth = x;
  this.screenHeight = y;
  this.width = 0.2 * x,
  this.height = 0.9 * y,
  this.centeredFeature;
  this.zoom = 1;

  this.tooltip = d3.select("#polygonMap").append("div").attr("class", "tooltip hidden");
  this.path_object = d3.geo.path();

  var svg = d3.select("#polygonMap").append("svg")
    .attr("width", "100%")
    .attr("height", "100%");
  svg.append("rect")
    .attr("class", "background")
    .attr("width", "100%")
    .attr("height", "100%")
  this.g = svg.append("g");
  this.loadMap();
};

/**
  Initializes the map.
  The function loads the map's data from the GeoJSON files
  specified in the constructor and renders them.
*/
PolygonMap.prototype.loadMap = function () {
  var mapReference = this;
  d3.json(this.regionsUrl, function(error, country){
    if (error){
      console.error(error);
      return;
    }
    var regions = topojson.feature(country, country.objects.regiones);
    mapReference.path_object.projection(mapReference.computeProjection(regions));

    mapReference.g.append("g")
      .attr("id", "regions")
      .selectAll("path")
      .data(regions.features)
      .enter().append("path")
      .attr("d", mapReference.path_object)
      .attr("id", function(d){return d.id;})
      .on("click", onRegionClick);
    mapReference.g.append("path")
      .datum(topojson.mesh(country, country.objects.regiones, function(a, b) { return a !== b; }))
      .attr("id", "region-borders")
      .attr("d", mapReference.path_object);
    d3.selectAll("#regions").selectAll("path")
      .on("mouseover", onRegionMouseover)
      .on("mouseout", onRegionMouseout);
    d3.selectAll(".background")
      .on("click", onRegionClick);
    d3.json(mapReference.communesUrl, function(error, country) {
      if (error) {
        return console.error(error);
      }

      mapReference.g.append("g")
        .attr("id", "communes")
        .selectAll("path")
        .data(topojson.feature(country, country.objects.comunas).features)
        .enter().append("path")
        .attr("d", mapReference.path_object)
        .attr("region",
        function(d){return d.properties["region_id"];})
        .on("click", onCommuneClick)
        .on("mouseover", onCommuneMouseover)
        .on("mouseout", onCommuneMouseout);

      mapReference.g.append("g")
        .attr("id", "commune-borders")
        .selectAll("path")
        .data(regions.features)
        .enter().append("g")
        .attr("region", function(d){return d.id;})
        .each(function(d,i){
          d3.select(this).append("path")
            .datum(topojson.mesh(country, country.objects.comunas,
               function(a, b) {
                  return a !== b && a.properties["region_id"] == d.id &&
                                    b.properties["region_id"] == d.id; }))
            .attr("d", mapReference.path_object);
        });
    });


  });


  d3.json("http://localhost:3000/comunas/13501/lineas", function(error, country){
    if (error){
      console.log("Error loading atacama");
      return;
    }
    mapReference.atacama = country;
  });

  /**Function called when the click event is triggered for a region*/
  function onRegionClick(d){
    if (d && mapReference.centeredFeature !== d) {
      screenCentroid = mapReference.path_object.centroid(d);
      pos_x = screenCentroid[0];
      pos_y = screenCentroid[1];
      bboxProjection = mapReference.computeProjection(d);
      scale = bboxProjection.scale();
      mapReference.zoom = scale / mapReference.path_object.projection().scale();
      mapReference.centeredFeature = d;
      // Notify observers
      for (var i = 0; i < mapReference.regionSelectedObververs.length; i++){
        mapReference.regionSelectedObververs[i](d);
      }
    }
    else {
      pos_x = mapReference.width / 2;
      pos_y = mapReference.height / 2;
      mapReference.zoom = 1;
      mapReference.centeredFeature = null;
    }

    mapReference.g.selectAll("path")
        .classed("active", mapReference.centeredFeature && function(d) { return d === mapReference.centeredFeature; });
    mapReference.g.selectAll("#communes").selectAll("path")
        .classed("active", mapReference.centeredFeature &&
          function(d) {
            return mapReference.centeredFeature.id == d.properties["region_id"];
          });
    mapReference.g.transition()
        .duration(750)
        .attr("transform", "translate(" + mapReference.width/2 + "," + mapReference.height/2 + ")scale(" +
              mapReference.zoom + ")translate(" + -pos_x + "," + -pos_y + ")")
        .style("stroke-width", 1.5 / mapReference.zoom + "px");
  }

  /**
  Function called when the click event is triggered for a commune.
  When the map is not zoomed (i.e. communes are not displayed) it dispatches
  the click event to the corresponding region.
  */
  function onCommuneClick(d){
    region = d.properties["region_id"];
    if (mapReference.centeredFeature && region == mapReference.centeredFeature.id){
      screenCentroid = mapReference.path_object.centroid(d);
      geoCentroid = d3.geo.centroid(d);
      // if (typeof move_center == 'function') {
      //   move_center(latlng[1], latlng[0]);
      // }
      // Notify observers
      for(var i = 0; i < mapReference.communeSelectedObververs.length ; i++){
        mapReference.communeSelectedObververs[i](d);
      }
    }
    else{
      region_path = d3.selectAll("path").filter(function(d,i) {if (d) {return d.id == region ? this : null}});
      var e = document.createEvent('UIEvents');
      e.initUIEvent('click', true, true, window, 1);
      region_path.node().dispatchEvent(e);
    }
  }

  /**Function called when the mouseover event is triggered for a region*/
  function onRegionMouseover(d){
    screenCentroid = mapReference.path_object.centroid(d);
    mapReference.tooltip.classed("hidden", false)
      .attr("style", "left:"+(mapReference.screenWidth - mapReference.width + screenCentroid[0])+
                      "px;top:" + (screenCentroid[1]) + "px")
      .html(d.properties.region_name);
    d3.select(this).classed("hover", true);
  }

  /**Function called when the mouseout event is triggered for a region*/
  function onRegionMouseout(d){
    mapReference.tooltip.classed("hidden", true);
    d3.selectAll(".hover").classed("hover", false);
  }

  /**
  Function called when the mouseover event is triggered for a commune.
  When the map is not zoomed (i.e. communes are not displayed) it dispatches
  the mouseover event to the corresponding region.
  */
  function onCommuneMouseover(d){
    region = d.properties["region_id"];
    if (mapReference.centeredFeature){
      if (region == mapReference.centeredFeature.id){
        commune_bbox = this.getBoundingClientRect();
        mapReference.tooltip
          .classed("hidden", false)
          .attr("style", "left:"+(commune_bbox.left+commune_bbox.width/2)+"px;top:"+(commune_bbox.top+commune_bbox.height/2)+"px")
          .html(d.properties.commune_name + "<br>Población: " + d.properties.population_2012);
        d3.select(this).classed("hover", true);
      }
    }
    else{
      region_path = d3.selectAll("path").filter(function(d,i) {if (d) {return d.id == region ? this : null}});
      var e = document.createEvent('UIEvents');
      e.initUIEvent('mouseover', true, true, window, 1);
      region_path.node().dispatchEvent(e);
    }
  }
  /**
  Function called when the mouseoutver event is triggered for a commune.
  When the map is not zoomed (i.e. communes are not displayed) it dispatches
  the mouseout event to the corresponding region.
  */  function onCommuneMouseout(d){
  region = d.properties["region_id"];
  if (mapReference.centeredFeature){
    if (region == mapReference.centeredFeature.id){
      mapReference.tooltip.classed("hidden", true);
      d3.selectAll(".hover").classed("hover", false);
    }
  }
  else{
    region_path = d3.selectAll("path").filter(function(d,i) {if (d){return d.id == region ? this : null}});
    var e = document.createEvent('UIEvents');
    e.initUIEvent('mouseout', true, true, window, 1);
    region_path.node().dispatchEvent(e);
  }
  }
};

/**
  Computes a projection that will make the specified feature fit
  the map's container
  @param {GeoJSON feature} feature - The feature which will be made to fit the container
  @return {d3.geo.projection} The projection which makes the specified feature fit the map's container
*/
PolygonMap.prototype.computeProjection = function (feature) {
  var center = d3.geo.centroid(feature);
  var scale  = 150;
  var offset = [this.width/2, this.height/2];
  var projection = d3.geo.mercator()
      .scale(scale)
      .center(center)
      .translate(offset);

  var path = d3.geo.path();
  path.projection(projection);

  var bounds  = path.bounds(feature);
  var hscale  = scale*this.width  / (bounds[1][0] - bounds[0][0]);
  var vscale  = scale*this.height / (bounds[1][1] - bounds[0][1]);
  var scale   = (hscale < vscale) ? hscale : vscale;
  var offset  = [this.width - (bounds[0][0] + bounds[1][0])/2,
                this.height - (bounds[0][1] + bounds[1][1])/2];

  projection = d3.geo.mercator()
      .center(center)
      .scale(scale).
      translate(offset);
  return projection;
};
PolygonMap.prototype.registerRegionSelectedObserver = function (observer) {
  if (typeof observer == 'function'){
    this.regionSelectedObververs.push(observer);
  }
};
PolygonMap.prototype.unregisterRegionSelectedObserver = function (observer) {
  // TODO Remove observer from list
};
PolygonMap.prototype.registerCommuneSelectedObserver = function (observer) {
  if (typeof observer == 'function'){
    this.communeSelectedObververs.push(observer);
  }
};
PolygonMap.prototype.unregisterCommuneSelectedObserver = function (observer) {
  // TODO Remove observer from list
};
