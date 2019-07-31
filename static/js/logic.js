// Creating map object
var map = L.map("map", {
  center: [40.1629, -89.1896],
  zoom: 6
});

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: "pk.eyJ1Ijoic3Jtb250ZWlybyIsImEiOiJjandyMTJzNjgwMDgyNDNwZDUwNWpkN2NoIn0.rggDqMijR64cH-l9E6JVag"
}).addTo(map);

var link = "https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/" + 
"il_illinois_zip_codes_geo.min.json";




// Function that will determine the color of a neighborhood based on the borough it belongs to
function chooseColor(ZCTA5CE10) {
  switch (ZCTA5CE10) {
  case "60626":
    return "yellow";
  case "60611":
    return "red";
  case "60653":
    return "orange";
  case "60647":
    return "green";
  case "60632":
    return "purple";
  default:
    return "red";
  }
}

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  // Creating a geoJSON layer with the retrieved data
  L.geoJson(data, {
    // Style each feature (in this case a neighborhood)
    style: function(feature) {
      return {
        color: "white",
        // Call the chooseColor function to decide which color to color our neighborhood (color based on borough)
        fillColor: chooseColor(feature.properties.ZCTA5CE10),
        fillOpacity: 0.5,
        weight: 1.5
      };
    },
    // Called on each feature
    onEachFeature: function(feature, layer) {
      // Set mouse events to change map styling
      layer.on({
        // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
        mouseover: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.9
          });
        },
        // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.5
          });
        },
        // When a feature (neighborhood) is clicked, it is enlarged to fit the screen
        click: function(event) {
          map.fitBounds(event.target.getBounds());
        }
      });
      // Giving each feature a pop-up with information pertinent to it
      layer.bindPopup("<h5>" + feature.properties.ZCTA5CE10 + "</h5> <hr> <h5>" + feature.properties.borough + "</h5>");

    }
  }).addTo(map);
});

var api_url = '/api/donations/'
d3.json(api_url, function(data){
  console.log(data[0].zipcode)
});
