$(document).ready(  function() {
    socket = io.connect('http://127.0.0.1:5000'); // To establish connection with app.py

    socket.on('connect', function() { // Socket.on to receieve event from app.py
        console.log("New User...");
        socket.emit('event',{'name':"Malik sb"}); // To send request to an endpoint (function) in app.py
    });
    socket.on('connetion',function(data){
         console.log(String(data));
    });
    socket.on('charges_total_header',function(data){
        if(document.getElementById('charges_total_header'))
        {
            document.getElementById('charges_total_header').innerHTML = 'Charges: '+String(data['charges'])+'   Total: '+String(data['total']);
        }
    });
    socket.on('viewCartItem',function(data){
        if(data['flag'] == 0)
            document.getElementById('header_cart').innerHTML = data['html'];
        else
        document.getElementById('mobile_header_cart').innerHTML = data['html'];
     });
    socket.on('wishlistItem',function(data){
        if(data['flag'] == 0)
            document.getElementById('wishlistItem').innerHTML = data['html'];
        else
        document.getElementById('mobile_header_wishlist').innerHTML = data['html'];
     });
    socket.on('cart_removed_via_email',function(data){
         if(data)
         {
             let entities= document.querySelectorAll(".total");
            let total = 0;
            //console.log(entities.length);
            let all_data = []
            for(let i=0;i<entities.length;i++)
            {
                all_data.push({'id':document.getElementById("image_"+String(i)).getAttribute('title'), 'quantity': document.getElementById("item-"+String(i)).value});
            }
            console.log(all_data);
            socket.emit('add_to_cart', {'check':"update_add_to_cart...!",'all_data':all_data,'id':null});
         }
    });
});
