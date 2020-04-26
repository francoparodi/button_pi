function socketIOinit() {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    socket.on('connect', function() {
        console.log('Websocket connected');
    });

    socket.emit('handleDaemon', {name: '1', action: 'START'});

    socket.on('daemonProcess', function(data) {
        var jStr = JSON.stringify(data);
        var jObj = JSON.parse(jStr);
        var channel10 = jObj.channel10;
        var channel18 = jObj.channel18;
        console.log(jObj.datetime + ' ' + 'Channel10: ' + channel10 + " - Channel18: " + channel18);
        document.getElementById("channel10").innerHTML = channel10;
        document.getElementById("channel18").innerHTML = channel18;
    });
}