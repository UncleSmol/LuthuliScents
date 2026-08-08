/* LuthuliScents — client-side cart backed by localStorage.
   Prices always come from data/products.json, never from the cart, so a
   tampered value cannot change the total. */

(function () {
  'use strict';

  window.CART_KEY = 'luthuliscents_cart';

  window.getCart = function () {
    try { return JSON.parse(localStorage.getItem(window.CART_KEY)) || {}; }
    catch (e) { return {}; }
  };

  window.saveCart = function (cart) {
    localStorage.setItem(window.CART_KEY, JSON.stringify(cart));
    window.updateCartBadge();
    if (typeof window.onCartChange === 'function') window.onCartChange();
  };

  window.addToCart = function (key) {
    var cart = window.getCart();
    cart[key] = (cart[key] || 0) + 1;
    window.saveCart(cart);
  };

  window.incrementCart = function (key) {
    window.addToCart(key);
  };

  window.decrementCart = function (key) {
    var cart = window.getCart();
    if (!cart[key]) return;
    cart[key] -= 1;
    if (cart[key] <= 0) delete cart[key];
    window.saveCart(cart);
  };

  window.removeFromCart = function (key) {
    var cart = window.getCart();
    delete cart[key];
    window.saveCart(cart);
  };

  window.clearCart = function () {
    window.saveCart({});
  };

  window.cartCount = function () {
    return Object.keys(window.getCart()).reduce(function (sum, k) {
      return sum + window.getCart()[k];
    }, 0);
  };

  /* Resolve cart entries into [{ product, quantity }] using the catalog. */
  window.cartItems = function () {
    var cart = window.getCart();
    return Object.keys(cart)
      .map(function (key) {
        var product = window.LS_PRODUCT(key);
        return product ? { product: product, quantity: cart[key] } : null;
      })
      .filter(Boolean);
  };

  window.cartSubtotal = function () {
    return window.cartItems().reduce(function (sum, item) {
      return sum + item.product.price * item.quantity;
    }, 0);
  };

  window.updateCartBadge = function () {
    var el = document.getElementById('cart-badge');
    if (!el) return;
    var n = window.cartCount();
    el.textContent = n > 0 ? String(n) : '';
    el.style.display = n > 0 ? 'inline-flex' : 'none';
  };
})();