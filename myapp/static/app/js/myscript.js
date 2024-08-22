//Increase Quantity 
$('.plus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =", id)
    $.ajax({
        type:"GET",
        url:"/pluscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data =", data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

//decrease Quantity 
$('.minus-cart').click(function(){
    var id=$(this).attr("pid").toString();
    var eml = this.parentNode.children[2]
    console.log("pid =", id)
    $.ajax({
        type:"GET",
        url:"/minuscart",
        data:{
            prod_id:id
        },
        success:function(data){
            console.log("data =", data);
            eml.innerText=data.quantity
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innerText=data.totalamount
        }
    })
})

//remove iteam from the cart
$('.remove-cart').click(function(){
    var id = $(this).attr("pid").toString();
    var eml=this
    $.ajax({
        type:"GET",
        url:"/removecart",
        data:{
            prod_id:id
        },
        success:function(data){
            document.getElementById("amount").innerText=data.amount
            document.getElementById("totalamount").innnerText=data.totalamount
            eml.parentNode.parentNode.parentNode.parentNode.remove()
            window.location.href = `http://127.0.0.1:8000/cart/`
        }
    })
})

//add product into wishlist
$('.plus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/pluswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://127.0.0.1:8000/product-detail/${id}`
        }
    })
})

//remove from wishlist
$('.minus-wishlist').click(function(){
    var id=$(this).attr("pid").toString();
    $.ajax({
        type:"GET",
        url:"/minuswishlist",
        data:{
            prod_id:id
        },
        success:function(data){
            window.location.href = `http://127.0.0.1:8000/product-detail/${id}`
        }
    })
})