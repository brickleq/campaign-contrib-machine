// Create a starting layer for donations data
var layer = new L.LayerGroup();

// Creating map object
var map = L.map("map", {
  center: [40.1629, -89.1896],
  zoom: 6,
  layers: [layer]
});
// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: "pk.eyJ1Ijoic3Jtb250ZWlybyIsImEiOiJjandyMTJzNjgwMDgyNDNwZDUwNWpkN2NoIn0.rggDqMijR64cH-l9E6JVag"
}).addTo(map);

function addGeoJson(data, layer){
  L.geoJson(data, {
    style: function(feature) {
      return {
        color: 'blue',
        fillOpacity: 0.3,
        weight: 1
      };
    }
  }).addTo(layer);
  map.fitBounds(L.geoJson(data).getBounds());
};
      
 // PARTY SELECTOR 

function init() {
  var zipcode = d3.select("#zipcode").text()
  d3.json("/api/zipcode_geo/" + zipcode, function(data) {
    // Creating a geoJSON layer with the retrieved data
    addGeoJson(data, layer); 
  });
};

// Initialize the dashboard
init();