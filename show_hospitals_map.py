from taipy.gui import Html

html_page = Html("""
    <head>
        <script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBIeklfsRu1yz97lY2gJzWHJcmrd7lx2zU&libraries=places"></script>
        <script type="text/javascript">
            function initialize() {
                geocoder = new google.maps.Geocoder();
                var mapOptions = {
                }
                var locations = ["12836 University Club Dr", "2204 Fitness Club Way"];
                var markers = [];
                var iterator = 0;
                var bounds = new google.maps.LatLngBounds();

                for (var i = 0; i < locations.length; i++) {
                    setTimeout(function() {
                            geocoder.geocode({'address': locations[iterator]}, function(results, status){
                        if (status == google.maps.GeocoderStatus.OK) {
                            var marker = new google.maps.Marker({
                                map: map,
                                position: results[0].geometry.location,
                                animation: google.maps.Animation.DROP
                            });
                            bounds.extend(marker.getPosition());
                            map.fitBounds(bounds);
                        } else {
                            console.log('Geocode was not successful for the following reason: ' + status);
                        }
                    });
                    iterator++;

                    }, i * 250);
                }
                var map = new google.maps.Map(document.getElementById("map-canvas"), mapOptions);
        
            }
            google.maps.event.addDomListener(window, 'load', initialize);
        </script>
    </head>
    <body>
        <div id="map-canvas" style="width: 100%; height: 400px;"></div>
    </body>
""")