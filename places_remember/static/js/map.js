function getPlace(placeObj) {
    var str ='';
    if (placeObj.country)
        str += placeObj.country;
    if (placeObj.city)
        str += ', ' + placeObj.city;
    if (placeObj.road)
        str += ', ' + placeObj.road;
    if (placeObj.house_number)
        str += ', ' + placeObj.house_number;
    return str;
}

function init(){
    // Create a map
    var map = new ol.Map({
        target:'map',
        layers: [],
        view: new ol.View({
            projection: 'EPSG:4326',
            center: [92.8720,56.0105], // Center in Krasnoyarsk
            zoom: 3,                  // Initial zoom
        }),
        controls:[
            new ol.control.Zoom(),
            new ol.control.ScaleLine(), // Create scale line
        ],
    });

    var osm = new ol.layer.Tile({
        title: 'OSM',
        /*source: new ol.source.OSM(
        {
            attributions: ['<a href="https://www.openstreetmap.org" target="_blank">OpenstreetMap</a> OpenstreetMap']
        })*/
        source: new ol.source.XYZ({
            url: "http://tile2.maps.2gis.com/tiles?x={x}&y={y}&z={z}&v=1.1"
        })
    });
    map.addLayer(osm);

    // Map layer with position marker
    var markers = new ol.layer.Vector({
      style: new ol.style.Style({   // Style of objects on layer
        image: new ol.style.Icon({
          src: '../../static/imgs/marker.png', // Marker image
          anchor: [0.5, 1], // The marker position relative to click point
          scale: 0.5, // Marker image compression value
        })
      })
    });
    map.addLayer(markers); // Add a layer to change its source


    // Get coordinates when user clicks on map
    map.on('click', function(evt){
        var coordinates = ol.proj.transform(evt.coordinate, 'EPSG:4326', 'EPSG:4326')
        // Create the Point object for adding it on map layer
        var marker = new ol.source.Vector({
            features: [
                new ol.Feature({
                    geometry: new ol.geom.Point(coordinates)
                })
            ]
        })

//        map.getView().setCenter(coordinates);

        var markerLayer = map.getLayers().getArray()[1]; // Take the second map layer (the first one is origin substrate)
        markerLayer.setSource(marker); // Set the marker to the second layer

        // Get geocoding data from Nominatim API
        var url = `https://nominatim.openstreetmap.org/reverse?lat=${coordinates[1]}&lon=${coordinates[0]}&format=geojson&accept-language=ru-RU`
        $.ajax({
            url: url,
            success: function(data) {
                var placeStr = getPlace(data.features[0].properties.address);
                console.log(placeStr)
                $('#id_place').attr('value', placeStr);
            }
        });
    });
}
