$(document).ready(  function() {
    socket = io.connect('http://127.0.0.1:5000'); // To establish connection with app.py

    socket.on('connect', function() { // Socket.on to receieve event from app.py
        console.log("New User...");
        socket.emit('event',{'name':"Malik sb"}); // To send request to an endpoint (function) in app.py
    });
    socket.on('connetion',function(data){
         console.log(String(data));
    });
});
