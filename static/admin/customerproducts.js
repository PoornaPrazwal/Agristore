import {cart} from '../scripts/home.js';


let productprice=0;

const products = [{
  image:'/images/onions.jpg',
  name:'Onions',
  price:productprice
},{
  image:'/images/greenchilli.jpg',
  name:'Greenchill',
  price:productprice
},{
  image:'/images/tomatoes.jpg',
  name:'Tomatoes',
  price:productprice
},{
  image:'/images/brinjal.jpg',
  name:'Brinjal',
  price:productprice
},{
  image:'/images/potato.webp',
  name:'Potato',
  price:productprice
},{
  image:'/images/radish.jpg',
  name:'Radish',
  price:productprice
}];

let productsHTML = '';
products.forEach((product) => {
   productsHTML +=  `
    <div class="product-container">
          <div class="product-image-container">
            <img class="product-image"
              src="${product.image}">
          </div>
          <div class="product-name limit-text-to-2-lines">
            ${product.name}
          </div>
          <div class="product-price js-productprice">
            ${product.price}
          </div>
          <p class="product-kg">in kgs</p>
          <div class="product-quantity-container">
            <select>
              <option selected value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
              <option value="9">9</option>
              <option value="10">10</option>
            </select>
          </div>
          <div class="product-spacer"></div>
          <div class="added-to-cart">
            <img src="/images/checkmark.png">
            Added
          </div>
          <button class="add-to-cart-button button-primary js-add-to-cart"
            data-product-name="${product.name}">
            Add
          </button>
        </div>
    `; 
});
document.querySelector('.js-products-grid').innerHTML = productsHTML;

/* document.querySelectorAll('.js-productprice')
    .forEach((price) =>{

    
}); */

document.querySelectorAll('.js-add-to-cart')
    .forEach((button) =>{
        button.addEventListener('click', () => {
          const productName = button.dataset.productName;
          let matchingItem;
          cart.forEach((item) => {
            if(productName === item.productName){
              matchingItem = item;
            }
          });

          if(matchingItem){
            matchingItem.quantity += 1;
          }
          else{
            cart.push({
              productName : productName,
              quantity : 1
            });
          }

          let cartQuantity = 0;

          cart.forEach((item) => {
            cartQuantity += item.quantity;
          });

          document.querySelector('.js-cart-quantity')
            .innerHTML = cartQuantity;

          
    });
});