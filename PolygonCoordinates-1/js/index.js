var firebaseConfig = {
    apiKey: "AIzaSyAVa0wLquGouOx7zeZUfwzT-8W2x-dODK0",
    authDomain: "iotworldhackathon-b6bb4.firebaseapp.com",
    databaseURL: "https://iotworldhackathon-b6bb4.firebaseio.com",
    projectId: "iotworldhackathon-b6bb4",
    storageBucket: "iotworldhackathon-b6bb4.appspot.com",
    messagingSenderId: "933839958651",
    appId: "1:933839958651:web:c6ef1c038208af86"
};

// Initialize Firebase
firebase.initializeApp(firebaseConfig);
var database = firebase.database();

// window.onload=function(){ with (new XMLHttpRequest()) {
//   onreadystatechange=cb;
//   open('GET','/Users/mohitjain/Documents/IoTWorldHackathon/PolygonCoordinates/getCoordinates.txt',true);
//   responseType='text';
//   send();
// }}
//
// function cb(){
//   if(this.readyState===4) {
//     document.getElementById('main').innerHTML=tbl(this.responseText);
//   }
// }
//
// function tbl(csv) { // do whatever is necessary to create your table here ...
//  return csv.split('\n').map(function(tr,i) {
//    return '<tr><td>' + tr.replace(/\t/g,'</td><td>') +'</td></tr>';
//  }).join('\n');
// }

function initialize() {
  // Map Center
  var myLatLng = new google.maps.LatLng(33.5190755, -111.9253654);
  // General Options
  var mapOptions = {
    zoom: 12,
    center: myLatLng,
    mapTypeId: google.maps.MapTypeId.RoadMap
  };
  var map = new google.maps.Map(document.getElementById('map-canvas'),mapOptions);
  // Polygon Coordinates
  var triangleCoords = [
    new google.maps.LatLng(33.5362475, -111.9267386),
    new google.maps.LatLng(33.5104882, -111.9627875),
    new google.maps.LatLng(33.5004686, -111.9027061)
  ];
  // Styling & Controls
  myPolygon = new google.maps.Polygon({
    paths: triangleCoords,
    draggable: true, // turn off if it gets annoying
    editable: true,
    strokeColor: '#FF0000',
    strokeOpacity: 0.8,
    strokeWeight: 2,
    fillColor: '#FF0000',
    fillOpacity: 0.35
  });

  myPolygon.setMap(map);
  //google.maps.event.addListener(myPolygon, "dragend", getPolygonCoords);
  google.maps.event.addListener(myPolygon.getPath(), "insert_at", getPolygonCoords);
  //google.maps.event.addListener(myPolygon.getPath(), "remove_at", getPolygonCoords);
  google.maps.event.addListener(myPolygon.getPath(), "set_at", getPolygonCoords);
}

//Display Coordinates below map
function getPolygonCoords() {
  var len = myPolygon.getPath().getLength();
  var htmlStr = "";
  for (var i = 0; i < len; i++) {
    htmlStr += "(" + myPolygon.getPath().getAt(i).toUrlValue(5) + "),";
    //Use this one instead if you want to get rid of the wrap > new google.maps.LatLng(),
    //htmlStr += "" + myPolygon.getPath().getAt(i).toUrlValue(5);
  }
  firebase.database().ref('data/').set({
    coordinates: htmlStr
  }, function(error) {
    if (error) {
      console.log("The write to database failed");
    } else {
      console.log("Database Updated!");
    }
  });
  document.getElementById('info').innerHTML = htmlStr;
}
function copyToClipboard(text) {
  window.prompt("Copy to clipboard: Ctrl+C, Enter", text);
}
