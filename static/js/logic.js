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

// Function that will determine the color of a neighborhood based on the borough it belongs to
function chooseColor(indicator, maximum) {
  var H_value = (1 - (indicator / maximum))*100;
  return 'hsl(' + H_value + ', 100%, 50%)';
}

function chooseOpacity(indicator, maximum) {
  var H_value = (indicator / maximum);
  return H_value;
}

function generateMap (party, map_variant) {
  // Grabbing our GeoJSON data..
  d3.json("/api/donations/" + party, function(data) {
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
          // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to full so that it stands out
          mouseover: function(event) {
            layer = event.target;
            layer.setStyle({
              fillOpacity: 1
            });
          },
          // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to its original value
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
};

function buildDonationReport(party) { 

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
    console.log(features.zipcodes);     
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
  generateMap('TOTAL', 'donations_sum');
};

function optionChanged(party) {
  // Fetch new data each time a new sample is selected
  // buildMap(party);
  generateMap(party);
  console.log(party);
}

var submit = d3.select("#submit");

submit.on("click", function() {

  // Prevent the page from refreshing
  d3.event.preventDefault();

  // Select the input element and get the raw HTML node
  var inputElementZipcode = d3.select("#selectZipcode");
  var inputElementParty = d3.select("#selectParty");
  // var inputElementState = d3.select("#selectState");

  var zipcodeQuery = inputElementZipcode.property("value");
  var party = inputElementParty.property("value");
  // var searchState = inputElementState.property("value");

  console.log(zipcodeQuery);
  console.log(party);

  var url = '/zipcode/' + zipcodeQuery;

  d3.json(url).then(function(zip) {
    console.log(zip);
    // var coordinates = zip_response.coordinates;
    // url = '/pets/' + searchTerm;
    // d3.json(url).then(function(pet_response) {
    //   console.log(pet_response);
    //   createMarkers(pet_response, coordinates);
      
    // });
  });
  // mapElement.style('display', 'block');
  // frontElement.style('display', 'none');

  // var url = '/locations/' + zipcode;
});

// Initialize the dashboard
init();