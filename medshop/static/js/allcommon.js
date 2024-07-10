
const fadeOut=()=>{
const loader=document.querySelector(".preloader");
loader.classList.remove("preloader");
}

window.addEventListener("load",function(){
setTimeout(fadeOut,1000);
});
      
function addToCart(product_id, product_name,product_discounted_price,user, product_perpack_mrp,product_img_url,prescription_status,remaining_stock) {
if(user !='none' && user){
console.log(prescription_status);

let cart = JSON.parse(localStorage.getItem('cart')) || [];
let found = false;

cart.forEach(item => {
    if (item.product_id === product_id && item.count<remaining_stock) {
        item.count += 1;
        found = true;
    }
    else if(item.product_id === product_id && item.count>=remaining_stock){
        alert("limit exceeded");
        found=true;
    }
});

if (!found) {
    let newItem = {
        user:user,
        product_id: product_id,
        product_name: product_name,
        product_perpack_mrp:product_perpack_mrp,
        product_discounted_price:product_discounted_price,
        product_img_url:product_img_url,
        prescription_status:prescription_status,
        remaining_stock:remaining_stock,
        count: 1
    };
    cart.push(newItem);
}

localStorage.setItem('cart', JSON.stringify(cart));
console.log(cart);
updateCart();
}
else{
alert("Please login first to continue buying");
}
}
function updateCart(){
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let t_count=0;
console.log("b");
if (cart){
cart.forEach(item => {
    t_count +=item.count;
});

}
console.log(t_count);
let x=document.getElementById('cartCount');
x.innerHTML=t_count;
console.log(x);

}
let cart = JSON.parse(localStorage.getItem('cart')) || [];
let t_count=0;
console.log("b");
if (cart){
cart.forEach(item => {
    t_count +=item.count;
});

}
console.log(t_count);
let x=document.getElementById('cartCount');
x.innerHTML=t_count;
console.log(x);



var swiper = new Swiper(".mySwiper", {
    slidesPerView: 4,
    centeredSlides: false,
    spaceBetween: 0,
    pagination: {
    el: ".swiper-pagination",
    type: "fraction",
    },
    navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
    },
    breakpoints: {
    200: {
        slidesPerView: 1,
        spaceBetween: 10,
    },
    350: {
        slidesPerView: 1,
        spaceBetween: 20,
    },
    500: {
        slidesPerView: 1,
        spaceBetween: 10,
    },
    580: {
        slidesPerView: 1,
        spaceBetween: 10,
    },
    616: {
        slidesPerView: 1,
        spaceBetween: 10,
    },
    640: {
        slidesPerView: 2,
        spaceBetween: 10,
    },
    700: {
        slidesPerView: 1,
        spaceBetween: 10,
    },
    768: {
        slidesPerView: 2,
        spaceBetween: 0,
    },
    902: {
        slidesPerView: 2,
        spaceBetween: 10,
    },
    1024: {
        slidesPerView: 3,
        spaceBetween: 10,
    },
    1450: {
        slidesPerView: 4,
        spaceBetween: 10,
    },
    1600: {
        slidesPerView: 4,
        spaceBetween: 10,
    },
    

    },
});




  

function RemoveCurrentUserItems(){
    let cart = JSON.parse(localStorage.getItem('cart')) || [];
    if(cart){
    localStorage.removeItem('cart');
    }
}
    


function SearchFunction(search_list){
    console.log(search_list)
    let search_list_decoded=JSON.parse(search_list);
    console.log(search_list_decoded)
    const searchInput = document.getElementById('search');
    const suggestionsList = document.getElementById('suggestions');
    
    
    let items=[];
    if(search_list_decoded){
        search_list_decoded.forEach(item =>{
        items.push(item);
        });
    }
    console.log(items);
    


    searchInput.addEventListener('input', handleInput);

    function handleInput() {
        
        if (searchInput.value.trim() === "") {
            suggestions.style.display = "none"; 
        } else {
            suggestions.style.display = "block";
        }
        const query = searchInput.value.toLowerCase();
        
        const filteredItems = items.filter(item => item.toLowerCase().includes(query));
        displaySuggestions(filteredItems);
    }

    function displaySuggestions(suggestions) {
        suggestionsList.innerHTML = '';
        suggestions.forEach(suggestion => {
            const listItem = document.createElement('li');
            listItem.classList.add('suggestion-item');
            listItem.textContent = suggestion;
            listItem.addEventListener('click', () => {
                searchInput.value = suggestion;
                suggestionsList.innerHTML = '';
            });
            suggestionsList.appendChild(listItem);
        });
    }
    
}

SearchFunction(search_list_json);


