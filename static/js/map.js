var loaded = 0;

function initMap() {
    var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: {lat: 50, lng: 0}
    });
    var ws = new WebSocket($('#ws_url').html());
    ws.onopen = function () {
        ws.send(JSON.stringify({
            tag: $('#tag').html(),
            count: $('#count').html()
        }))
    };
    ws.onmessage = function (evt) {
         addMarker(map, JSON.parse(evt.data));
    };
}

function addMarker(map, pic){
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
    marker.addListener('click', function () {
        $('#modal_body').html('<img src="' + pic.image + '" alt="">');
        $('#pic_modal').modal('show');
    });
    loaded++;
    $('#footer').html(loaded + 'of ' + $('#count').html())

}