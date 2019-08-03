var mapElement = d3.select('#map');

// SUBMIT ON CLICK

// // var zipcdeElement = d3.select('#selectZipcode');
var partyElement = d3.select('#selectParty');
// // var stateElement = d3.select('#selectState');


// // Select the submit button
var submit = d3.select("#submit");

submit.on("click", function() {

//   function buildMap(party) {

    d3.event.preventDefault();

//     // var inputElementZipcode = d3.select("#selectZipcode");
    var inputElementParty = d3.select("#selectParty");
//     // var inputElementState = d3.select("#selectState");

//     // var zipcodeQuery = inputElementZipcode.property("value");
    var searchParty = inputElementParty.property("value");
//     // var searchState = inputElementState.property("value");

    console.log(searchParty);
    

  }
);