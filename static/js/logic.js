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

var link = "/api/donations/";

// Function that will determine the color of a neighborhood based on the borough it belongs to
function chooseColor(indicator, maximum) {
  var H_value = (1 - (indicator / maximum))*100;
  return 'hsl(' + H_value + ', 100%, 50%)';
}

function chooseOpacity(indicator, maximum) {
  var H_value = (indicator / maximum);
  return H_value;
}

var map_variant = 'donations_sum'

// Grabbing our GeoJSON data..
d3.json(link, function(data) {
  // Creating a geoJSON layer with the retrieved data
  var maximum = data.maximums[map_variant]
  L.geoJson(data, {
    // Style each feature (in this case a neighborhood)
    style: function(feature) {
      if (maximum < feature.properties[map_variant]){
      }
      return {
        color: 'red',
        fillOpacity: chooseOpacity(feature.properties[map_variant], maximum),
        weight: 1
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
            fillOpacity: 1
          });
        },
        // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: chooseOpacity(feature.properties[map_variant], maximum)
          });
        }
      });
      // Giving each feature a pop-up with information pertinent to it
      layer.bindPopup("<strong>Zipcode</strong> " + feature.properties.zipcode + "<hr> <strong>" + map_variant + ":</strong> $" + feature.properties[map_variant]);

    }
  }).addTo(map);
});



var api_donations_url = '/api/donations/'
var api_parties_url = '/api/parties/'
