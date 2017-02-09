var loaded = 0;

MarkerClusterer.prototype.onClick = function() {
    return true;
};


ClusterIcon.prototype.triggerClusterClick = function(event) {
    var markerClusterer = this.cluster_.getMarkerClusterer();
    google.maps.event.trigger(markerClusterer, 'clusterclick', this.cluster_, event);

    var zoom = this.map_.getZoom();
    var maxZoom = markerClusterer.getMaxZoom();

    if (markerClusterer.isZoomOnClick()) {
        this.map_.fitBounds(this.cluster_.getBounds());
    }

    if (zoom >= maxZoom && this.cluster_.markers_ && this.cluster_.markers_.length > 1) {
        return showAllPreviews(markerClusterer);
    }
};

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: 50, lng: 0}
    });

    var markerCluster = new MarkerClusterer(map, [],
        {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});

    var ws = new WebSocket($('#ws_url').html());
    ws.onopen = function () {
        ws.send(JSON.stringify({
            tag: $('#tag').html(),
            count: $('#count').html()
        }))
    };

    ws.onmessage = function (evt) {
         addMarker(map, JSON.parse(evt.data), markerCluster);
    };
}

function addMarker(map, pic, cluster){
    var marker = new google.maps.Marker({
            position: {
                lat: pic.latitude,
                lng: pic.longitude
            },
            map: map,
            icon: {
                url: pic.preview,
                scaledSize: new google.maps.Size(32, 32)
            }
        });
    marker.picture_link = pic.image;
    cluster.addMarker(marker);
    marker.addListener('click', function () {
        showPicture(pic.image);
    });
    loaded++;
    $('#footer').html(loaded + 'of ' + $('#count').html())

}

function showAllPreviews(mc) {
    var cluster = mc.clusters_;
     if (cluster.length == 1 && cluster[0].markers_ && cluster[0].markers_.length > 1){
          var markers = cluster[0].markers_;
          var output = $('#modal_body');
          output.html('');
          for (var i=0; i < markers.length; i++)  {
              output.append('<img src="' + markers[i].icon.url +
                  '" onclick="showPicture(\'' + markers[i].picture_link +'\')"/>');
              $('#pic_modal').modal('show');
          }

          return false;
     }

     return true;
}

function showPicture(link) {
    $('#modal_body').html('<img src="' + link + '" alt="">');
    $('#pic_modal').modal('show');
}