// Create a starting layer for donations data
var layers = {
  donations_sumLayer: new L.LayerGroup(),
  donations_medianLayer: new L.LayerGroup(),
  donations_countLayer: new L.LayerGroup()
};

// Creating map object
var map = L.map("map", {
  center: [40.1629, -89.1896],
  zoom: 6,
  layers: [layers.donations_sumLayer]
});

var baseMaps = {
  "Total Donations": layers.donations_sumLayer,
  'Median Donation': layers.donations_medianLayer,
  'Total Donors': layers.donations_countLayer
};

// Create a control for our layers, add our overlay layers to it
L.control.layers(baseMaps, null).addTo(map);

// Adding tile layer
L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  maxZoom: 18,
  id: "mapbox.dark",
  accessToken: "pk.eyJ1Ijoic3Jtb250ZWlybyIsImEiOiJjandyMTJzNjgwMDgyNDNwZDUwNWpkN2NoIn0.rggDqMijR64cH-l9E6JVag"
}).addTo(map);



// Function that will determine the color of a neighborhood based on the borough it belongs to
function chooseColor(indicator, maximum) {
  var H_value = (indicator / maximum)*180;
  return 'hsl(' + H_value + ', 100%, 50%)';
}

function chooseOpacity(indicator, maximum) {
  var H_value = (indicator / maximum);
  return H_value;
}

function addGeoJson(data, map_variant, layer){
  var maximum = data.maximums[map_variant]
  L.geoJson(data, {
    // Style each feature (in this case a neighborhood)
    style: function(feature) {
      return {
        color: chooseColor(feature.properties[map_variant], maximum),
        fillOpacity: 0.5,
        weight: 1
      };
    },
    // Called on each feature
    onEachFeature: function(feature, layer) {
      // Set mouse events to change map styling
      layer.on({
        // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to full so that it stands out
        mouseover: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.8
          });
        },
        // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to its original value
        mouseout: function(event) {
          layer = event.target;
          layer.setStyle({
            fillOpacity: 0.3
          });
        }
      });
      // Giving each feature a pop-up with information pertinent to it
      layer.bindPopup("<h5><a target='_blank' href='/zipcode/" + feature.properties.zipcode + "'>" + feature.properties.zipcode + "</a></h5>" + 
      "<hr> <strong>Total Donations:</strong> $" + feature.properties.donations_sum +
      "<br> <strong>Median Donation:</strong> $" + feature.properties.donations_median +
      "<br> <strong>Total Donors:</strong> " + feature.properties.donations_count);
    }
  }).addTo(layer);
};

function generateMap (party, map_variant) {
  // Grabbing our GeoJSON data.
  d3.json("/api/donations/" + party, function(data) {
    // Creating a geoJSON layer with the retrieved data
    layers.donations_sumLayer.clearLayers();
    addGeoJson(data, 'donations_sum', layers.donations_sumLayer);
    layers.donations_medianLayer.clearLayers();
    addGeoJson(data, 'donations_median', layers.donations_medianLayer);
    layers.donations_countLayer.clearLayers();
    addGeoJson(data, 'donations_count', layers.donations_countLayer);
    console.log('map updated');
  }); 
};

      
 // PARTY SELECTOR 

function init() {
  console.log('running init');
  // Grab a reference to the dropdown select element
  // Use the list of sample names to populate the select options
  d3.json('/api/parties/', function(data) {
    console.log(data.parties);     
    var partyArray = data.parties;
    var stateArray = ["Illinois - Free Version"]

    d3.select("#selectParty")
      .selectAll("option")
      .data(partyArray)
      .enter()
      .append("option")
      .text(function(d) {
        return d;
      })
      .property("value", function(d) {
        return d;
      });

    d3.select("#selectState")
      .selectAll("option")
      .data(stateArray)
      .enter()
      .append("option")
      .text(function(d) {
        return d;
      })
      .property("value", function(d) {
        return d;
      });
  });
  d3.json('/api/zipcodes/', function(features) {
    d3.select("#selectZipcode")
      .selectAll("option")
      .data(features.zipcodes)
      .enter()
      .append("option")
      .text(function(d) {
        return d;
      })
      .property("value", function(d) {
        return d;
      });
  
  });
  generateMap('', 'donations_sum');
};

function optionChanged(party) {
  // Fetch new data each time a new sample is selected
  // buildMap(party);
  console.log('optionChanged');
  console.log(party);
  generateMap(party, 'donations_sum');
}

// Initialize the dashboard
init();