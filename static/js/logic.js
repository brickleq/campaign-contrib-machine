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
// d3.json(link, function(data) {
//   // Creating a geoJSON layer with the retrieved data
//   var maximum = data.maximums[map_variant]
//   L.geoJson(data, {
//     // Style each feature (in this case a neighborhood)
//     style: function(feature) {
//       if (maximum < feature.properties[map_variant]){
//       }
//       return {
//         color: 'red',
//         fillOpacity: chooseOpacity(feature.properties[map_variant], maximum),
//         weight: 1
//       };
//     },
//     // Called on each feature
//     onEachFeature: function(feature, layer) {
//       // Set mouse events to change map styling
//       layer.on({
//         // When a user's mouse touches a map feature, the mouseover event calls this function, that feature's opacity changes to 90% so that it stands out
//         mouseover: function(event) {
//           layer = event.target;
//           layer.setStyle({
//             fillOpacity: 1
//           });
//         },
//         // When the cursor no longer hovers over a map feature - when the mouseout event occurs - the feature's opacity reverts back to 50%
//         mouseout: function(event) {
//           layer = event.target;
//           layer.setStyle({
//             fillOpacity: chooseOpacity(feature.properties[map_variant], maximum)
//           });
//         }
//       });
//       // Giving each feature a pop-up with information pertinent to it
//       layer.bindPopup("<strong>Zipcode</strong> " + feature.properties.zipcode + "<hr> <strong>" + map_variant + ":</strong> $" + feature.properties[map_variant]);

//     }
//   }).addTo(map);
// });


 // PARTY SELECTOR 

 function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selectParty");
  console.log(selector)
  // Use the list of sample names to populate the select options
  d3.json('/api/parties/', function(data) {
    console.log(data.parties);     
    var partyArray = data.parties;

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
    
    // // Use the first sample from the list to build the initial plots
    // const partyName = party[0];
    // console.log(partyName);
    // buildCharts(partyName);
    // buildMetadata(partyName);
  
});
}

function optionChanged(party) {
  // // Fetch new data each time a new sample is selected
  // buildCharts(party);
  // buildMetadata(party);
}

// Initialize the dashboard
init();



// ZIPCODE SELECTOR 

    // function init() {
    //   // Grab a reference to the dropdown select element
    //   var zipselector = d3.select("#selectZipcode");
    //   //console.log(selector)
    //   // Use the list of sample names to populate the select options
    //   d3.json("/api/census/").then((zipcode) => {
    //     //console.log(sampleNames[0]);
    //     zipcode.forEach((zip) => {
    //       zipselector
    //         .append("option")
    //         .text(zip)
    //         .property("value", zip);
          
    //     });
        
    //     // Use the first sample from the list to build the initial plots
    //     const firstZip = zipcode[0];
    //     console.log(firstZip);
    //     buildCharts(firstZip);
    //     buildMetadata(firstZip);
    //   });
    // }
    
    // function optionChanged(zipcode) {
    //   // Fetch new data each time a new sample is selected
    //   buildCharts(zipcode);
    //   buildMetadata(zipcode);
    // }



var api_donations_url = '/api/donations/'
var api_parties_url = '/api/parties/'
