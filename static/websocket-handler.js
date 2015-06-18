(function() {
    function attemptConnection() {
        console.info('Attempting reconnection');
        new SocketHandler();
    }

    function SocketHandler() {
        this.socket = new WebSocket('ws://localhost:8888/ws');

        this.socket.onmessage = function(evt) {
            document.getElementById('main').innerHTML = evt.data;
        };

        this.socket.onerror = function(evt) {
            console.info('an error occurred: ' + evt);
        };

        this.socket.onopen = function(evt) {
            console.info('Connection established');
        };

        this.socket.onclose = function() {
            console.info('Connection closed');
            document.getElementById('main').innerHTML = '<img src="/static/stand-by.jpg" alt="">';
            window.setTimeout(attemptConnection, 1000);
        };
    }

    new SocketHandler();
})();