
function swap_LtoR(LtoRval){
let swapLtoR=document.getElementById('items_on_pgid');
let disable_btn=document.getElementById('offcanvasRightid');

if(LtoRval=='L'){
    disable_btn.disabled=true;
    swapLtoR.style.flexDirection="row-reverse";
}
else{
    disable_btn.disabled=false;
    swapLtoR.style.flexDirection="row";
}
}



function del_ThatItem(product_id){

console.log(product_id);
let cart = JSON.parse(localStorage.getItem('cart'));
console.log("django",cart);
const itemIdToRemove = product_id; 

if (cart) {
    cart.forEach(function(item,index) {
    if(item.product_id == itemIdToRemove){
        console.log("deleted")
        cart.splice(index,1);  
    }
        
    }
    )
    console.log("bhop",product_id);
}
localStorage.setItem('cart', JSON.stringify(cart));



}


  
    
function displayCartItems() {
// Retrieve the 'cart' item from local storage
    var cartItemsString = localStorage.getItem('cart');

    // Check if the 'cart' item exists
    if (cartItemsString !== null) {
    // Parse the 'cart' item as JSON (assuming it's stored as an array of strings)
    var cartItemsArray = JSON.parse(cartItemsString);

    // Access each item and display it on the HTML page
    var cartItemsContainer = document.getElementById('cart-Items');
    cartItemsArray.forEach(function(item) {
        var div_innerconatainer=document.createElement('div');
        var div_miditemscontainer=document.createElement('div');
        var div_productimg = document.createElement('div');
        var imgtag_productimg = document.createElement('img');
        console.log(item.product_img_url)
        imgtag_productimg.src=item.product_img_url
        imgtag_productimg.alt='product'
        div_productimg.appendChild(imgtag_productimg)
        var div_delete_particular_item=document.createElement('div');
        var div1 = document.createElement('div');
        var div2 = document.createElement('div');
        var div3 = document.createElement('div');

        div_innerconatainer.classList.add('cart-item-innercontainer');
        div_miditemscontainer.classList.add('miditemscontainer')
        div_delete_particular_item.classList.add('del_particular_item')
        div_productimg.classList.add('product-img-oncheckout-container')
        div_delete_particular_item.innerHTML=`<a href="" onclick="del_ThatItem(${item.product_id})"><i class="fa-solid fa-trash-can"></i></a>`
        div1.textContent = item.product_name;
        div1.classList.add('cart-item-desc');
        div2.innerHTML = `<a href="" class="btn-red" onclick="subReduce(${item.product_id})"><i class="fa-solid fa-minus"></i></a><span id="${item.product_id}">${item.count}</span><a href="" id="more-btn" onclick="addMore(${item.product_id})" class="btn-green"><i class="fa-solid fa-plus"></i></a>`;

        div2.classList.add('cart-item-count');
        div3.textContent = `Rs.${item.product_discounted_price}`;
        div3.classList.add('cart-item-price');
        div_innerconatainer.appendChild(div_productimg);
        div_miditemscontainer.appendChild(div1);
        div_miditemscontainer.appendChild(div3);
        div_miditemscontainer.appendChild(div2);
        div_innerconatainer.appendChild(div_miditemscontainer)
        div_innerconatainer.appendChild(div_delete_particular_item);
        cartItemsContainer.appendChild(div_innerconatainer);
        
    });
    } else {
    var pagecontent_frstpart=document.getElementById('total-cart-items-show-id');
    var cartemp=document.getElementById('cartemp');
    var footercontent=document.getElementById('footer-id');
    pagecontent_frstpart.style.display="none";
    footercontent.style.display="none";
    document.body.style.backgroundColor="#ddd";
    var div_cartempty=document.createElement('div');
    div_cartempty.innerHTML=`<img src="/static/media/cartempty.jpeg" alt="..." class="emptycartimg"> <p class=emptycartpara">OHHH!!!!!! The Cart is empty,please add medicines to continue further. </p>`;
    div_cartempty.classList.add('whencartemptycls');
    cartemp.appendChild(div_cartempty);
    console.log('No items found in the cart.');
    }
}

// Call the function to display cart items when the page loads
displayCartItems();
function addMore(medicine_id){
    var cartItemsString = localStorage.getItem('cart');
    console.log(medicine_id);
    // Check if the 'cart' item exists
    if (cartItemsString !== null) {
    // Parse the 'cart' item as JSON (assuming it's stored as an array of strings)
    var cartItemsArray = JSON.parse(cartItemsString);}
    cartItemsArray.forEach((item)=>{
    if(item.product_id==medicine_id && item.count){
        item.count +=1;
        document.getElementById(`${item.product_id}`).innerHTML=item.count;
    }
    
    })
    console.log("sskd");
    localStorage.setItem('cart', JSON.stringify(cartItemsArray));
    Cart_calculator();
}

function subReduce(medicine_id){
    var cartItemsString = localStorage.getItem('cart');
    console.log(medicine_id);
    // Check if the 'cart' item exists
    if (cartItemsString !== null) {
    // Parse the 'cart' item as JSON (assuming it's stored as an array of strings)
    var cartItemsArray = JSON.parse(cartItemsString);}
    cartItemsArray.forEach((item,index)=>{
    if(item.product_id==medicine_id && item.count>1){
        item.count -=1;
        document.getElementById(`${item.product_id}`).innerHTML=item.count;
    }
    else if(item.product_id==medicine_id && item.count==1){
        item.count -=1;
        document.getElementById(`${item.product_id}`).innerHTML=item.count;
        cartItemsArray.splice(index,1); 
        
    }  
    })
    console.log("sskd232e");
    localStorage.setItem('cart', JSON.stringify(cartItemsArray));
    Cart_calculator();
}

function Cart_calculator(){
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    let f=0;
    cart.forEach(item=>{
    if(item.count==0){
        f+=1;
    }})
    
    console.log("su1");
    function Cart_totprice(){
    let tprice=0;
    let toPay=0;
    let tdiscount=0;
    let tdiscountTotal=0;
    if(cart){
        cart.forEach(item=>{
        tprice += Number(item.product_discounted_price)*item.count;
        tdiscount =Number(item.product_perpack_mrp-item.product_discounted_price);
        tdiscountTotal +=tdiscount*item.count;
        
    });
        tdiscountTotal=parseFloat(tdiscountTotal.toPrecision(3));
        tprice=parseFloat(tprice.toPrecision(3));
        tdiscount=parseFloat(tdiscount.toPrecision(3));
        document.getElementById('cart_total_item_id').innerHTML=`Rs.${tprice}`;
        document.getElementById('cart_discount_item_id').innerHTML=`Rs.${tdiscountTotal}`;
        toPay=tprice +49;
        let sum=document.getElementById('topay_sumid');
        if(toPay==49){
        sum=0
        }
        else{
        sum.value=toPay
        }
        
        
        document.getElementById('cart_toPay_item_id').innerHTML=`Rs.${toPay}`;
        if(tprice>0){
        document.getElementById('savings-paraid').innerHTML=`<center>You saved ₹${tdiscountTotal} on this order<center/>`;
        document.getElementById('savings-total-valueid').innerHTML=`Savings<br>(i)Discount On MRP ₹${tdiscountTotal}`;
        }
        else{
        console.log("vmmvm");
        document.getElementById('cart_deliver_charges_item_id').innerHTML="Rs 0";
        toPay=0;
        document.getElementById('cart_toPay_item_id').innerHTML=`Rs.${toPay}`;
        let x=document.getElementById('total-savings-containerid');
        x.style.display="none";
        
        }
        
        
    }
    
    console.log("su2");
    }
    if(f==cart.length){
    localStorage.removeItem('cart');
    }
    
    Cart_totprice();
    
    

}
Cart_calculator();


function sendCartItems(){
cart = JSON.parse(localStorage.getItem('cart')) || [];
console.log("sidd",cart);
function getCSRFToken() {
    const csrfCookie = document.cookie.match(/csrftoken=([^ ;]+)/);
    return csrfCookie ? csrfCookie[1] : null;
}

// Get the CSRF token
const csrftoken = getCSRFToken();
console.log(csrftoken)
fetch('/med_cart/',{
    
    method:'POST',
    headers:{
    'Content-Type':'application/json',
    'X-CSRFToken':csrftoken,
    },
    body:JSON.stringify({cart:cart}),
})
.then(response=>response.json())
.then(data=>{
    console.log(data);
})
.catch(error=>console.error('Error:',error));
}




function cartSend(){
let validate_add=document.getElementById('useraddress');
let validate_email=document.getElementById('inputEmail');
let validate_no=document.getElementById('inputContactNumber');
let validate_City=document.getElementById('inputCity');
let validate_State=document.getElementById('inputState');
let validate_Zip=document.getElementById('inputZip');
let validate_Check=document.getElementById('gridCheck');
if(validate_add.value && validate_email.value && validate_City.value && validate_State.value && validate_no.value && validate_Zip.value && validate_Check.checked ){
    let dataToSend=localStorage.getItem('cart');
    document.getElementById('cart_dataid').value=dataToSend;
}
else{
    alert("Please Fill All The Delivery Details Correctly");
}

}

function UploadPrescription(){
    let cart = JSON.parse(localStorage.getItem('cart'));
    if(cart){
        cart.forEach(item=>{
            console.log("csssskdkdkdkdkdskd")
            if(item.prescription_status=="True"){
                
                console.log("vmijfjwjfjw");
                document.getElementById('Prescription').style.display="inline";
                console.log("ms;mc;")
            }
        });
    }
}

UploadPrescription();






