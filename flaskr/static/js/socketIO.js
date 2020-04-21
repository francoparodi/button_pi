function socketIOinit() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('Websocket connected');
    });

    socket.emit('handleDaemon', {name: '1', action: 'START'});

    socket.on('daemonProcess', function(data) {
        var jStr = JSON.stringify(data);
        var jObj = JSON.parse(jStr);
        var eventNumber = jObj.eventNumber;
        console.log(jObj.datetime + ' ' + eventNumber);
        document.getElementById("eventNumber").innerHTML = eventNumber;
    });
}